#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Investigador BR - Handler Vercel Simplificado
Sistema profissional para investigações OSINT no Brasil
Otimizado para Vercel Serverless Functions
"""

import os
import sys
import json
from flask import Flask, request, jsonify

# Adiciona o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Inicialização do Flask
app = Flask(__name__)

# Variável global para o investigador
investigador = None

def init_investigador():
    """Inicializa o investigador com tratamento de erros"""
    global investigador
    if investigador is not None:
        return investigador
    
    try:
        from osint_investigador import OSINTInvestigador
        investigador = OSINTInvestigador()
        return investigador
    except Exception as e:
        print(f"Erro ao inicializar investigador: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check para monitoramento"""
    inv = init_investigador()
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'environment': 'production',
        'investigador_loaded': inv is not None,
        'service': 'OSINT Investigador BR'
    })

@app.route('/api/consultar_cpf', methods=['POST'])
def consultar_cpf():
    """API para consulta de CPF"""
    try:
        inv = init_investigador()
        if not inv:
            return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados JSON inválidos'}), 400
            
        cpf = data.get('cpf', '').strip()
        if not cpf:
            return jsonify({'erro': 'CPF é obrigatório'}), 400
        
        resultado = inv.consultar_dados_pessoais_avancado(cpf=cpf)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

@app.route('/api/consultar_nome', methods=['POST'])
def consultar_nome():
    """API para consulta de Nome"""
    try:
        inv = init_investigador()
        if not inv:
            return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados JSON inválidos'}), 400
            
        nome = data.get('nome', '').strip()
        if not nome:
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        resultado = inv.consultar_dados_pessoais_avancado(nome=nome)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

@app.route('/api/consultar_cep', methods=['POST'])
def consultar_cep():
    """API para consulta de CEP"""
    try:
        inv = init_investigador()
        if not inv:
            return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados JSON inválidos'}), 400
            
        cep = data.get('cep', '').strip()
        if not cep:
            return jsonify({'erro': 'CEP é obrigatório'}), 400
        
        resultado = inv.consultar_cep(cep)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

@app.route('/api/consultar_ddd', methods=['POST'])
def consultar_ddd():
    """API para consulta de DDD"""
    try:
        inv = init_investigador()
        if not inv:
            return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados JSON inválidos'}), 400
            
        ddd = data.get('ddd', '').strip()
        if not ddd:
            return jsonify({'erro': 'DDD é obrigatório'}), 400
        
        resultado = inv.consultar_ddd(ddd)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

@app.route('/api/consultar_cnpj', methods=['POST'])
def consultar_cnpj():
    """API para consulta de CNPJ"""
    try:
        inv = init_investigador()
        if not inv:
            return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados JSON inválidos'}), 400
            
        cnpj = data.get('cnpj', '').strip()
        if not cnpj:
            return jsonify({'erro': 'CNPJ é obrigatório'}), 400
        
        resultado = inv.consultar_cnpj(cnpj)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

@app.route('/api/consultar_telefone', methods=['POST'])
def consultar_telefone():
    """API para consulta de Telefone"""
    try:
        inv = init_investigador()
        if not inv:
            return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados JSON inválidos'}), 400
            
        telefone = data.get('telefone', '').strip()
        if not telefone:
            return jsonify({'erro': 'Telefone é obrigatório'}), 400
        
        resultado = inv.consultar_telefone(telefone)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

# Handler principal para Vercel
def handler(request):
    """Handler principal para Vercel"""
    with app.test_request_context(request.url, method=request.method, data=request.data, headers=request.headers):
        try:
            response = app.full_dispatch_request()
            return response
        except Exception as e:
            return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

# Para execução local
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)