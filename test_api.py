from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/consultar/cruzamento', methods=['POST'])
def api_consultar_cruzamento():
    """API de cruzamento de dados pessoais - teste simples"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        return jsonify({
            "status": "success",
            "message": "Teste de cruzamento funcionando",
            "dados_recebidos": data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro interno: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/status')
def api_status():
    """Status da API"""
    return jsonify({
        "status": "success",
        "message": "API funcionando",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)