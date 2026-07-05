pipeline {

    agent any

    environment {
        DOCKER_USERNAME = "30balachandar333"
        BACKEND_IMAGE = "30balachandar333/dockergen-backend"
        FRONTEND_IMAGE = "30balachandar333/dockergen-frontend"
        KUBE_NAMESPACE = "dockergen"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                sh """
                docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend
                """
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh """
                docker build -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} ./frontend
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Images') {
            steps {

                sh """
                docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}
                docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                """

            }
        }

        stage('Deploy Backend') {

            steps {

                sh """
                export KUBECONFIG=/var/lib/jenkins/.kube/config

                kubectl set image deployment/backend \
                backend=${BACKEND_IMAGE}:${BUILD_NUMBER} \
                -n ${KUBE_NAMESPACE}

                kubectl rollout status deployment/backend -n ${KUBE_NAMESPACE}
                """

            }

        }

        stage('Deploy Frontend') {

            steps {

                sh """
                export KUBECONFIG=/var/lib/jenkins/.kube/config

                kubectl set image deployment/frontend \
                frontend=${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                -n ${KUBE_NAMESPACE}

                kubectl rollout status deployment/frontend -n ${KUBE_NAMESPACE}
                """

            }

        }

    }

    post {

        always {

            sh "docker image prune -f"

            cleanWs()

        }

    }

}
