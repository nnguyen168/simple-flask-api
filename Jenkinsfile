def CONTAINER_NAME="jenkins-pipeline"
def CONTAINER_TAG="latest"
def DOCKER_HUB_USER="6626"
def HTTP_PORT="8090"

node {
	
	stage('Initialize'){
		def dockerHome = tool 'myDocker'
		def mavenHome = tool 'myMaven'
		env.PATH = "${dockerHome}/bin:${mavenHome}/bin:${env.PATH}"
	}

	stage('Checkout') {
		checkout scm
	}
}
