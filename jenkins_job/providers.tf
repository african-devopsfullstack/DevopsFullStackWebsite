terraform {
  required_providers {
    jenkins = {
      source  = "taiidani/jenkins"
      version = "0.10.2"
    }
  }
}

provider "jenkins" {
  server_url = "https://jenkins-lab.africantech.dev"
  username   = var.JENKINS_USERNAME
  password   = var.JENKINS_PASSWORD
}