"""
Agent 4: Regional News Monitor
Monitors Reddit and regional sources for expansion, funding, and hiring signals
"""

import os
import sys
import logging
import praw
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.sheets_client import SheetsClient
from shared.utils import load_json_config, setup_logging, sanitize_text, get_timestamp, get_date

logger = setup_logging('agent_4')


class RegionalNewsMonitor:
    """Monitors Reddit for regional business signals"""
    
    def __init__(self, config_dir: str = 'config'):
        """
        Initialize monitor
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        
        # Initialize Sheets client
        self.sheets_client = SheetsClient()
        
        # Load configuration
        self.sources = load_json_config(f'{config_dir}/agent_4_sources.json')
        self.keywords = load_json_config(f'{config_dir}/agent_4_keywords.json')
        
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
    
    def check_keywords(self, text: str) -> Tuple[List[str], bool]:
        """
        Check if text contains keywords
        
        Args:
            text: Text to check
        
        Returns:
            Tuple of (found_keywords, has_regional_keyword)
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
        """
        Extract company name from text
        
        Args:
            text: Text to extract from
        
        Returns:
            Company name or None
        """
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
                        if potential_company and potential_company[0].isupper():
                            return potential_company
        
        return None
    
    def determine_signal_type(self, keywords: List[str]) -> str:
        """
        Determine the primary signal type based on keywords
        
        Args:
            keywords: List of found keywords
        
        Returns:
            Signal type string
        """
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
        """
        Analyze a Reddit post for relevant signals
        
        Args:
            post: PRAW submission object
        
        Returns:
            Signal dict or None
        """
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
            'detected_date': get_date(),
            'relevance_score': relevance_score,
            'title': sanitize_text(post.title, 200),
            'summary': sanitize_text(post.selftext, 500) if post.selftext else sanitize_text(post.title, 500)
        }
    
    def monitor_subreddit(self, subreddit_name: str) -> List[Dict]:
        """
        Monitor a single subreddit
        
        Args:
            subreddit_name: Name of subreddit to monitor
        
        Returns:
            List of signals found
        """
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
        """
        Process all configured subreddits
        
        Returns:
            List of all signals found
        """
        all_signals = []
        
        for subreddit_name in self.sources['subreddits']:
            signals = self.monitor_subreddit(subreddit_name)
            all_signals.extend(signals)
        
        return all_signals
    
    def write_to_sheets(self, signals: List[Dict]):
        """
        Write signals to Google Sheets
        
        Args:
            signals: List of signal dicts
        """
        if not signals:
            logger.info("No signals to write")
            return
        
        logger.info(f"Writing {len(signals)} signals to Google Sheets")
        
        # Prepare rows for Automation Queue tab
        rows = []
        for signal in signals:
            # Skip duplicates
            if self.sheets_client.check_duplicate('Automation Queue', 'E', signal['source_url']):
                logger.info(f"Skipping duplicate: {signal['source_url']}")
                continue
            
            row = [
                get_timestamp(),  # Timestamp
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
        
        if not rows:
            logger.info("No new signals to write (all duplicates)")
            return
        
        try:
            self.sheets_client.append_rows('Automation Queue', rows)
            logger.info(f"Successfully wrote {len(rows)} rows to Automation Queue")
        except Exception as e:
            logger.error(f"Error writing to sheets: {e}")
            raise
    
    def run(self):
        """Main execution method"""
        logger.info("=" * 60)
        logger.info("Agent 4: Regional News Monitor - Starting")
        logger.info("=" * 60)
        
        try:
            # Process subreddits
            signals = self.process_subreddits()
            logger.info(f"Total signals found: {len(signals)}")
            
            # Write to Google Sheets
            self.write_to_sheets(signals)
            
            logger.info("Agent 4: Regional News Monitor - Complete")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error in agent execution: {e}", exc_info=True)
            raise


def main():
    """Entry point for standalone execution"""
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
