"""
Cloud Functions entry points for Results CTO agents
"""

import os
import sys
import functions_framework
from flask import jsonify

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agent_3.agent import TechnicalDebtScanner
from agent_4.agent import RegionalNewsMonitor


@functions_framework.http
def agent_3_handler(request):
    """
    Cloud Function entry point for Agent 3: Technical Debt Scanner
    
    Args:
        request: Flask request object
    
    Returns:
        JSON response with status
    """
    try:
        scanner = TechnicalDebtScanner()
        scanner.run()
        
        return jsonify({
            'status': 'success',
            'message': 'Agent 3 executed successfully',
            'agent': 'Technical Debt Scanner'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'agent': 'Technical Debt Scanner'
        }), 500


@functions_framework.http
def agent_4_handler(request):
    """
    Cloud Function entry point for Agent 4: Regional News Monitor
    
    Args:
        request: Flask request object
    
    Returns:
        JSON response with status
    """
    try:
        monitor = RegionalNewsMonitor()
        monitor.run()
        
        return jsonify({
            'status': 'success',
            'message': 'Agent 4 executed successfully',
            'agent': 'Regional News Monitor'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'agent': 'Regional News Monitor'
        }), 500
