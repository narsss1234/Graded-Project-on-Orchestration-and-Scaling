pipeline{

    agent any

    stages{

        stage('Fetch the code'){
            steps{
                script{
                    git branch: 'main', url: 'ssh://git-codecommit.ap-south-1.amazonaws.com/v1/repos/Graded-Project-on-Orchestration-and-Scaling'
                }
            }
        }

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
    }
}