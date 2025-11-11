#!/bin/bash
# Initialize Git repository and prepare for first push

echo "========================================="
echo "Results CTO Agents - Repository Setup"
echo "========================================="
echo ""

# Check if already a git repo
if [ -d .git ]; then
    echo "⚠️  Git repository already initialized"
    echo ""
    read -p "Do you want to reinitialize? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    rm -rf .git
fi

# Initialize git
echo "Initializing Git repository..."
git init
git branch -M main
echo "✓ Git initialized"
echo ""

# Prompt for remote URL
read -p "Enter your GitHub repository URL (leave blank to skip): " REPO_URL
echo ""

if [ ! -z "$REPO_URL" ]; then
    git remote add origin "$REPO_URL"
    echo "✓ Remote added: $REPO_URL"
    echo ""
else
    echo "⚠️  Remote not added. Add later with:"
    echo "   git remote add origin <your-repo-url>"
    echo ""
fi

# Check for .env file
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ .env created (you need to edit this)"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your credentials before proceeding"
    echo ""
fi

# Check for credentials
if [ ! -f credentials.json ]; then
    echo "⚠️  WARNING: credentials.json not found"
    echo "   You need to add your Google service account credentials"
    echo "   Place the file in the root directory as 'credentials.json'"
    echo ""
fi

# Stage files
echo "Staging files for commit..."
git add .
echo "✓ Files staged"
echo ""

# Initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: Results CTO Agents

- Agent 3: Technical Debt Scanner
- Agent 4: Regional News Monitor  
- Google Sheets integration
- GCP deployment automation
- CI/CD with GitHub Actions"
echo "✓ Initial commit created"
echo ""

# Summary
echo "========================================="
echo "✅ Repository Initialized!"
echo "========================================="
echo ""

if [ ! -z "$REPO_URL" ]; then
    echo "Next steps:"
    echo "1. Edit .env with your credentials"
    echo "2. Add credentials.json to root directory"
    echo "3. Run: python3 test_setup.py"
    echo "4. Push to GitHub: git push -u origin main"
else
    echo "Next steps:"
    echo "1. Edit .env with your credentials"
    echo "2. Add credentials.json to root directory"
    echo "3. Add remote: git remote add origin <url>"
    echo "4. Run: python3 test_setup.py"
    echo "5. Push to GitHub: git push -u origin main"
fi

echo ""
echo "For detailed instructions, see QUICKSTART.md"
echo "========================================="
