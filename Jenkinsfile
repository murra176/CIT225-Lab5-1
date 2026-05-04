pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/flask-final'   // CHANGE
        DOCKER_CREDS = 'docker-creds'                          // CHANGE IF NEEDED
        GIT_REPO = 'YOUR_GITHUB_REPO_URL'                      // CHANGE
    }

    stages {

        stage('Checkout') {
            steps {
                git "${GIT_REPO}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install flake8'
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh 'flake8 . || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push $DOCKER_IMAGE:$BUILD_NUMBER'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                sed -i "s|image: .*|image: $DOCKER_IMAGE:$BUILD_NUMBER|" deployment-dev.yaml
                kubectl apply -f deployment-dev.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get pods'
                sh 'kubectl get services'
            }
        }
    }
}
