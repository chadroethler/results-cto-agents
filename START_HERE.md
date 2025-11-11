# 🚀 START HERE

Welcome to your Results CTO Lead Generation Agents repository!

## What You Have

A complete, production-ready system with:

✅ **2 Automated Agents**
- Agent 3: Technical Debt Scanner (RSS feeds)
- Agent 4: Regional News Monitor (Reddit API)

✅ **Google Sheets Integration**
- Automatic data collection
- Daily signal detection
- Review workflow

✅ **Deployment Automation**
- One-command GCP deployment
- GitHub Actions CI/CD
- Cloud Scheduler for daily runs

✅ **Complete Documentation**
- Build guide
- Deployment guide
- API documentation

## 📂 Repository Structure

```
results-cto-agents/
├── agents/              # Agent code
│   ├── agent_3/        # Technical Debt Scanner
│   ├── agent_4/        # Regional News Monitor
│   └── shared/         # Shared utilities
├── config/             # Configuration files
├── scripts/            # Deployment scripts
├── tests/              # Unit tests
├── docs/               # Documentation
└── .github/workflows/  # CI/CD automation
```

## ⚡ Quick Start (10 Minutes)

### 1. Initialize Git (30 seconds)

```bash
cd results-cto-agents-repo
./scripts/init_repo.sh
```

This will:
- Initialize Git repository
- Prompt for your GitHub URL
- Create initial commit
- Set up .env file

### 2. Configure Credentials (2 minutes)

Edit `.env` file:
```bash
nano .env
```

Add:
```env
SPREADSHEET_ID=your_google_sheet_id
CREDENTIALS_FILE=credentials.json
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=ResultsCTO-Agent/1.0
GCP_PROJECT_ID=your-gcp-project
GCP_REGION=us-central1
```

Place your Google service account JSON in root as `credentials.json`

### 3. Validate Setup (1 minute)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 test_setup.py
```

### 4. Test Locally (2 minutes)

```bash
python3 agents/agent_3/agent.py
python3 agents/agent_4/agent.py
```

Check your Google Sheet!

### 5. Push to GitHub (1 minute)

```bash
git push -u origin main
```

### 6. Deploy to GCP (3 minutes)

**Option A - Manual:**
```bash
./scripts/deploy_gcp.sh
```

**Option B - GitHub Actions:**
1. Add secrets in GitHub repo settings
2. Push triggers automatic deployment

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | 10-minute setup guide |
| **[docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md)** | Complete technical guide |
| **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** | Deployment instructions |
| **[README.md](README.md)** | Project overview |

## 🔑 Required Accounts (All Free)

1. **Google Cloud Platform**
   - Free tier: $300 credit + always-free tier
   - Needed for: Cloud Functions, Sheets API

2. **Google Sheet**
   - Free with any Google account
   - Create "Automation Queue" tab

3. **Reddit API**
   - Free at reddit.com/prefs/apps
   - Needed for Agent 4

4. **GitHub** (optional but recommended)
   - Free for public/private repos
   - Enables automatic deployment

## 💰 Cost

**Current setup: $0/month**

The free tier covers:
- 2 Cloud Functions (2M invocations/month free)
- Cloud Scheduler (3 jobs free)
- Google Sheets API (100 requests/100 seconds)
- Reddit API (60 requests/minute)

## 🛠️ Customization

Want to adjust what the agents find?

Edit configuration files:
```bash
nano config/agent_3_keywords.json  # Change technical keywords
nano config/agent_4_keywords.json  # Change business signals
nano config/agent_3_sources.json   # Add/remove RSS feeds
nano config/agent_4_sources.json   # Add/remove subreddits
```

## 📊 Daily Workflow

1. **10 AM** - Check Google Sheets "Automation Queue"
2. **Review** - Scan "Pending Review" entries (5-10 mins)
3. **Approve/Reject** - Update status column
4. **Research** - Investigate approved companies
5. **Add to Pipeline** - Move to prospect list

## 🆘 Troubleshooting

**Setup issues:**
```bash
python3 test_setup.py  # Diagnoses problems
```

**Deployment issues:**
```bash
gcloud functions logs read agent-3-tech-debt --limit=50
```

**Code issues:**
```bash
pytest tests/ -v  # Run unit tests
```

## 🎯 Success Metrics

After 1 week, you should see:
- 20-50 signals detected
- 30%+ approval rate
- <10 minutes/day review time

## 📈 Next Steps

**Week 1:**
- ✅ Deploy and validate
- ✅ Tune keywords based on results
- ✅ Adjust false positive rate

**Week 2-4:**
- Subscribe to Apollo.io ($49/month)
- Deploy additional agents
- Scale to full system

**Month 3:**
- Consider HubSpot migration
- Add paid enrichment services
- Expand to 12-agent system

## 💡 Pro Tips

1. **Start simple** - Run free agents for 1 week before adding complexity
2. **Tune keywords** - Adjust based on false positive rate
3. **Review daily** - 10 minutes keeps pipeline full
4. **Use GitHub Actions** - Automatic deployment saves time
5. **Monitor logs** - Catch issues early

## 🤔 Questions?

1. Check **[QUICKSTART.md](QUICKSTART.md)** first
2. Review **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** troubleshooting
3. Run `python3 test_setup.py` to diagnose
4. Check logs: `gcloud functions logs read`

---

## ✨ Ready to Start?

```bash
./scripts/init_repo.sh
```

Then follow the prompts! 🚀

---

**Built for Results CTO** | Production-Ready | Zero Monthly Cost
