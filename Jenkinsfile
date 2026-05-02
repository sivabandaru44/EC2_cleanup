pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
    }

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'pip install boto3'
            }
        }

        stage('Run Cleanup') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat 'python cleanup_ec2.py'
                }
            }
        }
    }
}
