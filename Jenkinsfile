pipeline{

    agent any

    stages{

        // stage('Lets configure AWS'){
        //     steps{
        //         script{
        //             withCredentials([
        //                 usernamePassword(credentialsId: 'aws', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')
        //                 ]) {
        //                     sh 'aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID'
        //                     sh 'aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY'
        //                     sh 'aws configure set region ap-south-1'
        //             }
        //         }
        //     }
        // }

        stage('Fetch the code'){
            steps{
                script{
                    git branch: 'main', url: 'https://git-codecommit.ap-south-1.amazonaws.com/v1/repos/Graded-Project-on-Orchestration-and-Scaling'
                }
            }
        }
    }
}