pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning GitHub Repository') {
            steps {
                echo 'Cloning GitHub Repository...'
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/sachin62025/MLOps-project.git'
            }
        }

        stage('Setting up Virtual Environment and Installing Dependencies') {
            steps {
                echo 'Setting up virtual environment and installing dependencies...'
                sh """
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                """
            }
        }
    }
}
