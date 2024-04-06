# import boto3, to access aws resources
import boto3
import time

# Initialize Boto3 clients - ec2, autoscaling, elbv2 and route53
ec2_client = boto3.client('ec2')
autoscaling_client = boto3.client('autoscaling')
elb_client = boto3.client('elbv2')
route53_client = boto3.client('route53')

# function to define vpc, subnets and also igw and nat gateways
def create_vpc_and_subnets():

    # Created VPC
    vpc_response = ec2_client.create_vpc(CidrBlock='10.0.0.0/16')

    # storing vpc id, as we need it to associate other resources
    vpc_id = vpc_response['Vpc']['VpcId']
    

    # Create Internet Gateway and attach it to the VPC
    igw_response = ec2_client.create_internet_gateway()

    # getting internet gateway id
    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    # attach the internet gateway with the VPC id
    ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    
    # Create route table for public subnets
    public_route_table_response = ec2_client.create_route_table(VpcId=vpc_id)

    # storing the public route table id
    public_route_table_id = public_route_table_response['RouteTable']['RouteTableId']

    # create route this is public, so attach to the igw
    ec2_client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id,
        RouteTableId=public_route_table_id
    )
    
    # Create route table for private subnets
    private_route_table_response = ec2_client.create_route_table(VpcId=vpc_id)

    # not attaching the private route to anything at this time
    private_route_table_id = private_route_table_response['RouteTable']['RouteTableId']
    
    # Create 3 public subnets
    public_subnet_ids = []
    for i in range(3):
        subnet_response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=f'10.0.0.{i}/24')
        subnet_id = subnet_response['Subnet']['SubnetId']
        ec2_client.associate_route_table(RouteTableId=public_route_table_id, SubnetId=subnet_id)
        public_subnet_ids.append(subnet_id)
    
    # Create NAT Gateway
    nat_gateway_response = ec2_client.create_nat_gateway(SubnetId=public_subnet_ids[0])
    nat_gateway_id = nat_gateway_response['NatGateway']['NatGatewayId']
    
    # Wait for NAT Gateway to be available
    while True:
        response = ec2_client.describe_nat_gateways(NatGatewayIds=[nat_gateway_id])
        if response['NatGateways'][0]['State'] == 'available':
            break
        time.sleep(10)
    
    # Associate private subnets with the route table and NAT Gateway
    for i in range(3):
        ec2_client.associate_route_table(RouteTableId=private_route_table_id, SubnetId=public_subnet_ids[i])
        ec2_client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            NatGatewayId=nat_gateway_id,
            RouteTableId=private_route_table_id
        )
    return vpc_id, public_subnet_ids

def create_load_balancer_and_asg(vpc_id, public_subnet_ids,security_group_id):
    # Create Load Balancer
    elb_response = elb_client.create_load_balancer(
        Name='MyLoadBalancer',
        Subnets=public_subnet_ids,
        SecurityGroups=[security_group_id],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'MyLoadBalancer'
            },
        ]
    )
    elb_arn = elb_response['LoadBalancers'][0]['LoadBalancerArn']
    
    # Define Auto Scaling Group
    autoscaling_response = autoscaling_client.create_auto_scaling_group(
        AutoScalingGroupName='MyAutoScalingGroup',
        LaunchConfigurationName='MyLaunchConfiguration',
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=2,
        VPCZoneIdentifier=','.join(public_subnet_ids),
        AvailabilityZones=['ap-south-1a'],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'MyASG'
            },
        ]
    )

    return elb_arn

def configure_dns(elb_arn):
    # Configure DNS using Route 53
    # Example: Create a hosted zone and add records
    hosted_zone_response = route53_client.create_hosted_zone(
        Name='example.com',
        CallerReference=str(time.time())
    )
    hosted_zone_id = hosted_zone_response['HostedZone']['Id'].split('/')[-1]
    route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'example.com',
                        'Type': 'A',
                        'AliasTarget': {
                            'DNSName': elb_arn,
                            'EvaluateTargetHealth': False,
                            'HostedZoneId': 'hosted_zone_id'
                        }
                    }
                }
            ]
        }
    )

# Main function
def main():
    vpc_id, public_subnet_ids = create_vpc_and_subnets()
    elb_arn = create_load_balancer_and_asg(vpc_id, public_subnet_ids)
    configure_dns(elb_arn)

if __name__ == "__main__":
    main()