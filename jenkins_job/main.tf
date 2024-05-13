resource "jenkins_folder" "this" {
  name = "devops_fullstack"
}

resource "jenkins_job" "this" {
  name = "devops_fullstack_site"
  template = templatefile("${path.module}/job.xml", {
    description = "Deploying devops fullstack site"
  })
  folder = jenkins_folder.this.id
}