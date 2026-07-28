# Q3 – CI/CD Pipeline on Ghaymah Cloud

## Overview

This task implements a complete CI/CD pipeline using **GitHub Actions** and **Ghaymah Cloud**.

The pipeline automatically builds the application, performs a smoke test, deploys to the **staging** environment for development changes, and deploys to the **production** environment after merging into the `main` branch with **manual approval** enabled.

---

# Pipeline Workflow

```text
Developer
    │
    │ Push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Build Docker Image
    ├── Smoke Test (/health)
    │
    ├──────────────┐
    │              │
    ▼              ▼
develop         main
    │              │
Deploy          Manual Approval
Staging             │
                    ▼
             Deploy Production
```

---

# CI Pipeline

The Continuous Integration stage performs:

- Checkout repository
- Build Docker image
- Start container
- Execute smoke test
- Verify `/health` endpoint
- Stop and remove the test container

This ensures that only healthy builds continue to deployment.

---

# CD Pipeline

## Staging Deployment

Triggered automatically when code is pushed to the **develop** branch.

Steps:

1. Install Ghaymah CLI
2. Authenticate using GitHub Secrets
3. Load `.ghaymah.staging.json`
4. Deploy application to the staging environment

Purpose:

- Integration testing
- Validation before production
- Detect deployment issues early

---

## Production Deployment

Triggered after merging into the **main** branch.

Deployment requires **manual approval** through the GitHub Environment protection rules before execution.

Steps:

1. Install Ghaymah CLI
2. Authenticate using GitHub Secrets
3. Load `.ghaymah.production.json`
4. Deploy application to the production environment

Purpose:

- Stable release
- Manual verification before deployment
- Reduce production risks

---

# Pipeline Evidence

The following screenshots demonstrate successful execution of the CI/CD pipeline and deployment for both **Staging** and **Production** environments.

## Staging Pipeline

![Staging Pipeline](images/staging-pipeline-success.jpg)

---

## Production Pipeline

![Production Pipeline](images/production-pipeline-success.jpg)

---

## Deployment Verification

The following screenshot confirms that both **Staging** and **Production** applications were successfully deployed on **Ghaymah Cloud**.

![Deployment Verification](images/production-and-staging-deployment.jpg)

---

# Staging vs Production

| Staging | Production |
|----------|------------|
| Testing environment | Live environment |
| Used by developers | Used by end users |
| Automatic deployment | Protected deployment |
| Safe for validation | High availability |
| Can be updated frequently | Only verified releases |

---

# Manual Approval

Production deployments are protected using **GitHub Environments**.

The workflow pauses before deploying to production until manual approval is granted.

Benefits:

- Prevent accidental deployments
- Final verification before release
- Safer production deployments

---

# Ghaymah CLI Integration

Deployment is performed using the official **Ghaymah CLI**.

Installation:

```bash
curl -sSL https://cli.ghaymah.systems/install.sh | bash
```

Authentication:

```bash
gy auth login \
  --email "<EMAIL>" \
  --password "<PASSWORD>"
```

Deployment:

```bash
cp .ghaymah.production.json .ghaymah.json
gy resource app launch
```

For the staging environment, the workflow uses:

```bash
cp .ghaymah.staging.json .ghaymah.json
```

before deployment.

---

# GitHub Secrets

Sensitive credentials are stored securely as GitHub Secrets.

Secrets used:

- GHAYMAH_EMAIL
- GHAYMAH_PW

No credentials are stored inside the repository.

---

# Technologies Used

- GitHub Actions
- Docker
- Ghaymah Cloud
- Ghaymah CLI
- GitHub Environments
- GitHub Secrets

---

# Result

The pipeline successfully provides:

- Automated Docker image build
- Automated smoke testing
- Automatic deployment to the Staging environment
- Manual approval before Production deployment
- Secure deployment using GitHub Secrets
- Production deployment using Ghaymah CLI

This implementation demonstrates a complete production-ready CI/CD workflow following modern DevOps and SRE best practices.
