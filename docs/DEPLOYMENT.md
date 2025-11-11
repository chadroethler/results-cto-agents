# Deployment Guide

Complete guide for deploying Results CTO agents to Google Cloud Platform.

## Prerequisites

- Google Cloud Platform account
- gcloud CLI installed
- Git repository (GitHub/GitLab)
- Service account with credentials
- Google Sheet created and shared with service account

## Setup Steps

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd results-cto-agents
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values
```

Required variables:
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_REGION`: Deployment region (e.g., us-central1)
- `SPREADSHEET_ID`: Your Google Sheets ID
- `REDDIT_CLIENT_ID`: Reddit API client ID
- `REDDIT_CLIENT_SECRET`: Reddit API secret
- `REDDIT_USER_AGENT`: Your app name

### 3. Add Credentials

Place your service account JSON file in the root directory as `credentials.json`.

**Important:** Never commit this file to Git (it's in .gitignore).

### 4. Validate Setup

```bash
python3 test_setup.py
```

This checks:
- Environment variables
- Credentials file
- Configuration files
- Python dependencies
- Google Sheets connection

### 5. Test Locally

```bash
# Test Agent 3
python3 agents/agent_3/agent.py

# Test Agent 4
python3 agents/agent_4/agent.py
```

Check your Google Sheet's "Automation Queue" tab for results.

## Deployment Options

### Option A: Manual Deployment Script

```bash
chmod +x scripts/deploy_gcp.sh
./scripts/deploy_gcp.sh
```

This script:
1. Enables required GCP APIs
2. Deploys both Cloud Functions
3. Sets up Cloud Scheduler jobs
4. Configures daily execution

### Option B: GitHub Actions (Recommended)

#### Setup GitHub Secrets

In your GitHub repository, go to Settings → Secrets and add:

- `GCP_SA_KEY`: Service account JSON (entire file content)
- `GCP_PROJECT_ID`: Your project ID
- `SPREADSHEET_ID`: Your spreadsheet ID
- `REDDIT_CLIENT_ID`: Reddit client ID
- `REDDIT_CLIENT_SECRET`: Reddit secret
- `REDDIT_USER_AGENT`: User agent string

#### Trigger Deployment

Push to main branch:

```bash
git add .
git commit -m "Deploy agents"
git push origin main
```

Or manually trigger from GitHub Actions tab.

## Post-Deployment

### Verify Deployment

```bash
# List deployed functions
gcloud functions list

# View logs
gcloud functions logs read agent-3-tech-debt --limit=50
gcloud functions logs read agent-4-regional-news --limit=50

# Test manually
curl -X POST https://REGION-PROJECT_ID.cloudfunctions.net/agent-3-tech-debt
```

### Monitor Execution

1. **Cloud Console**: 
   - Navigate to Cloud Functions
   - View execution logs and metrics

2. **Cloud Scheduler**:
   - View scheduled job history
   - Check for failed executions

3. **Google Sheets**:
   - Check Automation Queue for new entries
   - Review daily at 10 AM (after both agents run)

## Updating Agents

### Update Code

1. Make changes to agent code
2. Test locally
3. Commit and push to main branch
4. GitHub Actions will automatically deploy

### Update Configuration

Update config files locally, then:

```bash
./scripts/deploy_gcp.sh
```

Config files are deployed with the function code.

### Update Schedule

Modify Cloud Scheduler jobs:

```bash
gcloud scheduler jobs update http agent-3-daily \
  --schedule="0 6 * * *" \
  --time-zone="America/Chicago"
```

## Troubleshooting

### Deployment Fails

**Error: API not enabled**
```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```

**Error: Insufficient permissions**
- Verify service account has required roles:
  - Cloud Functions Developer
  - Cloud Scheduler Admin
  - Service Account User

### Function Fails

**Check logs:**
```bash
gcloud functions logs read agent-3-tech-debt --limit=100
```

**Common issues:**
- Missing environment variables
- Credentials file not included in deployment
- Configuration files not found

### Scheduler Not Working

**Verify scheduler is enabled:**
```bash
gcloud scheduler jobs list
```

**Manually trigger job:**
```bash
gcloud scheduler jobs run agent-3-daily
```

## Cost Management

### Free Tier Limits

- Cloud Functions: 2M invocations/month
- Cloud Scheduler: 3 jobs free
- With 2 agents running daily: **$0/month**

### Monitor Costs

```bash
# View billing
gcloud billing accounts list
gcloud billing projects describe PROJECT_ID
```

## Security Best Practices

1. **Never commit credentials**
   - Use .gitignore
   - Store in Secret Manager (production)

2. **Restrict function access**
   - Use Cloud IAM for production
   - Remove `--allow-unauthenticated` flag

3. **Rotate credentials**
   - Reddit API keys: Every 90 days
   - Service accounts: Every 6 months

4. **Monitor access**
   - Enable Cloud Audit Logs
   - Review access patterns

## Rollback

If deployment fails, rollback to previous version:

```bash
# List versions
gcloud functions list

# Deploy specific version
gcloud functions deploy agent-3-tech-debt \
  --source=gs://GCS_BUCKET/SOURCE_VERSION
```

## Support

- Check logs first: `gcloud functions logs read`
- Review configuration: `python3 test_setup.py`
- Test locally before deploying
- Verify Google Sheets access

For additional help, refer to:
- [Google Cloud Functions docs](https://cloud.google.com/functions/docs)
- [GitHub Actions docs](https://docs.github.com/en/actions)
