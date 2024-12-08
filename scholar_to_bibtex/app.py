from flask import Flask, jsonify, request
from scholar_to_bibtex import ScholarToBibtex
from healthcheck import register_health_routes
import os
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_user_id(url):
    """Extract user ID from Google Scholar URL."""
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        user_id = query_params.get('user', [None])[0]
        if not user_id:
            raise ValueError("No user ID found in URL")
        return user_id
    except Exception as e:
        logger.error(f"Error extracting user ID from URL: {str(e)}")
        raise ValueError(f"Invalid Google Scholar URL: {str(e)}")

app = Flask(__name__)

# Register health check routes
register_health_routes(app)

# Get Scholar URL from environment
scholar_url = os.getenv('SCHOLAR_PROFILE_URL')
if not scholar_url:
    logger.error("SCHOLAR_PROFILE_URL not set in environment")
    raise ValueError("SCHOLAR_PROFILE_URL environment variable is required")

try:
    user_id = extract_user_id(scholar_url)
    logger.info(f"Extracted user ID: {user_id}")
except ValueError as e:
    logger.error(f"Error with Scholar URL: {str(e)}")
    raise

# Initialize ScholarToBibtex
scholar_to_bibtex = ScholarToBibtex(
    serpapi_key=os.getenv('SERPAPI_KEY'),
    output_dir=os.getenv('OUTPUT_DIR', '/app/data'),
    user_id=user_id
)

@app.route('/update', methods=['POST'])
def update_citations():
    try:
        result = scholar_to_bibtex.update_citations()
        return jsonify({
            'status': 'success',
            'message': 'Citations updated successfully',
            'details': result
        }), 200
    except Exception as e:
        logger.error(f"Error updating citations: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to update citations',
            'error': str(e)
        }), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration (excluding sensitive data)."""
    return jsonify({
        'scholar_url': scholar_url,
        'user_id': user_id,
        'output_dir': os.getenv('OUTPUT_DIR', '/app/data')
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 