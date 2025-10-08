#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Investigador BR - Handler Vercel
Sistema profissional para investigações OSINT no Brasil
Otimizado para Vercel Serverless Functions
"""

import os
import sys
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from osint_investigador import OSINTInvestigador
    from dotenv import load_dotenv
except ImportError as e:
    logging.error(f"Erro de importação: {e}")
    # Fallback para imports básicos
    OSINTInvestigador = None

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Inicialização do Flask
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'osint-investigador-br-2024')

# Configuração CORS
CORS(app, origins=['*'])

# Headers de segurança
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Inicialização do investigador (com fallback)
try:
    investigador = OSINTInvestigador() if OSINTInvestigador else None
except Exception as e:
    logger.error(f"Erro ao inicializar investigador: {e}")
    investigador = None

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Erro ao carregar template: {e}")
        return jsonify({'erro': 'Erro ao carregar página'}), 500

@app.route('/manifest.json')
def manifest():
    """Serve o manifest PWA"""
    return send_from_directory('../static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    """Serve o service worker PWA"""
    return send_from_directory('../static', 'sw.js')

@app.route('/api/health')
def health_check():
    """Health check para monitoramento"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'environment': 'production',
        'investigador_loaded': investigador is not None
    })

@app.route('/api/consultar_cpf', methods=['POST'])
def consultar_cpf():
    """API para consulta de CPF"""
    if not investigador:
        return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
    
    try:
        data = request.get_json()
        cpf = data.get('cpf', '').strip()
        
        if not cpf:
            return jsonify({'erro': 'CPF é obrigatório'}), 400
        
        # Usa o método correto para consulta de CPF
        resultado = investigador.consultar_dados_pessoais_avancado(cpf=cpf)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta CPF: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_nome', methods=['POST'])
def consultar_nome():
    """API para consulta de nome"""
    if not investigador:
        return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
    
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        
        if not nome:
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        # Usa o método correto para consulta de nome
        resultado = investigador.consultar_dados_pessoais_avancado(nome=nome)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta nome: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_telefone', methods=['POST'])
def consultar_telefone():
    """API para consulta de telefone"""
    if not investigador:
        return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
    
    try:
        data = request.get_json()
        telefone = data.get('telefone', '').strip()
        
        if not telefone:
            return jsonify({'erro': 'Telefone é obrigatório'}), 400
        
        resultado = investigador.consultar_telefone(telefone)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta telefone: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_cep', methods=['POST'])
def consultar_cep():
    """API para consulta de CEP"""
    if not investigador:
        return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
    
    try:
        data = request.get_json()
        cep = data.get('cep', '').strip()
        
        if not cep:
            return jsonify({'erro': 'CEP é obrigatório'}), 400
        
        resultado = investigador.consultar_cep(cep)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta CEP: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_ddd', methods=['POST'])
def consultar_ddd():
    """API para consulta de DDD"""
    if not investigador:
        return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
    
    try:
        data = request.get_json()
        ddd = data.get('ddd', '').strip()
        
        if not ddd:
            return jsonify({'erro': 'DDD é obrigatório'}), 400
        
        resultado = investigador.consultar_ddd(ddd)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta DDD: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/api/consultar_cnpj', methods=['POST'])
def consultar_cnpj():
    """API para consulta de CNPJ"""
    if not investigador:
        return jsonify({'erro': 'Serviço temporariamente indisponível'}), 503
    
    try:
        data = request.get_json()
        cnpj = data.get('cnpj', '').strip()
        
        if not cnpj:
            return jsonify({'erro': 'CNPJ é obrigatório'}), 400
        
        resultado = investigador.consultar_cnpj(cnpj)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na consulta CNPJ: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handler para páginas não encontradas"""
    return jsonify({'erro': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({'erro': 'Erro interno do servidor'}), 500

# Handler para Vercel
def handler(request, response):
    """Handler principal para Vercel"""
    return app(request, response)

# Para desenvolvimento local
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)