from flask import jsonify

def register_health_routes(app):
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'scholar-service'
        }), 200 