from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'OSINT Investigador BR',
        'version': '1.0.0'
    })

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    return jsonify({
        'message': 'API funcionando!',
        'method': request.method,
        'status': 'ok'
    })

# Handler para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=False)