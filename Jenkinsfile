pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/sivabandaru44/EC2_cleanup.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install boto3'
            }
        }

        stage('Run Cleanup') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat 'python cleanup_ec2.py'
                }
            }
        }
    }
}
