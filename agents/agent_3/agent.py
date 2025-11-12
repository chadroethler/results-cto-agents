"""
Agent 3: Technical Debt Scanner
Monitors RSS feeds for technical debt signals and companies seeking help
"""

import os

from shared.sheets_client import SheetsClient
from shared.utils import load_json_config, setup_logging, sanitize_text, get_timestamp, get_date

import sys
import feedparser
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = setup_logging("agent_3")


class TechnicalDebtScanner:
    """Scans RSS feeds for technical debt signals"""

    def __init__(self, config_dir: str = "config"):
        """
        Initialize scanner

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir

        # Initialize Sheets client
        self.sheets_client = SheetsClient()

        # Load configuration
        self.sources = load_json_config(f"{config_dir}/agent_3_sources.json")
        self.keywords = load_json_config(f"{config_dir}/agent_3_keywords.json")

        # Combine all keyword categories
        self.all_keywords = []
        for category in self.keywords.values():
            self.all_keywords.extend([kw.lower() for kw in category])

        logger.info(f"Initialized with {len(self.sources['rss_feeds'])} feeds")
        logger.info(f"Monitoring {len(self.all_keywords)} keywords")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def fetch_feed(self, feed_config: Dict) -> List[Dict]:
        """
        Fetch and parse an RSS feed with retry logic

        Args:
            feed_config: Feed configuration dict

        Returns:
            List of entry dicts
        """
        try:
            logger.info(f"Fetching feed: {feed_config['name']}")
            feed = feedparser.parse(feed_config["url"])

            if feed.bozo:  # Feed parsing error
                logger.warning(f"Feed parsing error for {feed_config['name']}: {feed.bozo_exception}")
                return []

            entries = []
            for entry in feed.entries[:20]:  # Limit to last 20 entries
                entries.append(
                    {
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", ""),
                        "published": entry.get("published", ""),
                        "source": feed_config["name"],
                    }
                )

            logger.info(f"Retrieved {len(entries)} entries from {feed_config['name']}")
            return entries

        except Exception as e:
            logger.error(f"Error fetching feed {feed_config['name']}: {e}")
            return []

    def check_keywords(self, text: str) -> List[str]:
        """
        Check if text contains any keywords

        Args:
            text: Text to check

        Returns:
            List of found keywords
        """
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

        Args:
            text: Text to extract from

        Returns:
            Company name or None
        """
        # Common patterns: "Company X announced...", "At Company Y, we..."
        patterns = [" at ", " for ", " with ", " announced ", " launched ", " raised ", " founded "]

        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in patterns and i + 1 < len(words):
                potential_company = words[i + 1].strip(".,;:")
                if potential_company and potential_company[0].isupper() and len(potential_company) > 2:
                    return potential_company

        return None

    def analyze_entry(self, entry: Dict) -> Optional[Dict]:
        """
        Analyze a feed entry for relevant signals

        Args:
            entry: Feed entry dict

        Returns:
            Signal dict or None
        """
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
            "company_name": company_name or "Unknown",
            "signal_type": "Technical Debt",
            "signal_description": ", ".join(found_keywords[:3]),  # Top 3 keywords
            "source_url": entry["link"],
            "source": entry["source"],
            "detected_date": get_date(),
            "relevance_score": relevance_score,
            "title": sanitize_text(entry["title"], 200),
            "summary": sanitize_text(entry["summary"], 500),
        }

    def process_feeds(self) -> List[Dict]:
        """
        Process all configured feeds

        Returns:
            List of signals found
        """
        all_signals = []

        for feed_config in self.sources["rss_feeds"]:
            entries = self.fetch_feed(feed_config)

            for entry in entries:
                signal = self.analyze_entry(entry)
                if signal:
                    all_signals.append(signal)
                    logger.info(f"Found signal: {signal['title'][:50]}... (score: {signal['relevance_score']})")

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
        # Column order: Queue ID, Agent Source, Company Name, Signal Type,
        # Signal Details, Priority Score, Status, Date Added, Action Required,
        # Assigned To, Notes
        rows = []
        for signal in signals:
            # Skip duplicates - check column K (Notes) which has the URL
            if self.sheets_client.check_duplicate("Automation Queue", "K", signal["source_url"]):
                logger.info(f"Skipping duplicate: {signal['source_url']}")
                continue

            row = [
                "",  # Queue ID (empty - can add auto-increment later)
                "Agent 3",  # Agent Source
                signal.get("company_name", "Unknown"),  # Company Name
                signal.get("signal_type", "Technical Debt"),  # Signal Type
                signal.get("signal_description", ""),  # Signal Details
                signal.get("relevance_score", 2),  # Priority Score
                "Pending Review",  # Status
                get_date(),  # Date Added
                "",  # Action Required (empty)
                "",  # Assigned To (empty)
                signal.get("source_url", ""),  # Notes (URL)
            ]
            rows.append(row)

        if not rows:
            logger.info("No new signals to write (all duplicates)")
            return

        try:
            self.sheets_client.append_rows("Automation Queue", rows)
            logger.info(f"Successfully wrote {len(rows)} rows to Automation Queue")
        except Exception as e:
            logger.error(f"Error writing to sheets: {e}")
            raise

    def run(self):
        """Main execution method"""
        logger.info("=" * 60)
        logger.info("Agent 3: Technical Debt Scanner - Starting")
        logger.info("=" * 60)

        try:
            # Process feeds
            signals = self.process_feeds()
            logger.info(f"Total signals found: {len(signals)}")

            # Write to Google Sheets
            self.write_to_sheets(signals)

            logger.info("Agent 3: Technical Debt Scanner - Complete")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Error in agent execution: {e}", exc_info=True)
            raise


def main():
    """Entry point for standalone execution"""
    if not os.getenv("AGENT_3_ENABLED", "true").lower() == "true":
        logger.info("Agent 3 is disabled")
        return

    try:
        scanner = TechnicalDebtScanner()
        scanner.run()
    except Exception as e:
        logger.error(f"Fatal error in Agent 3: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
