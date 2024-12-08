from flask import Flask, request, jsonify, send_file
from scholar_to_bibtex import extract_author_id, get_publications, create_bibtex_entry
from dotenv import load_dotenv
import os
import tempfile

app = Flask(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv('SERPAPI_KEY')

@app.route('/convert', methods=['POST'])
def convert_to_bibtex():
    try:
        data = request.get_json()
        if not data or 'scholar_url' not in data:
            return jsonify({'error': 'Missing scholar_url in request body'}), 400

        scholar_url = data['scholar_url']
        
        # Extract author ID
        author_id = extract_author_id(scholar_url)
        if not author_id:
            return jsonify({'error': 'Invalid Google Scholar URL'}), 400

        # Fetch publications
        publications = get_publications(author_id, api_key)
        if not publications:
            return jsonify({'error': 'No publications found'}), 404

        # Convert to BibTeX
        bibtex_entries = [create_bibtex_entry(article) for article in publications]
        bibtex_text = '\n\n'.join(bibtex_entries)

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bib') as f:
            f.write(bibtex_text)
            temp_path = f.name

        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f'scholar_{author_id}_publications.bib',
            mimetype='application/x-bibtex'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/convert/preview', methods=['POST'])
def preview_bibtex():
    """Preview BibTeX without downloading"""
    try:
        data = request.get_json()
        if not data or 'scholar_url' not in data:
            return jsonify({'error': 'Missing scholar_url in request body'}), 400

        scholar_url = data['scholar_url']
        author_id = extract_author_id(scholar_url)
        publications = get_publications(author_id, api_key)
        bibtex_entries = [create_bibtex_entry(article) for article in publications]
        
        return jsonify({
            'author_id': author_id,
            'publication_count': len(publications),
            'bibtex': '\n\n'.join(bibtex_entries)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'api_key_configured': bool(api_key)
    })

if __name__ == '__main__':
    if not api_key:
        print("Error: SERPAPI_KEY not found in environment variables")
        print("Please create a .env file with your SerpAPI key: SERPAPI_KEY=your_key_here")
    else:
        app.run(host='0.0.0.0', debug=True, port=5000) 