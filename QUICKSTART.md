# Quick Start Guide

Get your agents running in 10 minutes.

## 🚀 Step 1: Initialize Repository (1 minute)

```bash
# Create GitHub repository at github.com (don't initialize with README)
# Then run:

cd results-cto-agents-repo
git init
git add .
git commit -m "Initial commit: Results CTO agents"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## ⚙️ Step 2: Configure Environment (3 minutes)

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Minimum required:
```env
SPREADSHEET_ID=your_spreadsheet_id_here
CREDENTIALS_FILE=credentials.json
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=ResultsCTO-Agent/1.0
```

Add your `credentials.json` file to the root directory.

## ✅ Step 3: Validate Setup (1 minute)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 test_setup.py
```

## 🧪 Step 4: Test Locally (2 minutes)

```bash
python3 agents/agent_3/agent.py
python3 agents/agent_4/agent.py
```

Check your Google Sheet for results!

## ☁️ Step 5: Deploy to GCP (3 minutes)

### Option A: Manual Deployment

```bash
chmod +x scripts/deploy_gcp.sh
./scripts/deploy_gcp.sh
```

### Option B: GitHub Actions (Recommended)

1. Go to GitHub repo → Settings → Secrets
2. Add these secrets:
   - `GCP_SA_KEY` (entire credentials.json content)
   - `GCP_PROJECT_ID`
   - `SPREADSHEET_ID`
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USER_AGENT`

3. Push to trigger deployment:
```bash
git push origin main
```

## ✨ Done!

Your agents are now running daily:
- Agent 3: 8 AM CST (Technical Debt Scanner)
- Agent 4: 9 AM CST (Regional News Monitor)

## 📊 Daily Workflow

1. Open Google Sheets at 10 AM
2. Go to "Automation Queue" tab
3. Review "Pending Review" entries (5-10 minutes)
4. Update Status to "Approved" or "Rejected"
5. Research approved companies
6. Add to pipeline

## 🔧 Common Commands

```bash
# View logs
gcloud functions logs read agent-3-tech-debt --limit=50

# Test function manually
curl -X POST https://REGION-PROJECT.cloudfunctions.net/agent-3-tech-debt

# Update configuration
./scripts/deploy_gcp.sh

# Run tests
pytest tests/ -v
```

## 📚 Next Steps

- Read [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment guide
- Read [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) for architecture details
- Customize keywords in `config/agent_X_keywords.json`
- Add more RSS feeds in `config/agent_X_sources.json`

## 🆘 Need Help?

1. Run `python3 test_setup.py` to diagnose issues
2. Check logs: `gcloud functions logs read FUNCTION_NAME`
3. Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) troubleshooting section

---

**That's it! You now have an automated lead generation system running at $0/month.** 🎉
