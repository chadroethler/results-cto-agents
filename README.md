# Results CTO Lead Generation Agents

Automated lead generation system using RSS feeds and Reddit API to identify potential clients.

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd results-cto-agents
cp .env.example .env
# Edit .env with your credentials
```

### 2. Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 test_setup.py
```

### 3. Deploy to Google Cloud
```bash
./scripts/deploy_gcp.sh
```

## 📁 Project Structure

```
results-cto-agents/
├── agents/
│   ├── agent_3/          # Technical Debt Scanner
│   ├── agent_4/          # Regional News Monitor
│   └── shared/           # Shared utilities
├── config/               # Configuration files
├── scripts/              # Deployment scripts
├── .github/workflows/    # CI/CD automation
├── tests/                # Unit tests
└── docs/                 # Documentation
```

## 🔧 Configuration

See `.env.example` for required environment variables.

## 📚 Documentation

- [Complete Build Guide](docs/BUILD_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Documentation](docs/API.md)

## 📊 Monitoring

View logs in Google Cloud Console or locally:
```bash
tail -f logs/agent_3.log
tail -f logs/agent_4.log
```

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Submit PR

## 📄 License

Private - Results CTO Internal Use Only
