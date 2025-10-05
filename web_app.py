"""
Interface Web para OSINT Investigador BR
Aplicação Flask com interface moderna e responsiva
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import csv
import io
from datetime import datetime
from osint_investigador import investigador
from utils.logger import logger
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)
CORS(app)

# Configurações
app.config['SECRET_KEY'] = 'osint-investigador-br-2024'
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/consultar/cep', methods=['POST'])
def api_consultar_cep():
    """API para consulta de CEP"""
    try:
        data = request.get_json()
        cep = data.get('cep', '').strip()
        
        if not cep:
            return jsonify({'erro': 'CEP é obrigatório'}), 400
        
        resultado = investigador.consultar_cep(cep)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_cep: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/consultar/ddd', methods=['POST'])
def api_consultar_ddd():
    """API para consulta de DDD"""
    try:
        data = request.get_json()
        ddd = data.get('ddd', '').strip()
        
        if not ddd:
            return jsonify({'erro': 'DDD é obrigatório'}), 400
        
        resultado = investigador.consultar_ddd(ddd)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_ddd: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/consultar/cnpj', methods=['POST'])
def api_consultar_cnpj():
    """API para consulta de CNPJ"""
    try:
        data = request.get_json()
        cnpj = data.get('cnpj', '').strip()
        fonte = data.get('fonte', 'brasilapi')
        
        if not cnpj:
            return jsonify({'erro': 'CNPJ é obrigatório'}), 400
        
        resultado = investigador.consultar_cnpj(cnpj, fonte)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_cnpj: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/consultar/bancos', methods=['GET'])
def api_consultar_bancos():
    """API para listar bancos"""
    try:
        resultado = investigador.consultar_bancos()
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_bancos: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/consultar/banco/<codigo>', methods=['GET'])
def api_consultar_banco(codigo):
    """API para consultar banco específico"""
    try:
        resultado = investigador.buscar_banco_por_codigo(codigo)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_banco: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/consultar/municipios/<uf>', methods=['GET'])
def api_consultar_municipios(uf):
    """API para consultar municípios por UF"""
    try:
        resultado = investigador.consultar_municipios_uf(uf)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_municipios: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/cache/limpar', methods=['POST'])
def api_limpar_cache():
    """API para limpar cache"""
    try:
        resultado = investigador.limpar_cache()
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API limpar_cache: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/cache/estatisticas', methods=['GET'])
def api_estatisticas_cache():
    """API para estatísticas do cache"""
    try:
        resultado = investigador.estatisticas_cache()
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API estatisticas_cache: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/exportar/<formato>', methods=['POST'])
def api_exportar_dados(formato):
    """API para exportar dados"""
    try:
        data = request.get_json()
        dados = data.get('dados', {})
        nome_arquivo = data.get('nome_arquivo', f'osint_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        if formato.lower() == 'json':
            output = io.StringIO()
            json.dump(dados, output, ensure_ascii=False, indent=2)
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='application/json',
                as_attachment=True,
                download_name=f'{nome_arquivo}.json'
            )
        
        elif formato.lower() == 'csv':
            output = io.StringIO()
            
            # Converte dados para formato tabular
            if isinstance(dados, dict):
                if 'cidades' in dados:  # DDD
                    writer = csv.writer(output)
                    writer.writerow(['Estado', 'Cidade'])
                    for cidade in dados.get('cidades', []):
                        writer.writerow([dados.get('estado', ''), cidade])
                
                elif 'bancos' in dados:  # Bancos
                    writer = csv.writer(output)
                    writer.writerow(['Código', 'Nome', 'Nome Completo', 'ISPB'])
                    for banco in dados.get('bancos', []):
                        writer.writerow([
                            banco.get('code', ''),
                            banco.get('name', ''),
                            banco.get('fullName', ''),
                            banco.get('ispb', '')
                        ])
                
                else:  # Dados gerais
                    writer = csv.writer(output)
                    writer.writerow(['Campo', 'Valor'])
                    for key, value in dados.items():
                        if isinstance(value, (str, int, float)):
                            writer.writerow([key, value])
            
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'{nome_arquivo}.csv'
            )
        
        else:
            return jsonify({'erro': 'Formato não suportado'}), 400
    
    except Exception as e:
        logger.error(f"Erro na API exportar_dados: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handler para erro 404"""
    return jsonify({'erro': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erro 500"""
    return jsonify({'erro': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    logger.info(f"Iniciando OSINT Investigador BR Web App em {FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)