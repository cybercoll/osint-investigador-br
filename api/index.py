from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    """
    Rota principal da API
    """
    response_data = {
        "status": "success",
        "message": "OSINT Investigador BR - API Funcionando!",
        "version": "1.0.0",
        "method": request.method,
        "path": request.path
    }
    return jsonify(response_data)

@app.route('/api')
def api():
    """
    Rota da API
    """
    response_data = {
        "status": "success",
        "message": "OSINT Investigador BR - API Funcionando!",
        "version": "1.0.0",
        "method": request.method,
        "path": request.path,
        "endpoint": "api"
    }
    return jsonify(response_data)

@app.route('/api/<path:path>')
def api_catch_all(path):
    """
    Rota catch-all para /api/*
    """
    response_data = {
        "status": "success",
        "message": "OSINT Investigador BR - API Funcionando!",
        "version": "1.0.0",
        "method": request.method,
        "path": request.path,
        "endpoint": f"api/{path}"
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)