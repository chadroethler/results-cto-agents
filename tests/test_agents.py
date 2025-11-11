"""
Basic unit tests for agents
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

from shared.utils import sanitize_text, get_date, get_timestamp
from shared.sheets_client import SheetsClient


class TestUtils:
    """Test utility functions"""
    
    def test_sanitize_text(self):
        """Test text sanitization"""
        # Normal text
        assert sanitize_text("Hello World") == "Hello World"
        
        # Long text
        long_text = "a" * 600
        result = sanitize_text(long_text, max_length=500)
        assert len(result) <= 503  # 500 + "..."
        assert result.endswith("...")
        
        # Empty text
        assert sanitize_text("") == ""
        assert sanitize_text(None) == ""
    
    def test_get_date(self):
        """Test date formatting"""
        date = get_date()
        assert len(date) == 10  # YYYY-MM-DD
        assert date[4] == '-'
        assert date[7] == '-'
    
    def test_get_timestamp(self):
        """Test timestamp formatting"""
        timestamp = get_timestamp()
        assert len(timestamp) == 19  # YYYY-MM-DD HH:MM:SS
        assert timestamp[4] == '-'
        assert timestamp[10] == ' '


class TestAgent3:
    """Test Agent 3 functionality"""
    
    @patch('agents.agent_3.agent.SheetsClient')
    @patch('agents.agent_3.agent.load_json_config')
    def test_initialization(self, mock_config, mock_sheets):
        """Test agent initialization"""
        from agent_3.agent import TechnicalDebtScanner
        
        mock_config.side_effect = [
            {'rss_feeds': []},
            {'technical_debt_signals': ['legacy']}
        ]
        
        scanner = TechnicalDebtScanner()
        assert scanner is not None
    
    def test_keyword_checking(self):
        """Test keyword matching"""
        from agent_3.agent import TechnicalDebtScanner
        
        with patch('agents.agent_3.agent.SheetsClient'), \
             patch('agents.agent_3.agent.load_json_config') as mock_config:
            
            mock_config.side_effect = [
                {'rss_feeds': []},
                {'technical_debt_signals': ['legacy system', 'refactor']}
            ]
            
            scanner = TechnicalDebtScanner()
            
            # Should find keywords
            text = "We need to refactor our legacy system"
            keywords = scanner.check_keywords(text)
            assert len(keywords) >= 2
            
            # Should not find keywords
            text = "This is unrelated content"
            keywords = scanner.check_keywords(text)
            assert len(keywords) == 0


class TestAgent4:
    """Test Agent 4 functionality"""
    
    @patch('agents.agent_4.agent.SheetsClient')
    @patch('agents.agent_4.agent.load_json_config')
    @patch('agents.agent_4.agent.praw.Reddit')
    def test_initialization(self, mock_reddit, mock_config, mock_sheets):
        """Test agent initialization"""
        from agent_4.agent import RegionalNewsMonitor
        
        mock_config.side_effect = [
            {'subreddits': [], 'regional_focus': []},
            {'funding_signals': ['funding']}
        ]
        
        monitor = RegionalNewsMonitor()
        assert monitor is not None
    
    def test_signal_type_determination(self):
        """Test signal type classification"""
        from agent_4.agent import RegionalNewsMonitor
        
        with patch('agents.agent_4.agent.SheetsClient'), \
             patch('agents.agent_4.agent.load_json_config') as mock_config, \
             patch('agents.agent_4.agent.praw.Reddit'):
            
            mock_config.side_effect = [
                {'subreddits': [], 'regional_focus': []},
                {'funding_signals': ['funding'], 'hiring_signals': ['hiring']}
            ]
            
            monitor = RegionalNewsMonitor()
            
            # Funding signal
            assert monitor.determine_signal_type(['funding', 'raised']) == 'Funding Announcement'
            
            # Hiring signal
            assert monitor.determine_signal_type(['hiring', 'seeking']) == 'Hiring Expansion'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
