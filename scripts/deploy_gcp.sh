#!/bin/bash
# Deploy agents to Google Cloud Platform

set -e  # Exit on error

echo "========================================="
echo "Results CTO Agents - GCP Deployment"
echo "========================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Check required variables
if [ -z "$GCP_PROJECT_ID" ] || [ -z "$GCP_REGION" ]; then
    echo "Error: GCP_PROJECT_ID and GCP_REGION must be set in .env"
    exit 1
fi

echo "Project ID: $GCP_PROJECT_ID"
echo "Region: $GCP_REGION"
echo ""

# Set project
gcloud config set project $GCP_PROJECT_ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable sheets.googleapis.com
echo "✓ APIs enabled"
echo ""

# Deploy Agent 3
echo "Deploying Agent 3: Technical Debt Scanner..."
gcloud functions deploy agent-3-tech-debt \
    --gen2 \
    --runtime=python311 \
    --region=$GCP_REGION \
    --source=. \
    --entry-point=agent_3_handler \
    --trigger-http \
    --allow-unauthenticated \
    --timeout=540s \
    --memory=512MB \
    --set-env-vars="SPREADSHEET_ID=$SPREADSHEET_ID,AGENT_3_ENABLED=$AGENT_3_ENABLED,LOG_LEVEL=$LOG_LEVEL,ENVIRONMENT=production"

echo "✓ Agent 3 deployed"
echo ""

# Deploy Agent 4
echo "Deploying Agent 4: Regional News Monitor..."
gcloud functions deploy agent-4-regional-news \
    --gen2 \
    --runtime=python311 \
    --region=$GCP_REGION \
    --source=. \
    --entry-point=agent_4_handler \
    --trigger-http \
    --allow-unauthenticated \
    --timeout=540s \
    --memory=512MB \
    --set-env-vars="SPREADSHEET_ID=$SPREADSHEET_ID,REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID,REDDIT_CLIENT_SECRET=$REDDIT_CLIENT_SECRET,REDDIT_USER_AGENT=$REDDIT_USER_AGENT,AGENT_4_ENABLED=$AGENT_4_ENABLED,LOG_LEVEL=$LOG_LEVEL,ENVIRONMENT=production"

echo "✓ Agent 4 deployed"
echo ""

# Setup Cloud Scheduler jobs
echo "Setting up Cloud Scheduler..."

# Agent 3 - Daily at 8 AM
gcloud scheduler jobs create http agent-3-daily \
    --location=$GCP_REGION \
    --schedule="0 8 * * *" \
    --uri="https://$GCP_REGION-$GCP_PROJECT_ID.cloudfunctions.net/agent-3-tech-debt" \
    --http-method=POST \
    --time-zone="America/Chicago" \
    --attempt-deadline=600s \
    --message-body='{"trigger":"scheduled"}' \
    || echo "Job agent-3-daily already exists, updating..."

# Agent 4 - Daily at 9 AM
gcloud scheduler jobs create http agent-4-daily \
    --location=$GCP_REGION \
    --schedule="0 9 * * *" \
    --uri="https://$GCP_REGION-$GCP_PROJECT_ID.cloudfunctions.net/agent-4-regional-news" \
    --http-method=POST \
    --time-zone="America/Chicago" \
    --attempt-deadline=600s \
    --message-body='{"trigger":"scheduled"}' \
    || echo "Job agent-4-daily already exists, updating..."

echo "✓ Cloud Scheduler configured"
echo ""

echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Agent 3 URL: https://$GCP_REGION-$GCP_PROJECT_ID.cloudfunctions.net/agent-3-tech-debt"
echo "Agent 4 URL: https://$GCP_REGION-$GCP_PROJECT_ID.cloudfunctions.net/agent-4-regional-news"
echo ""
echo "Scheduled jobs:"
echo "  - Agent 3: Daily at 8 AM CST"
echo "  - Agent 4: Daily at 9 AM CST"
echo ""
echo "View logs: gcloud functions logs read --limit=50"
echo "Test manually:"
echo "  curl -X POST https://$GCP_REGION-$GCP_PROJECT_ID.cloudfunctions.net/agent-3-tech-debt"
