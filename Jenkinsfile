pipeline{

    agent any

    stages{

        stage('Configure AWS Credentials') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY',
                    credentialsId: 'aws' // Replace with your Jenkins credentials ID
                ]]) {
                    sh 'aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID'
                    sh 'aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY'
                    sh 'aws configure set region ap-south-1'
                }
            }
        }


        stage('Fetch the code'){
            steps{
                script{
                    git branch: 'main', url: 'ssh://git-codecommit.ap-south-1.amazonaws.com/v1/repos/Graded-Project-on-Orchestration-and-Scaling'
                }
            }
        }

        stage('checking the folder'){
            steps{
                script{
                    sh 'ls'
                }
            }
        }

        stage('Build the docker backend image 1'){
            steps{
                script{
                    sh 'cd backend/helloService && docker build -t 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-hello:latest .'
                }
            }
        }

        stage('Build the docker backend image 2'){
            steps{
                script{
                    sh 'cd backend/profileService && docker build -t 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-profile:latest .'
                }
            }
        }

        stage('Build the docker frontend image'){
            steps{
                script{
                    sh 'cd frontend && docker build -t 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-frontend:latest .'
                }
            }
        }

        stage('Configure ECR and push the images'){
            steps{
                script{
                    sh 'aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 367065853931.dkr.ecr.ap-south-1.amazonaws.com'
                    sh 'docker push 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-hello:latest'
                    sh 'docker push 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-profile:latest'
                    sh 'docker push 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-frontend:latest'
                }
            }
        }
    }
}