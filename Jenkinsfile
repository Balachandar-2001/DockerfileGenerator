pipeline {

    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        DOCKER_USERNAME = "30balachandar333"

        BACKEND_IMAGE = "30balachandar333/dockergen-backend"
        FRONTEND_IMAGE = "30balachandar333/dockergen-frontend"

        KUBE_NAMESPACE = "dockergen"

        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                echo "Building Backend Image..."

                sh """
                    docker build \
                    -t ${BACKEND_IMAGE}:${BUILD_NUMBER} \
                    ./backend
                """
            }
        }

        stage('Build Frontend Image') {
            steps {
                echo "Building Frontend Image..."

                sh """
                    docker build \
                    -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                    ./frontend
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
                        echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''
                }

            }
        }

        stage('Push Docker Images') {

            steps {

                echo "Pushing Backend Image..."

                sh """
                    docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}
                """

                echo "Pushing Frontend Image..."

                sh """
                    docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                """

            }

        }

        stage('Deploy Backend') {

            steps {

                echo "Updating Backend Deployment..."

                sh """
                    kubectl set image deployment/backend \
                    backend=${BACKEND_IMAGE}:${BUILD_NUMBER} \
                    -n ${KUBE_NAMESPACE}

                    kubectl rollout status deployment/backend \
                    -n ${KUBE_NAMESPACE}
                """

            }

        }

        stage('Deploy Frontend') {

            steps {

                echo "Updating Frontend Deployment..."

                sh """
                    kubectl set image deployment/frontend \
                    frontend=${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                    -n ${KUBE_NAMESPACE}

                    kubectl rollout status deployment/frontend \
                    -n ${KUBE_NAMESPACE}
                """

            }

        }

        stage('Verify Deployment') {

            steps {

                echo "Verifying Pods..."

                sh """
                    kubectl get pods -n ${KUBE_NAMESPACE}
                """

            }

        }

    }

    post {

        success {

            echo "======================================"
            echo "Deployment Successful"
            echo "Build Number : ${BUILD_NUMBER}"
            echo "======================================"

        }

        failure {

            echo "======================================"
            echo "Deployment Failed"
            echo "======================================"

        }

        always {

            sh '''
                docker logout || true
                docker image prune -af || true
            '''

            cleanWs()

        }

    }

}
