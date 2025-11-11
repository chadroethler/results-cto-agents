# Complete Build Guide: Agents 3 & 4
## Free RSS-Based Lead Generation System

**Total Cost: $0/month** | **Setup Time: 2-3 hours** | **Maintenance: 15 minutes/week**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Architecture](#system-architecture)
3. [Environment Setup](#environment-setup)
4. [Agent 3: Technical Debt Scanner](#agent-3-technical-debt-scanner)
5. [Agent 4: Regional News Monitor](#agent-4-regional-news-monitor)
6. [Google Sheets Integration](#google-sheets-integration)
7. [Deployment](#deployment)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Skills
- Basic Python knowledge
- Familiarity with command line
- Basic understanding of APIs

### Required Accounts (All Free)
- ✅ Google Cloud Platform account (free tier)
- ✅ Reddit account (for API access)
- ✅ Google account (for Sheets API)

### System Requirements
- Python 3.9 or higher
- 1GB disk space
- Internet connection

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│              RSS FEEDS & REDDIT API                  │
│  (TechCrunch, GitHub, Hacker News, r/programming)   │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              AGENT 3 & AGENT 4                       │
│         (Python Scripts on GCP/Local)                │
│  • Parse feeds                                       │
│  • Filter by keywords                                │
│  • Extract signals                                   │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            GOOGLE SHEETS CRM                         │
│         "Automation Queue" Tab                       │
│  • Pending Review entries                            │
│  • Daily human review (5-10 mins)                    │
└─────────────────────────────────────────────────────┘
```

---

## Environment Setup

### Step 1: Create Project Directory

```bash
mkdir -p ~/results-cto-agents
cd ~/results-cto-agents
mkdir -p agent_3_tech_debt agent_4_regional_news logs config
```

### Step 2: Install Python Dependencies

Create `requirements.txt`:

```txt
# requirements.txt
google-api-python-client==2.108.0
google-auth-httplib2==0.1.1
google-auth-oauthlib==1.1.0
feedparser==6.0.10
praw==7.7.1
python-dotenv==1.0.0
requests==2.31.0
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

### Step 3: Google Sheets API Setup

#### 3.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project"
3. Name it: "Results-CTO-Agents"
4. Click "Create"

#### 3.2 Enable Google Sheets API

1. In Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click "Enable"

#### 3.3 Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: "agent-service-account"
4. Click "Create and Continue"
5. Role: "Editor"
6. Click "Done"

#### 3.4 Download Credentials

1. Click on the service account email
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose "JSON"
5. Save as `credentials.json` in your project root

#### 3.5 Share Google Sheet with Service Account

1. Open the service account JSON file
2. Copy the "client_email" value (looks like: `agent-service-account@project-id.iam.gserviceaccount.com`)
3. Open your Google Sheet
4. Click "Share"
5. Paste the service account email
6. Give "Editor" permissions
7. Click "Send"

### Step 4: Reddit API Setup

#### 4.1 Create Reddit App

1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Scroll down and click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: ResultsCTO-Agent4
   - **App type**: Script
   - **Description**: Lead generation monitor
   - **About URL**: (leave blank)
   - **Redirect URI**: http://localhost:8080
4. Click "Create app"
5. Note your **client_id** (under app name) and **client_secret**

### Step 5: Create Environment File

Create `.env` file in project root:

```bash
# .env
# Google Sheets Configuration
SPREADSHEET_ID=your_spreadsheet_id_here
CREDENTIALS_FILE=credentials.json

# Reddit API Configuration
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=ResultsCTO-Agent4/1.0

# Agent Configuration
AGENT_3_ENABLED=true
AGENT_4_ENABLED=true
LOG_LEVEL=INFO
```

**To find your SPREADSHEET_ID:**
- Open your Google Sheet
- Look at the URL: `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit`
- Copy the `YOUR_SPREADSHEET_ID` part

---

## Agent 3: Technical Debt Scanner

### Purpose
Monitor tech news, GitHub, and forums for companies discussing technical challenges, legacy systems, or modernization needs.

### Configuration Files

#### config/agent_3_sources.json

```json
{
  "rss_feeds": [
    {
      "name": "TechCrunch",
      "url": "https://techcrunch.com/feed/",
      "priority": "high"
    },
    {
      "name": "GitHub Trending",
      "url": "https://github.com/trending.atom",
      "priority": "medium"
    },
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/rss",
      "priority": "high"
    },
    {
      "name": "Dev.to",
      "url": "https://dev.to/feed",
      "priority": "medium"
    },
    {
      "name": "The New Stack",
      "url": "https://thenewstack.io/feed/",
      "priority": "high"
    }
  ],
  "update_frequency_minutes": 60
}
```

#### config/agent_3_keywords.json

```json
{
  "technical_debt_signals": [
    "legacy system",
    "technical debt",
    "refactor",
    "modernization",
    "migration",
    "deprecated",
    "outdated infrastructure",
    "monolith to microservices",
    "code cleanup",
    "tech stack overhaul"
  ],
  "pain_point_signals": [
    "scaling issues",
    "performance problems",
    "downtime",
    "slow deployments",
    "manual processes",
    "difficult to maintain",
    "breaking frequently",
    "hard to test"
  ],
  "solution_seeking": [
    "looking for CTO",
    "hiring technical consultant",
    "need technical leadership",
    "seeking architecture advice",
    "modernization project",
    "digital transformation"
  ],
  "company_size_indicators": [
    "series a",
    "series b",
    "startup",
    "growing team",
    "scaling",
    "raised funding"
  ]
}
```

### Agent 3 Main Script

#### agent_3_tech_debt/agent_3.py

```python
#!/usr/bin/env python3
"""
Agent 3: Technical Debt Scanner
Monitors RSS feeds for technical debt signals and companies seeking help
"""

import os
import sys
import json
import logging
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Add parent directory to path for shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.sheets_client import SheetsClient
from shared.utils import load_json_config, setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging('agent_3', os.getenv('LOG_LEVEL', 'INFO'))


class TechnicalDebtScanner:
    """Scans RSS feeds for technical debt signals"""
    
    def __init__(self):
        self.sheets_client = SheetsClient(
            credentials_file=os.getenv('CREDENTIALS_FILE'),
            spreadsheet_id=os.getenv('SPREADSHEET_ID')
        )
        
        # Load configuration
        self.sources = load_json_config('config/agent_3_sources.json')
        self.keywords = load_json_config('config/agent_3_keywords.json')
        
        # Combine all keyword categories
        self.all_keywords = []
        for category in self.keywords.values():
            self.all_keywords.extend([kw.lower() for kw in category])
        
        logger.info(f"Initialized with {len(self.sources['rss_feeds'])} feeds")
        logger.info(f"Monitoring {len(self.all_keywords)} keywords")
    
    def fetch_feed(self, feed_config: Dict) -> List[Dict]:
        """Fetch and parse an RSS feed"""
        try:
            logger.info(f"Fetching feed: {feed_config['name']}")
            feed = feedparser.parse(feed_config['url'])
            
            if feed.bozo:  # Feed parsing error
                logger.warning(f"Feed parsing error for {feed_config['name']}: {feed.bozo_exception}")
                return []
            
            entries = []
            for entry in feed.entries[:20]:  # Limit to last 20 entries
                entries.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': feed_config['name']
                })
            
            logger.info(f"Retrieved {len(entries)} entries from {feed_config['name']}")
            return entries
            
        except Exception as e:
            logger.error(f"Error fetching feed {feed_config['name']}: {e}")
            return []
    
    def check_keywords(self, text: str) -> List[str]:
        """Check if text contains any keywords"""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.all_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def extract_company_name(self, text: str) -> Optional[str]:
        """
        Attempt to extract company name from text
        This is a simple implementation - can be enhanced with NLP
        """
        # Common patterns: "Company X announced...", "At Company Y, we..."
        patterns = [
            " at ", " for ", " with ", " announced ", 
            " launched ", " raised ", " founded "
        ]
        
        # This is a placeholder - in production, use NER or GPT-4
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in patterns and i + 1 < len(words):
                potential_company = words[i + 1].strip('.,;:')
                if potential_company[0].isupper() and len(potential_company) > 2:
                    return potential_company
        
        return None
    
    def analyze_entry(self, entry: Dict) -> Optional[Dict]:
        """Analyze a feed entry for relevant signals"""
        full_text = f"{entry['title']} {entry['summary']}"
        
        # Check for keywords
        found_keywords = self.check_keywords(full_text)
        
        if not found_keywords:
            return None
        
        # Try to extract company name
        company_name = self.extract_company_name(full_text)
        
        # Calculate relevance score (simple heuristic)
        relevance_score = min(len(found_keywords) * 2, 10)
        
        return {
            'company_name': company_name or 'Unknown',
            'signal_type': 'Technical Debt',
            'signal_description': ', '.join(found_keywords[:3]),  # Top 3 keywords
            'source_url': entry['link'],
            'source': entry['source'],
            'detected_date': datetime.now().strftime('%Y-%m-%d'),
            'relevance_score': relevance_score,
            'title': entry['title'],
            'summary': entry['summary'][:500]  # Truncate long summaries
        }
    
    def process_feeds(self) -> List[Dict]:
        """Process all configured feeds"""
        all_signals = []
        
        for feed_config in self.sources['rss_feeds']:
            entries = self.fetch_feed(feed_config)
            
            for entry in entries:
                signal = self.analyze_entry(entry)
                if signal:
                    all_signals.append(signal)
                    logger.info(f"Found signal: {signal['title'][:50]}... (score: {signal['relevance_score']})")
        
        return all_signals
    
    def write_to_sheets(self, signals: List[Dict]):
        """Write signals to Google Sheets"""
        if not signals:
            logger.info("No signals to write")
            return
        
        logger.info(f"Writing {len(signals)} signals to Google Sheets")
        
        # Prepare rows for Automation Queue tab
        rows = []
        for signal in signals:
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
                signal['company_name'],
                signal['signal_type'],
                signal['signal_description'],
                signal['source_url'],
                signal['detected_date'],
                'Agent 3',
                'Pending Review',
                '',  # Notes (empty)
                signal['relevance_score']
            ]
            rows.append(row)
        
        try:
            self.sheets_client.append_rows('Automation Queue', rows)
            logger.info(f"Successfully wrote {len(rows)} rows to Automation Queue")
        except Exception as e:
            logger.error(f"Error writing to sheets: {e}")
    
    def run(self):
        """Main execution method"""
        logger.info("=" * 60)
        logger.info("Agent 3: Technical Debt Scanner - Starting")
        logger.info("=" * 60)
        
        # Process feeds
        signals = self.process_feeds()
        
        logger.info(f"Total signals found: {len(signals)}")
        
        # Write to Google Sheets
        self.write_to_sheets(signals)
        
        logger.info("Agent 3: Technical Debt Scanner - Complete")
        logger.info("=" * 60)


def main():
    """Entry point"""
    if not os.getenv('AGENT_3_ENABLED', 'true').lower() == 'true':
        logger.info("Agent 3 is disabled")
        return
    
    try:
        scanner = TechnicalDebtScanner()
        scanner.run()
    except Exception as e:
        logger.error(f"Fatal error in Agent 3: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

## Agent 4: Regional News Monitor

### Purpose
Monitor Reddit and regional news for companies announcing expansion, funding, or hiring in your target markets.

### Configuration Files

#### config/agent_4_sources.json

```json
{
  "subreddits": [
    "programming",
    "webdev",
    "SaaS",
    "startups",
    "entrepreneur",
    "technology",
    "softwaredevelopment"
  ],
  "regional_focus": [
    "midwest",
    "iowa",
    "chicago",
    "minneapolis",
    "kansas city",
    "st louis",
    "omaha",
    "des moines"
  ],
  "check_frequency_hours": 4
}
```

#### config/agent_4_keywords.json

```json
{
  "expansion_signals": [
    "opening new office",
    "expanding to",
    "new location",
    "regional expansion",
    "opening headquarters",
    "new branch"
  ],
  "funding_signals": [
    "raised funding",
    "series a",
    "series b",
    "seed round",
    "venture capital",
    "funding round",
    "investment"
  ],
  "hiring_signals": [
    "hiring",
    "looking for",
    "seeking",
    "join our team",
    "we're growing",
    "positions open",
    "careers",
    "cto",
    "vp engineering",
    "head of product"
  ],
  "growth_signals": [
    "fastest growing",
    "doubled revenue",
    "scaling",
    "rapid growth",
    "expanding team",
    "inc 5000"
  ]
}
```

### Agent 4 Main Script

#### agent_4_regional_news/agent_4.py

```python
#!/usr/bin/env python3
"""
Agent 4: Regional News Monitor
Monitors Reddit and regional sources for expansion, funding, and hiring signals
"""

import os
import sys
import json
import logging
import praw
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.sheets_client import SheetsClient
from shared.utils import load_json_config, setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging('agent_4', os.getenv('LOG_LEVEL', 'INFO'))


class RegionalNewsMonitor:
    """Monitors Reddit for regional business signals"""
    
    def __init__(self):
        self.sheets_client = SheetsClient(
            credentials_file=os.getenv('CREDENTIALS_FILE'),
            spreadsheet_id=os.getenv('SPREADSHEET_ID')
        )
        
        # Load configuration
        self.sources = load_json_config('config/agent_4_sources.json')
        self.keywords = load_json_config('config/agent_4_keywords.json')
        
        # Initialize Reddit client
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        # Combine all keywords
        self.all_keywords = []
        for category in self.keywords.values():
            self.all_keywords.extend([kw.lower() for kw in category])
        
        # Add regional keywords
        self.regional_keywords = [r.lower() for r in self.sources['regional_focus']]
        
        logger.info(f"Initialized with {len(self.sources['subreddits'])} subreddits")
        logger.info(f"Monitoring {len(self.all_keywords)} keywords")
        logger.info(f"Regional focus: {', '.join(self.sources['regional_focus'])}")
    
    def check_keywords(self, text: str) -> tuple[List[str], bool]:
        """
        Check if text contains keywords
        Returns: (found_keywords, has_regional_keyword)
        """
        text_lower = text.lower()
        found_keywords = []
        has_regional = False
        
        # Check business signal keywords
        for keyword in self.all_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Check regional keywords
        for region in self.regional_keywords:
            if region in text_lower:
                has_regional = True
                break
        
        return found_keywords, has_regional
    
    def extract_company_name(self, text: str) -> Optional[str]:
        """Extract company name from text"""
        # Look for common patterns
        patterns = [
            "company called",
            "startup called",
            "working at",
            "working for",
            "joined"
        ]
        
        words = text.split()
        for i, word in enumerate(words):
            word_lower = word.lower()
            for pattern in patterns:
                if pattern in ' '.join(words[max(0, i-2):i+1]).lower():
                    if i + 1 < len(words):
                        potential_company = words[i + 1].strip('.,;:')
                        if potential_company[0].isupper():
                            return potential_company
        
        return None
    
    def determine_signal_type(self, keywords: List[str]) -> str:
        """Determine the primary signal type based on keywords"""
        keyword_str = ' '.join(keywords).lower()
        
        if any(x in keyword_str for x in ['funding', 'raised', 'series', 'investment']):
            return 'Funding Announcement'
        elif any(x in keyword_str for x in ['hiring', 'seeking', 'positions']):
            return 'Hiring Expansion'
        elif any(x in keyword_str for x in ['opening', 'expanding', 'new office']):
            return 'Geographic Expansion'
        elif any(x in keyword_str for x in ['growing', 'scaling', 'doubled']):
            return 'Growth Signal'
        else:
            return 'Regional Activity'
    
    def analyze_post(self, post) -> Optional[Dict]:
        """Analyze a Reddit post for relevant signals"""
        full_text = f"{post.title} {post.selftext}"
        
        # Check for keywords
        found_keywords, has_regional = self.check_keywords(full_text)
        
        # Must have both business signal AND regional keyword
        if not (found_keywords and has_regional):
            return None
        
        # Try to extract company name
        company_name = self.extract_company_name(full_text)
        
        # Determine signal type
        signal_type = self.determine_signal_type(found_keywords)
        
        # Calculate relevance score
        base_score = len(found_keywords) * 2
        regional_bonus = 2 if has_regional else 0
        upvote_bonus = min(post.score // 10, 3)  # Up to 3 points for popular posts
        relevance_score = min(base_score + regional_bonus + upvote_bonus, 10)
        
        return {
            'company_name': company_name or 'Unknown',
            'signal_type': signal_type,
            'signal_description': ', '.join(found_keywords[:3]),
            'source_url': f"https://reddit.com{post.permalink}",
            'source': f"Reddit r/{post.subreddit.display_name}",
            'detected_date': datetime.now().strftime('%Y-%m-%d'),
            'relevance_score': relevance_score,
            'title': post.title,
            'summary': post.selftext[:500] if post.selftext else post.title
        }
    
    def monitor_subreddit(self, subreddit_name: str) -> List[Dict]:
        """Monitor a single subreddit"""
        signals = []
        
        try:
            logger.info(f"Monitoring r/{subreddit_name}")
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Check posts from last 24 hours
            for post in subreddit.new(limit=50):
                # Check if post is recent (last 24 hours)
                post_time = datetime.fromtimestamp(post.created_utc)
                if datetime.now() - post_time > timedelta(hours=24):
                    continue
                
                signal = self.analyze_post(post)
                if signal:
                    signals.append(signal)
                    logger.info(f"Found signal: {signal['title'][:50]}... (score: {signal['relevance_score']})")
            
        except Exception as e:
            logger.error(f"Error monitoring r/{subreddit_name}: {e}")
        
        return signals
    
    def process_subreddits(self) -> List[Dict]:
        """Process all configured subreddits"""
        all_signals = []
        
        for subreddit_name in self.sources['subreddits']:
            signals = self.monitor_subreddit(subreddit_name)
            all_signals.extend(signals)
        
        return all_signals
    
    def write_to_sheets(self, signals: List[Dict]):
        """Write signals to Google Sheets"""
        if not signals:
            logger.info("No signals to write")
            return
        
        logger.info(f"Writing {len(signals)} signals to Google Sheets")
        
        # Prepare rows for Automation Queue tab
        rows = []
        for signal in signals:
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
                signal['company_name'],
                signal['signal_type'],
                signal['signal_description'],
                signal['source_url'],
                signal['detected_date'],
                'Agent 4',
                'Pending Review',
                '',  # Notes
                signal['relevance_score']
            ]
            rows.append(row)
        
        try:
            self.sheets_client.append_rows('Automation Queue', rows)
            logger.info(f"Successfully wrote {len(rows)} rows to Automation Queue")
        except Exception as e:
            logger.error(f"Error writing to sheets: {e}")
    
    def run(self):
        """Main execution method"""
        logger.info("=" * 60)
        logger.info("Agent 4: Regional News Monitor - Starting")
        logger.info("=" * 60)
        
        # Process subreddits
        signals = self.process_subreddits()
        
        logger.info(f"Total signals found: {len(signals)}")
        
        # Write to Google Sheets
        self.write_to_sheets(signals)
        
        logger.info("Agent 4: Regional News Monitor - Complete")
        logger.info("=" * 60)


def main():
    """Entry point"""
    if not os.getenv('AGENT_4_ENABLED', 'true').lower() == 'true':
        logger.info("Agent 4 is disabled")
        return
    
    try:
        monitor = RegionalNewsMonitor()
        monitor.run()
    except Exception as e:
        logger.error(f"Fatal error in Agent 4: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

## Shared Modules

### shared/sheets_client.py

```python
"""
Google Sheets client for agent interactions
"""

import logging
from typing import List, Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class SheetsClient:
    """Client for interacting with Google Sheets"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        """
        Initialize Sheets client
        
        Args:
            credentials_file: Path to service account JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.spreadsheet_id = spreadsheet_id
        
        # Authenticate
        creds = Credentials.from_service_account_file(
            credentials_file,
            scopes=self.SCOPES
        )
        
        self.service = build('sheets', 'v4', credentials=creds)
        self.sheets = self.service.spreadsheets()
        
        logger.info(f"Initialized Sheets client for spreadsheet: {spreadsheet_id}")
    
    def append_rows(self, sheet_name: str, rows: List[List]):
        """
        Append rows to a sheet
        
        Args:
            sheet_name: Name of the sheet tab
            rows: List of rows to append
        """
        try:
            body = {'values': rows}
            
            result = self.sheets.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:Z",
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Appended {result.get('updates', {}).get('updatedRows', 0)} rows to {sheet_name}")
            return result
            
        except HttpError as error:
            logger.error(f"Error appending to sheet: {error}")
            raise
    
    def read_range(self, range_name: str) -> List[List]:
        """
        Read data from a range
        
        Args:
            range_name: Range in A1 notation (e.g., 'Sheet1!A1:D10')
        
        Returns:
            List of rows
        """
        try:
            result = self.sheets.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            logger.info(f"Read {len(values)} rows from {range_name}")
            return values
            
        except HttpError as error:
            logger.error(f"Error reading from sheet: {error}")
            raise
    
    def update_range(self, range_name: str, values: List[List]):
        """
        Update a range with new values
        
        Args:
            range_name: Range in A1 notation
            values: New values to write
        """
        try:
            body = {'values': values}
            
            result = self.sheets.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(f"Updated {result.get('updatedCells', 0)} cells in {range_name}")
            return result
            
        except HttpError as error:
            logger.error(f"Error updating sheet: {error}")
            raise
    
    def batch_update(self, updates: List[Dict]):
        """
        Perform batch updates
        
        Args:
            updates: List of update requests
        """
        try:
            body = {'requests': updates}
            
            result = self.sheets.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            
            logger.info(f"Completed batch update with {len(updates)} requests")
            return result
            
        except HttpError as error:
            logger.error(f"Error in batch update: {error}")
            raise
```

### shared/utils.py

```python
"""
Utility functions shared across agents
"""

import json
import logging
import os
from typing import Dict, Any


def load_json_config(filepath: str) -> Dict[str, Any]:
    """
    Load JSON configuration file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Parsed JSON data
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {filepath}: {e}")
        raise


def setup_logging(agent_name: str, level: str = 'INFO') -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        agent_name: Name of the agent (for log file)
        level: Logging level
    
    Returns:
        Configured logger
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    file_handler = logging.FileHandler(f'logs/{agent_name}.log')
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup logger
    logger = logging.getLogger(agent_name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def sanitize_text(text: str, max_length: int = 500) -> str:
    """
    Sanitize and truncate text
    
    Args:
        text: Input text
        max_length: Maximum length
    
    Returns:
        Sanitized text
    """
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length] + '...'
    
    return text
```

---

## Google Sheets Integration

### Google Sheets Structure

Your CRM spreadsheet needs an **"Automation Queue"** tab with these columns:

| Column | Header | Description |
|--------|--------|-------------|
| A | Timestamp | When signal was detected |
| B | Company Name | Extracted or "Unknown" |
| C | Signal Type | E.g., "Technical Debt", "Funding" |
| D | Signal Description | Keywords found |
| E | Source URL | Link to original content |
| F | Detected Date | YYYY-MM-DD |
| G | Agent Source | "Agent 3" or "Agent 4" |
| H | Status | "Pending Review" (default) |
| I | Notes | Empty (for your notes) |
| J | Relevance Score | 1-10 |

### Create the Sheet Structure

1. Open your Google Sheet
2. Create a new tab named: `Automation Queue`
3. Add these headers in Row 1:
   ```
   Timestamp | Company Name | Signal Type | Signal Description | Source URL | 
   Detected Date | Agent Source | Status | Notes | Relevance Score
   ```
4. Format Row 1: Bold, background color #1F4E78, text color white
5. Freeze Row 1: View → Freeze → 1 row
6. Set column widths:
   - A: 180px (Timestamp)
   - B: 200px (Company Name)
   - C: 150px (Signal Type)
   - D: 250px (Description)
   - E: 300px (URL)
   - F: 120px (Date)
   - G: 100px (Agent)
   - H: 120px (Status)
   - I: 300px (Notes)
   - J: 100px (Score)

### Test Sheet Connection

Create a test script:

```python
# test_sheets.py
from dotenv import load_dotenv
import os
from shared.sheets_client import SheetsClient

load_dotenv()

client = SheetsClient(
    credentials_file=os.getenv('CREDENTIALS_FILE'),
    spreadsheet_id=os.getenv('SPREADSHEET_ID')
)

# Test write
test_row = [
    '2025-01-01 12:00:00',
    'Test Company',
    'Test Signal',
    'test keywords',
    'https://example.com',
    '2025-01-01',
    'Test Agent',
    'Testing',
    'This is a test',
    10
]

client.append_rows('Automation Queue', [test_row])
print("✅ Test successful! Check your Google Sheet.")
```

Run it:

```bash
python3 test_sheets.py
```

---

## Deployment

### Option 1: Local Cron Job (Simplest)

#### 1.1 Make Scripts Executable

```bash
chmod +x agent_3_tech_debt/agent_3.py
chmod +x agent_4_regional_news/agent_4.py
```

#### 1.2 Test Manual Execution

```bash
# Test Agent 3
python3 agent_3_tech_debt/agent_3.py

# Test Agent 4
python3 agent_4_regional_news/agent_4.py
```

#### 1.3 Setup Cron Jobs

Edit your crontab:

```bash
crontab -e
```

Add these lines (adjust paths to match your system):

```bash
# Agent 3: Daily at 8 AM
0 8 * * * cd /home/yourusername/results-cto-agents && /usr/bin/python3 agent_3_tech_debt/agent_3.py >> logs/agent3_cron.log 2>&1

# Agent 4: Daily at 9 AM
0 9 * * * cd /home/yourusername/results-cto-agents && /usr/bin/python3 agent_4_regional_news/agent_4.py >> logs/agent4_cron.log 2>&1
```

**Cron schedule examples:**
- `0 8 * * *` - Every day at 8 AM
- `0 */6 * * *` - Every 6 hours
- `0 8,14,20 * * *` - 8 AM, 2 PM, and 8 PM
- `0 8 * * 1-5` - Every weekday at 8 AM

#### 1.4 Verify Cron Jobs

```bash
# List your cron jobs
crontab -l

# Check cron logs
tail -f logs/agent3_cron.log
tail -f logs/agent4_cron.log
```

### Option 2: GCP Cloud Functions (Recommended for Production)

#### 2.1 Create requirements.txt for Cloud

```txt
# requirements_cloud.txt
google-api-python-client==2.108.0
google-auth==2.25.0
feedparser==6.0.10
praw==7.7.1
```

#### 2.2 Create Cloud Function - Agent 3

Create `agent_3_cloud/main.py`:

```python
import os
import functions_framework
from agent_3 import TechnicalDebtScanner

@functions_framework.http
def agent_3_handler(request):
    """Cloud Function entry point for Agent 3"""
    try:
        scanner = TechnicalDebtScanner()
        scanner.run()
        return {'status': 'success', 'message': 'Agent 3 executed successfully'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500
```

Deploy:

```bash
gcloud functions deploy agent-3-tech-debt \
  --runtime python39 \
  --trigger-http \
  --entry-point agent_3_handler \
  --region us-central1 \
  --set-env-vars SPREADSHEET_ID=your_spreadsheet_id \
  --timeout 540s \
  --memory 256MB
```

#### 2.3 Setup Cloud Scheduler

```bash
# Agent 3 - Daily at 8 AM
gcloud scheduler jobs create http agent-3-daily \
  --schedule="0 8 * * *" \
  --uri="https://us-central1-your-project.cloudfunctions.net/agent-3-tech-debt" \
  --http-method=POST \
  --time-zone="America/Chicago"

# Agent 4 - Daily at 9 AM
gcloud scheduler jobs create http agent-4-daily \
  --schedule="0 9 * * *" \
  --uri="https://us-central1-your-project.cloudfunctions.net/agent-4-regional-news" \
  --http-method=POST \
  --time-zone="America/Chicago"
```

---

## Monitoring & Maintenance

### Daily Workflow (5-10 minutes)

1. **Open Google Sheets**
   - Navigate to "Automation Queue" tab

2. **Filter for Pending Reviews**
   - Click Data → Create a filter
   - Filter Status column = "Pending Review"

3. **Review Each Entry**
   - Click Source URL to view original content
   - Assess if company/signal is relevant
   - Update Status to:
     - "Approved" - Relevant, add to pipeline
     - "Rejected" - Not relevant
     - "Needs More Info" - Requires research

4. **For Approved Entries**
   - Research the company
   - Add to "Company Details" tab (if new)
   - Move to "Active Prospects" tab
   - Plan outreach strategy

### Weekly Maintenance (15-30 minutes)

#### Check Agent Logs

```bash
# View recent Agent 3 logs
tail -100 logs/agent_3.log

# View recent Agent 4 logs
tail -100 logs/agent4.log

# Check for errors
grep ERROR logs/*.log
```

#### Verify Data Quality

1. Check for duplicate entries in Automation Queue
2. Validate that relevance scores make sense
3. Review "Unknown" companies - can you identify them?

#### Adjust Configurations

If you're getting too many false positives:

**agent_3_keywords.json:**
- Make keywords more specific
- Add exclusion patterns

**agent_4_sources.json:**
- Adjust regional focus
- Add/remove subreddits

#### Test RSS Feeds

Some feeds break over time. Test them:

```bash
# Test feeds manually
python3 -c "
import feedparser
feeds = [
    'https://techcrunch.com/feed/',
    'https://news.ycombinator.com/rss'
]
for url in feeds:
    feed = feedparser.parse(url)
    print(f'{url}: {len(feed.entries)} entries')
"
```

### Monthly Maintenance (30-60 minutes)

1. **Review Performance**
   - How many signals found?
   - How many were relevant (approved)?
   - Approval rate by agent

2. **Update Keywords**
   - Add new industry terms
   - Remove ineffective keywords

3. **Expand Sources**
   - Find new relevant RSS feeds
   - Add new subreddits to monitor

4. **Optimize Timing**
   - Adjust cron schedules if needed
   - Consider time zones for regional news

---

## Troubleshooting

### "Permission denied" Error

**Problem:** Agents can't write to Google Sheets

**Solution:**
1. Check service account email in `credentials.json`
2. Verify it has Editor access to your spreadsheet
3. Share spreadsheet with service account email

### No Entries Appearing in Sheets

**Problem:** Agents run but no data in sheets

**Solutions:**
1. Check SPREADSHEET_ID in `.env` is correct
2. Verify Automation Queue tab exists with exact name
3. Check logs for errors: `cat logs/agent_3.log`
4. Run test script: `python3 test_sheets.py`

### RSS Feed Errors

**Problem:** "Feed parsing error" in logs

**Solutions:**
1. Some feeds change URLs - update `sources.json`
2. Feed might be temporarily down - retry later
3. Feed might require authentication - find alternative
4. Test feed manually in browser

### Reddit API Errors

**Problem:** "Invalid credentials" or "429 Too Many Requests"

**Solutions:**

**Invalid Credentials:**
1. Verify REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in `.env`
2. Check Reddit app is still active at reddit.com/prefs/apps
3. Regenerate secret if needed

**Rate Limiting:**
1. Reduce check frequency in `sources.json`
2. Limit subreddits monitored
3. Add delays between requests

### Too Many False Positives

**Problem:** Most detected signals aren't relevant

**Solutions:**

**Option 1 - Stricter Keywords:**
```json
{
  "technical_debt_signals": [
    "legacy system migration",
    "modernization project",
    "technical debt sprint"
  ]
}
```

**Option 2 - Require Multiple Keywords:**
Modify `agent_3.py`:
```python
def analyze_entry(self, entry: Dict) -> Optional[Dict]:
    # ... existing code ...
    
    # Require at least 2 keywords
    if len(found_keywords) < 2:
        return None
```

**Option 3 - Higher Relevance Threshold:**
Only review scores ≥ 7 in Google Sheets

### Agent Crashes

**Problem:** Agent stops mid-execution

**Check Logs:**
```bash
tail -100 logs/agent_3.log
```

**Common Issues:**
1. **Network timeout** - Add retry logic
2. **Memory error** - Reduce batch size
3. **Rate limiting** - Add delays

**Add Retry Logic:**
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def fetch_feed(self, feed_config: Dict) -> List[Dict]:
    # ... existing code ...
```

### Google Sheets API Quota

**Problem:** "Quota exceeded" error

**Solutions:**
1. Reduce agent frequency
2. Batch write operations (already implemented)
3. Upgrade to paid Google Workspace (higher quotas)

**Current Free Tier Limits:**
- 100 requests per 100 seconds per user
- 500 requests per 100 seconds per project

### Time Zone Issues

**Problem:** Timestamps don't match your local time

**Solution:** Specify timezone in scripts:

```python
from datetime import datetime
import pytz

# Set timezone
tz = pytz.timezone('America/Chicago')
now = datetime.now(tz)
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
```

---

## Advanced Configuration

### Email Alerts on Errors

Add email notifications when agents fail:

```python
# shared/alerts.py
import smtplib
from email.mime.text import MIMEText

def send_alert(subject: str, message: str):
    """Send email alert"""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = os.getenv('ALERT_EMAIL_FROM')
    msg['To'] = os.getenv('ALERT_EMAIL_TO')
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(
            os.getenv('ALERT_EMAIL_FROM'),
            os.getenv('ALERT_EMAIL_PASSWORD')
        )
        server.send_message(msg)
```

Update `.env`:
```bash
ALERT_EMAIL_FROM=your-email@gmail.com
ALERT_EMAIL_TO=your-email@gmail.com
ALERT_EMAIL_PASSWORD=your-app-password
```

### Deduplication

Prevent duplicate entries:

```python
def is_duplicate(self, url: str) -> bool:
    """Check if URL already exists in sheet"""
    existing = self.sheets_client.read_range('Automation Queue!E:E')
    urls = [row[0] for row in existing if row]
    return url in urls

def write_to_sheets(self, signals: List[Dict]):
    """Write signals, skipping duplicates"""
    unique_signals = [s for s in signals if not self.is_duplicate(s['source_url'])]
    # ... rest of method ...
```

### Slack Notifications

Send high-priority signals to Slack:

```python
import requests

def send_to_slack(signal: Dict):
    """Send signal to Slack webhook"""
    if signal['relevance_score'] >= 8:
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        message = {
            'text': f"🚨 High Priority Signal (Score: {signal['relevance_score']})",
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"*{signal['title']}*\n{signal['signal_description']}"
                    }
                },
                {
                    'type': 'actions',
                    'elements': [{
                        'type': 'button',
                        'text': {'type': 'plain_text', 'text': 'View Source'},
                        'url': signal['source_url']
                    }]
                }
            ]
        }
        
        requests.post(webhook_url, json=message)
```

---

## Next Steps

### Week 1: Validation
- ✅ Deploy Agents 3 & 4
- ✅ Run for 1 week
- ✅ Review daily results
- ✅ Tune keywords and sources

### Week 2-4: Optimization
- Adjust relevance scoring
- Add more RSS feeds
- Fine-tune regional keywords
- Reduce false positives

### Month 2: Expansion
- Subscribe to Apollo.io ($49/month)
- Deploy Agent 1 (Funding Monitor)
- Deploy Agent 5 (Company Enrichment)
- Deploy Agent 7 (Email Generator)

### Month 3: Full System
- Subscribe to PhantomBuster ($59/month)
- Subscribe to Claude API ($30/month)
- Deploy remaining agents
- Migrate to HubSpot (optional)

---

## Cost Tracking

### Current Setup (Agents 3 & 4)

| Service | Monthly Cost |
|---------|--------------|
| Google Sheets API | $0 (free tier) |
| Reddit API | $0 (free) |
| RSS Feeds | $0 (free) |
| GCP Cloud Functions | $0 (free tier + $300 credit) |
| **TOTAL** | **$0/month** |

### Future Expansion

**Phase 2 (Months 2-3): $138/month**
- Apollo.io: $49
- PhantomBuster: $59
- Claude API: $30

**Phase 3 (Month 4+): $168-218/month**
- Phase 2 services: $138
- GCP hosting: $30-80 (after free credit)

---

## Resources & Documentation

### APIs & Services
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Reddit API (PRAW)](https://praw.readthedocs.io)
- [Feedparser Documentation](https://feedparser.readthedocs.io)

### Python Libraries
- [google-api-python-client](https://github.com/googleapis/google-api-python-client)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [praw](https://praw.readthedocs.io/)

### Deployment
- [GCP Cloud Functions](https://cloud.google.com/functions/docs)
- [GCP Cloud Scheduler](https://cloud.google.com/scheduler/docs)
- [Cron Syntax](https://crontab.guru/)

### Community
- Results CTO Project Documentation (this project)
- Stack Overflow: `google-sheets-api`, `reddit-api`, `rss-feeds`

---

## Support & Questions

### Getting Help

1. **Check logs first:** Most issues are visible in `logs/*.log`
2. **Review this guide:** Search for your error message
3. **Test components individually:**
   - Test Google Sheets: `python3 test_sheets.py`
   - Test RSS feeds manually
   - Test Reddit API with PRAW

### Common Issues Reference

| Error | Section |
|-------|---------|
| Permission denied | [Troubleshooting](#permission-denied-error) |
| No data in sheets | [Troubleshooting](#no-entries-appearing-in-sheets) |
| Feed errors | [Troubleshooting](#rss-feed-errors) |
| Reddit API issues | [Troubleshooting](#reddit-api-errors) |
| Too many false positives | [Troubleshooting](#too-many-false-positives) |

---

## Quick Reference

### Start Agents Manually
```bash
python3 agent_3_tech_debt/agent_3.py
python3 agent_4_regional_news/agent_4.py
```

### View Logs
```bash
tail -f logs/agent_3.log
tail -f logs/agent_4.log
```

### Check Cron Jobs
```bash
crontab -l
```

### Edit Configuration
```bash
nano config/agent_3_keywords.json
nano config/agent_4_sources.json
```

### Test Google Sheets
```bash
python3 test_sheets.py
```

---

## Success Metrics

Track these weekly:

1. **Signals Detected**
   - Total signals found
   - By agent (3 vs 4)
   - By source (feed/subreddit)

2. **Signal Quality**
   - Approval rate (approved / total)
   - Average relevance score
   - False positive rate

3. **Workflow Efficiency**
   - Time spent reviewing
   - Signals converted to prospects
   - Prospects converted to outreach

**Target KPIs (Month 1):**
- 20-50 signals/week
- 30%+ approval rate
- <10 minutes/day review time

---

**🎉 You're ready to build! Start with validation, tune based on results, then expand to paid agents.**

**Questions? Everything you need is in this guide. Master these 2 agents before adding complexity.**
