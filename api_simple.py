from flask import Flask, request, jsonify, render_template_string
import requests
import json
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Página principal simples"""
    return "<h1>OSINT Investigador BR - Versão Simples</h1>"

@app.route('/api')
def api_info():
    """Informações da API"""
    return jsonify({
        "status": "success",
        "message": "OSINT Investigador BR API",
        "version": "2.0.0",
        "endpoints": [
            "/api/consultar/cruzamento",
            "/api/status"
        ]
    })

@app.route('/api/status')
def api_status():
    """Status da API"""
    return jsonify({
        "status": "success",
        "message": "API funcionando",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/consultar/cruzamento', methods=['POST'])
def api_consultar_cruzamento():
    """API de cruzamento de dados pessoais"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        # Extrair dados de entrada
        nome = data.get('nome', '').strip()
        cpf = data.get('cpf', '').strip()
        telefone = data.get('telefone', '').strip()
        
        # Validar se pelo menos um campo foi fornecido
        if not nome and not cpf and not telefone:
            return jsonify({"erro": "Pelo menos um campo deve ser fornecido"}), 400
        
        # Resultado simplificado do cruzamento
        resultado_cruzamento = {
            "dados_entrada": {
                "nome": nome if nome else None,
                "cpf": cpf if cpf else None,
                "telefone": telefone if telefone else None
            },
            "dados_encontrados": {
                "cpf_info": {"status": "simulado", "nome": "João da Silva"} if cpf else None,
                "telefone_info": {"status": "simulado", "operadora": "Vivo"} if telefone else None,
                "nome_info": {"status": "simulado", "registros": 3} if nome else None
            },
            "vinculos": [
                "CPF e telefone pertencem à mesma pessoa" if cpf and telefone else None,
                "Nome confere com dados do CPF" if nome and cpf else None
            ],
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
        # Remove valores None
        resultado_cruzamento["vinculos"] = [v for v in resultado_cruzamento["vinculos"] if v]
        
        return jsonify(resultado_cruzamento)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro interno: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/<path:path>')
def api_catch_all(path):
    """Captura outras rotas da API"""
    return jsonify({
        "status": "success",
        "message": "Endpoint não encontrado",
        "available_endpoints": [
            "/api/consultar/cruzamento",
            "/api/status"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)