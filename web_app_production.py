#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Investigador BR - Versão Produção
Sistema profissional para investigações OSINT no Brasil
Otimizado para deployment online e acesso mobile
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from osint_investigador import OSINTInvestigador
from dotenv import load_dotenv

# Configuração de logging para produção
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Exporta a aplicação para Vercel
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'osint-investigador-br-2024')

# Configuração CORS para acesso mobile e web
CORS(app, origins=['*'])

# Headers de segurança para produção
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Inicialização do investigador OSINT
investigador = OSINTInvestigador()

@app.route('/')
def index():
    """Página principal otimizada para mobile"""
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    """Serve o manifest PWA"""
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    """Serve o service worker PWA"""
    return send_from_directory('static', 'sw.js')

@app.route('/api/consultar_cpf', methods=['POST'])
def consultar_cpf():
    """API para consulta de CPF otimizada"""
    try:
        data = request.get_json()
        cpf = data.get('cpf', '').strip()
        
        if not cpf:
            return jsonify({'erro': 'CPF é obrigatório'}), 400
        
        logger.info(f"Consulta CPF iniciada: {cpf[:3]}***")
        resultado = investigador.consultar_cpf(cpf)
        logger.info(f"Consulta CPF concluída: {cpf[:3]}***")
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta CPF: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_nome', methods=['POST'])
def consultar_nome():
    """API para consulta de nome otimizada"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        
        if not nome:
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        logger.info(f"Consulta nome iniciada: {nome[:10]}...")
        resultado = investigador.consultar_nome(nome)
        logger.info(f"Consulta nome concluída: {nome[:10]}...")
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta nome: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_telefone', methods=['POST'])
def consultar_telefone():
    """API para consulta de telefone otimizada"""
    try:
        data = request.get_json()
        telefone = data.get('telefone', '').strip()
        
        if not telefone:
            return jsonify({'erro': 'Telefone é obrigatório'}), 400
        
        logger.info(f"Consulta telefone iniciada: {telefone[:5]}***")
        resultado = investigador.consultar_telefone(telefone)
        logger.info(f"Consulta telefone concluída: {telefone[:5]}***")
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta telefone: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_cep', methods=['POST'])
def consultar_cep():
    """API para consulta de CEP otimizada"""
    try:
        data = request.get_json()
        cep = data.get('cep', '').strip()
        
        if not cep:
            return jsonify({'erro': 'CEP é obrigatório'}), 400
        
        logger.info(f"Consulta CEP iniciada: {cep}")
        resultado = investigador.consultar_cep(cep)
        logger.info(f"Consulta CEP concluída: {cep}")
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta CEP: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_ddd', methods=['POST'])
def consultar_ddd():
    """API para consulta de DDD otimizada"""
    try:
        data = request.get_json()
        ddd = data.get('ddd', '').strip()
        
        if not ddd:
            return jsonify({'erro': 'DDD é obrigatório'}), 400
        
        logger.info(f"Consulta DDD iniciada: {ddd}")
        resultado = investigador.consultar_ddd(ddd)
        logger.info(f"Consulta DDD concluída: {ddd}")
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta DDD: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_cnpj', methods=['POST'])
def consultar_cnpj():
    """API para consulta de CNPJ otimizada"""
    try:
        data = request.get_json()
        cnpj = data.get('cnpj', '').strip()
        
        if not cnpj:
            return jsonify({'erro': 'CNPJ é obrigatório'}), 400
        
        logger.info(f"Consulta CNPJ iniciada: {cnpj[:8]}***")
        resultado = investigador.consultar_cnpj(cnpj)
        logger.info(f"Consulta CNPJ concluída: {cnpj[:8]}***")
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta CNPJ: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/health')
def health_check():
    """Health check para monitoramento"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'environment': 'production'
    })

@app.errorhandler(404)
def not_found(error):
    """Handler para páginas não encontradas"""
    return jsonify({'erro': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({'erro': 'Erro interno do servidor'}), 500

# Função principal para Vercel
def handler(event, context):
    """Handler principal para Vercel serverless"""
    return app

if __name__ == '__main__':
    # Configuração para desenvolvimento local
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando OSINT Investigador BR na porta {port}")
    logger.info(f"Modo debug: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )