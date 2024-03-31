pipeline{

    agent any

    stages{

        stage('Fetch the code'){
            steps{
                script{
                    git branch: 'master', url: 'https://git-codecommit.ap-south-1.amazonaws.com/v1/repos/Graded-Project-on-Orchestration-and-Scaling-Code-Commit'
                }
            }
        }
    }
}