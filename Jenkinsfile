pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
        SCANNER_HOME = tool 'sonar-scanner'
        IMAGE_NAME = 'idrisniyi94/devopsfullstack-site'
        IMAGE_TAG = "v.0.0.${BUILD_NUMBER}"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                git branch 
    }
}