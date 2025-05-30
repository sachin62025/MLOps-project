
pipline{
    agent any
    stages{
        stages('Cloning Github Repository'){
            steps{
                script{
                    echo 'Cloning GitHub Repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/sachin62025/MLOps-project.git']]) 
                }
            }
        }
    }
}

