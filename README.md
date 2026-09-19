# Jenkins CI/CD Pipeline with Docker

**Leo Stephen — Cloud & DevOps Portfolio Project**

## What This Project Does

Every time code is pushed to this repository, Jenkins automatically:
1. Pulls the latest code from GitHub
2. Installs dependencies
3. Runs automated tests (if tests fail — deployment stops here)
4. Builds a Docker image
5. Deploys the container

Zero manual steps. Zero human intervention.

## Tech Stack

| Tool | Purpose |
|---|---|
| Jenkins | CI/CD automation server |
| Docker | Containerisation |
| Python | Application code |
| pytest | Automated testing |
| GitHub | Source code & webhook trigger |

## Project Structure

```
jenkins-docker-pipeline/
├── app.py              # Main Python application
├── test_app.py         # Automated tests (pytest)
├── Dockerfile          # Container build instructions
├── Jenkinsfile         # Pipeline definition (5 stages)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Pipeline Stages

```
GitHub Push → Jenkins Webhook
     ↓
[Stage 1] Checkout     — Pull latest code
     ↓
[Stage 2] Install      — pip install requirements
     ↓
[Stage 3] Test         — pytest (stops here if tests fail)
     ↓
[Stage 4] Build        — docker build
     ↓
[Stage 5] Deploy       — docker run (replaces old container)
```

## How to Set Up Jenkins (GCP)

### 1. Create a GCP VM
```bash
gcloud compute instances create jenkins-server \
  --zone=asia-south1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=jenkins-server

gcloud compute firewall-rules create allow-jenkins \
  --allow=tcp:8080 \
  --target-tags=jenkins-server
```

### 2. SSH into the VM and install Jenkins + Docker
```bash
gcloud compute ssh jenkins-server --zone=asia-south1-a

# Inside the VM:
sudo apt update && sudo apt install -y default-jdk

curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key \
  | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list

sudo apt update && sudo apt install -y jenkins
sudo apt install -y docker.io
sudo usermod -aG docker jenkins
sudo systemctl start jenkins && sudo systemctl enable jenkins
sudo systemctl restart jenkins
```

### 3. Open Jenkins
- Go to `http://YOUR-VM-IP:8080`
- Get the initial password: `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`
- Install suggested plugins → create admin user

### 4. Create the Pipeline Job
- New Item → name: `leo-pipeline` → select **Pipeline** → OK
- Pipeline section → Definition: **Pipeline script from SCM**
- SCM: **Git** → Repository URL: `https://github.com/YOUR-USERNAME/jenkins-docker-pipeline.git`
- Branch: `*/main` → Script Path: `Jenkinsfile` → Save
- Click **Build Now**

### 5. Clean Up (avoid GCP charges)
```bash
gcloud compute instances delete jenkins-server --zone=asia-south1-a
```

## Key Concepts Demonstrated

- **CI/CD**: Continuous Integration — every push is automatically tested and deployed
- **Fail-fast**: If tests fail in Stage 3, Docker build and deployment never happen — broken code never reaches production
- **Containerisation**: Docker ensures the app runs identically on any environment
- **Infrastructure as Code**: Jenkinsfile is version-controlled — the pipeline definition lives alongside the code

## Author
**Leo Stephen** — Aspiring Cloud & DevOps Engineer
leojose715@gmail.com | [LinkedIn](https://linkedin.com/in/leostephen)
