pipeline {
    agent any
    stages {
        stage('Cloning Github Repository') {
            steps {
                echo 'Cloning GitHub Repository...'
                // Using git step with credentials and branch
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/sachin62025/MLOps-project.git'
            }
        }
    }
}