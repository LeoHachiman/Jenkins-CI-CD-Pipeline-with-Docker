# Jenkins CI/CD Pipeline with Docker

**An open-source Cloud & DevOps project demonstrating automated CI/CD with Jenkins, Docker, Python, pytest, GitHub, and Google Cloud Platform.**

![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Pytest](https://img.shields.io/badge/Testing-pytest-green)
![GCP](https://img.shields.io/badge/Cloud-GCP-4285F4)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

This project demonstrates a practical **Continuous Integration and Continuous Deployment (CI/CD)** workflow using Jenkins and Docker.

The pipeline connects a GitHub repository to Jenkins through a webhook. Whenever new code is pushed, Jenkins automatically retrieves the latest source code, installs the required dependencies, runs automated tests, builds a Docker image, and deploys the resulting container.

The project is designed as a reproducible learning and reference implementation for developers building practical skills in **Cloud Engineering, DevOps, CI/CD, containerization, and automated testing**.

---

## 🚀 What This Project Does

When code is pushed to GitHub, Jenkins executes the following workflow:

```text
GitHub Push
     │
     ▼
Jenkins Webhook
     │
     ▼
┌─────────────────────┐
│  1. Checkout        │
│  Get latest source  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  2. Install         │
│  Dependencies       │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  3. Test            │
│  Run pytest         │
└──────────┬──────────┘
           │
      Tests pass?
       /       \
     No         Yes
     │           │
     ▼           ▼
   STOP      4. Build
                 │
                 ▼
          Docker Image
                 │
                 ▼
            5. Deploy
                 │
                 ▼
          Running Container
```

### Pipeline behavior

* Source code is automatically pulled from GitHub.
* Python dependencies are installed.
* Automated tests are executed with pytest.
* If tests fail, the pipeline stops before deployment.
* A Docker image is built only after successful testing.
* The container is deployed automatically.

This provides a **fail-fast CI/CD workflow**, preventing code that fails the automated test stage from continuing to the deployment stage.

---

## 🛠️ Technology Stack

| Technology                | Purpose                            |
| ------------------------- | ---------------------------------- |
| **GitHub**                | Source control and webhook trigger |
| **Jenkins**               | CI/CD automation                   |
| **Docker**                | Application containerization       |
| **Python**                | Application development            |
| **pytest**                | Automated testing                  |
| **Google Cloud Platform** | Jenkins server / cloud environment |
| **Jenkinsfile**           | Pipeline as code                   |

---

## 📂 Project Structure

```text
jenkins-docker-pipeline/
│
├── app.py              # Main Python application
├── test_app.py         # Automated tests using pytest
├── Dockerfile          # Docker image build instructions
├── Jenkinsfile         # Jenkins CI/CD pipeline definition
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

# 🔄 CI/CD Pipeline

The Jenkins pipeline consists of five stages.

### Stage 1 — Checkout

Jenkins retrieves the latest source code from the GitHub repository.

```text
GitHub → Jenkins
```

### Stage 2 — Install

Required Python dependencies are installed from:

```text
requirements.txt
```

### Stage 3 — Test

Automated tests are executed using:

```bash
pytest
```

If a test fails, Jenkins stops the pipeline.

This means the Docker build and deployment stages are not executed for code that does not pass the test stage.

### Stage 4 — Build

After successful testing, Jenkins builds the Docker image using the project's `Dockerfile`.

```bash
docker build
```

### Stage 5 — Deploy

The newly built image is used to run the application container.

The deployment process replaces the previous container with the new version.

---

# ☁️ Deploying Jenkins on Google Cloud

This project uses a Google Cloud VM as the Jenkins environment.

The following example uses:

```text
Region: asia-south1
Zone: asia-south1-a
Machine type: e2-medium
OS: Ubuntu 22.04 LTS
```

> **Cost warning:** Running cloud resources can incur charges. Delete resources when they are no longer required.

---

## 1. Create a GCP VM

Make sure the Google Cloud CLI is authenticated and configured for the correct project.

Create the Jenkins VM:

```bash
gcloud compute instances create jenkins-server \
  --zone=asia-south1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=jenkins-server
```

Create a firewall rule for Jenkins:

```bash
gcloud compute firewall-rules create allow-jenkins \
  --allow=tcp:8080 \
  --target-tags=jenkins-server
```

> For a real production deployment, exposing Jenkins directly on port 8080 should be replaced with a more secure architecture, such as HTTPS behind a reverse proxy or load balancer, appropriate firewall restrictions, and proper authentication.

---

# 2. Connect to the VM

```bash
gcloud compute ssh jenkins-server \
  --zone=asia-south1-a
```

---

# 3. Install Java and Jenkins

Inside the VM:

```bash
sudo apt update
sudo apt install -y default-jdk
```

Add the Jenkins package repository:

```bash
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key \
  | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
```

```bash
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list
```

Install Jenkins:

```bash
sudo apt update
sudo apt install -y jenkins
```

Start and enable Jenkins:

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

---

# 4. Install Docker

```bash
sudo apt install -y docker.io
```

Allow Jenkins to access Docker:

```bash
sudo usermod -aG docker jenkins
```

Restart Jenkins:

```bash
sudo systemctl restart jenkins
```

---

# 5. Open Jenkins

Find the external IP address of the VM and open:

```text
http://YOUR-VM-IP:8080
```

Retrieve the initial Jenkins administrator password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Then:

1. Open Jenkins in your browser.
2. Enter the initial administrator password.
3. Install the suggested plugins.
4. Create the Jenkins administrator account.
5. Complete the Jenkins setup.

---

# 🔗 6. Connect Jenkins to GitHub

Create a Jenkins Pipeline job.

```text
Jenkins Dashboard
       ↓
New Item
       ↓
Pipeline
```

Example job name:

```text
leo-pipeline
```

Select:

```text
Pipeline script from SCM
```

Configure:

```text
SCM: Git
Repository URL:
https://github.com/LeoHachiman/Jenkins-CI-CD-Pipeline-with-Docker.git

Branch:
*/main

Script Path:
Jenkinsfile
```

Save the configuration.

---

# 🔔 GitHub Webhook

The project is designed around a GitHub-to-Jenkins webhook workflow.

The intended flow is:

```text
Developer
    │
    │ git push
    ▼
 GitHub
    │
    │ webhook
    ▼
 Jenkins
    │
    ▼
 Jenkinsfile
    │
    ▼
 CI/CD Pipeline
```

Configure the appropriate GitHub webhook in the repository and the corresponding GitHub trigger in Jenkins.

For a Jenkins server hosted on a private network, additional networking or a publicly reachable webhook endpoint will be required.

---

# 🧪 Testing

Run the project's automated tests locally with:

```bash
pytest
```

A successful test run allows the pipeline to continue to the Docker build and deployment stages.

A failed test stops the pipeline before deployment.

This demonstrates the **fail-fast principle** in CI/CD.

---

# 🐳 Docker

The application is containerized using the project's `Dockerfile`.

Build the image:

```bash
docker build -t jenkins-cicd-demo .
```

Run the container:

```bash
docker run --rm jenkins-cicd-demo
```

If the application exposes a network port, publish the required port according to the application's configuration.

---

# 🔐 Security Considerations

This project is intended primarily as a learning and reference implementation.

Do **not** commit the following to GitHub:

* Cloud credentials
* AWS access keys
* GCP service-account keys
* Jenkins passwords
* API tokens
* SSH private keys
* Database credentials
* Other sensitive secrets

Use appropriate secret-management mechanisms such as Jenkins Credentials, GitHub Secrets, or cloud-provider secret-management services.

The example firewall configuration exposes Jenkins on TCP port `8080`. For production use, Jenkins should be protected with an appropriate network and HTTPS architecture rather than being unnecessarily exposed to the public internet.

---

# 🧹 Clean Up GCP Resources

Cloud resources can generate charges even when they are not actively being used.

Delete the Jenkins VM when you no longer need it:

```bash
gcloud compute instances delete jenkins-server \
  --zone=asia-south1-a
```

If you created the firewall rule specifically for this project and no longer need it:

```bash
gcloud compute firewall-rules delete allow-jenkins
```

Always verify the resources in your GCP project before cleanup.

---

# 🎯 Key DevOps Concepts Demonstrated

### Continuous Integration

Code changes are automatically retrieved and tested through Jenkins.

### Continuous Deployment

Successful builds continue to the container deployment stage.

### Fail-Fast Pipeline

Testing occurs before Docker build and deployment.

```text
Test Failure
     ↓
Pipeline Stops
     ↓
No Build
     ↓
No Deployment
```

### Containerization

Docker packages the application and its runtime environment into a container.

### Pipeline as Code

The Jenkins pipeline is defined in a version-controlled `Jenkinsfile` alongside the application.

### Git-Based Workflow

GitHub acts as the source-code repository and webhook trigger for the CI/CD workflow.

### Cloud Infrastructure

Jenkins is hosted on a Google Cloud VM, providing hands-on experience with cloud compute, networking, Linux administration, and deployment automation.

---

# 📚 Learning Objectives

This project was built to develop practical understanding of:

* CI/CD concepts
* Jenkins
* Jenkins Pipeline
* GitHub webhooks
* Docker
* Python application testing
* pytest
* Linux administration
* Google Cloud Compute Engine
* Cloud networking and firewall rules
* Pipeline automation
* Container deployment
* Infrastructure and deployment troubleshooting

---

# 🗺️ Roadmap

The project can be extended with additional DevOps and cloud engineering capabilities.

### Planned improvements

* [ ] Add linting to the CI pipeline
* [ ] Add dependency vulnerability scanning
* [ ] Add Docker image security scanning
* [ ] Add container health checks
* [ ] Improve deployment error handling
* [ ] Add staging and production environments
* [ ] Add deployment rollback
* [ ] Add container registry integration
* [ ] Add Infrastructure as Code
* [ ] Add monitoring and observability
* [ ] Add deployment notifications
* [ ] Explore additional cloud deployment options
* [ ] Improve contributor documentation

---

# 🤝 Contributing

Contributions, suggestions, documentation improvements, and bug reports are welcome.

Before contributing:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the tests.
5. Verify that no credentials or secrets are included.
6. Open a pull request describing your changes.

If you find a problem or have an improvement idea, GitHub Issues can be used to discuss it.

---

# 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for details.

---

# 👨‍💻 Author

**Leo Stephen**

Cloud & DevOps Engineer in training, building practical projects around cloud infrastructure, CI/CD, automation, containers, and DevOps.

* GitHub: [LeoHachiman](https://github.com/LeoHachiman)
* LinkedIn: [Leo Stephen](https://linkedin.com/in/leostephen)

---

## ⭐ Why this project?

This repository is part of my hands-on journey into Cloud and DevOps engineering.

Rather than learning CI/CD only through theory, I built this project to understand the complete workflow from:

```text
Code
 ↓
GitHub
 ↓
Webhook
 ↓
Jenkins
 ↓
Automated Testing
 ↓
Docker Build
 ↓
Container Deployment
 ↓
Cloud Infrastructure
```

The project will continue to evolve as I learn and implement additional cloud, DevOps, automation, security, and reliability practices.
