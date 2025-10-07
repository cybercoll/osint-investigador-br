"""
Interface Web para OSINT Investigador BR
Aplicação Flask com interface moderna e responsiva
"""
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from brasilapi_integration import BrasilAPIClient, validar_cpf
from viacep_integration import ViaCEPClient
from directd_integration import consultar_dados_pessoais_cpf, consultar_dados_pessoais_nome, verificar_directd_config
import json
import csv
import io
from datetime import datetime
from osint_investigador import investigador
from utils.logger import logger
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

# Inicializar clientes das APIs gratuitas
brasil_api = BrasilAPIClient()
viacep_client = ViaCEPClient()

app = Flask(__name__)
CORS(app)

# Configurar para servir arquivos estáticos PWA
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

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


@app.route('/api/cep/<cep>', methods=['GET'])
def api_cep_get(cep):
    """API GET para consulta de CEP"""
    try:
        if not cep:
            return jsonify({'success': False, 'error': 'CEP é obrigatório'}), 400
        
        resultado = investigador.consultar_cep(cep)
        
        if resultado.get('sucesso'):
            return jsonify({'success': True, 'data': resultado})
        else:
            return jsonify({'success': False, 'error': resultado.get('erro', 'Erro desconhecido')}), 400
    
    except Exception as e:
        logger.error(f"Erro na API cep GET: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


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


@app.route('/api/ddd/<ddd>', methods=['GET'])
def api_ddd_get(ddd):
    """API GET para consulta de DDD"""
    try:
        if not ddd:
            return jsonify({'success': False, 'error': 'DDD é obrigatório'}), 400
        
        resultado = investigador.consultar_ddd(ddd)
        
        if resultado.get('sucesso'):
            return jsonify({'success': True, 'data': resultado})
        else:
            return jsonify({'success': False, 'error': resultado.get('erro', 'Erro desconhecido')}), 400
    
    except Exception as e:
        logger.error(f"Erro na API ddd GET: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/cache/stats', methods=['GET'])
def api_cache_stats():
    """API para estatísticas do cache"""
    try:
        resultado = investigador.estatisticas_cache()
        return jsonify({'success': True, 'data': resultado})
    
    except Exception as e:
        logger.error(f"Erro na API cache stats: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/telefone/<telefone>', methods=['GET'])
def api_consultar_telefone_get(telefone):
    """API para consultar telefone via GET"""
    try:
        resultado = investigador.consultar_telefone(telefone)
        if resultado.get('sucesso'):
            return jsonify({
                'success': True,
                'data': resultado
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('erro', 'Erro desconhecido')
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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


@app.route('/api/cnpj/<cnpj>', methods=['GET'])
def api_cnpj_get(cnpj):
    """API GET para consulta de CNPJ"""
    try:
        fonte = request.args.get('fonte', 'cnpja')
        
        if not cnpj:
            return jsonify({'erro': 'CNPJ é obrigatório'}), 400
        
        resultado = investigador.consultar_cnpj(cnpj, fonte)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API cnpj_get: {e}")
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
        
        # Se encontrou o banco, retorna com a chave 'banco'
        if "erro" not in resultado:
            return jsonify({"banco": resultado})
        else:
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


@app.route('/api/consultar/dados-pessoais', methods=['POST'])
def api_consultar_dados_pessoais():
    """API para consulta de dados pessoais por telefone"""
    try:
        data = request.get_json()
        telefone = data.get('telefone', '').strip()
        
        if not telefone:
            return jsonify({'erro': 'Telefone é obrigatório'}), 400
        
        resultado = investigador.consultar_dados_pessoais_telefone(telefone)
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_dados_pessoais: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/consultar/dados-pessoais-avancado', methods=['POST'])
def api_consultar_dados_pessoais_avancado():
    """API para consulta avançada de dados pessoais com cruzamento de informações"""
    try:
        data = request.get_json()
        telefone = data.get('telefone', '').strip()
        cpf = data.get('cpf', '').strip()
        nome = data.get('nome', '').strip()
        data_nascimento = data.get('data_nascimento', '').strip()
        
        # Pelo menos um campo deve ser preenchido
        if not any([telefone, cpf, nome, data_nascimento]):
            return jsonify({'erro': 'Pelo menos um campo deve ser preenchido'}), 400
        
        resultado = investigador.consultar_dados_pessoais_avancado(
            telefone=telefone,
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento
        )
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Erro na API consultar_dados_pessoais_avancado: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/dados-pessoais/<telefone>', methods=['GET'])
def api_dados_pessoais_get(telefone):
    """API GET para consulta de dados pessoais por telefone"""
    try:
        if not telefone:
            return jsonify({'success': False, 'error': 'Telefone é obrigatório'}), 400
        
        resultado = investigador.consultar_dados_pessoais_telefone(telefone)
        
        if "erro" not in resultado:
            return jsonify({'success': True, 'data': resultado})
        else:
            return jsonify({'success': False, 'error': resultado.get('erro', 'Erro desconhecido')}), 400
    
    except Exception as e:
        logger.error(f"Erro na API dados_pessoais GET: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/cache/clear', methods=['POST'])
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


# === NOVAS ROTAS PARA APIs GRATUITAS ===

@app.route('/api/free/cep/<cep>', methods=['GET'])
def api_free_cep(cep):
    """API gratuita para consulta de CEP usando BrasilAPI e ViaCEP"""
    try:
        if not cep:
            return jsonify({'success': False, 'error': 'CEP é obrigatório'}), 400
        
        # Consulta via BrasilAPI
        resultado_brasil = brasil_api.consultar_cep(cep)
        
        # Consulta via ViaCEP como backup
        resultado_viacep = viacep_client.consultar_cep(cep)
        
        return jsonify({
            'success': True,
            'data': {
                'brasilapi': resultado_brasil,
                'viacep': resultado_viacep,
                'timestamp': datetime.now().isoformat()
            }
        })
    
    except Exception as e:
        logger.error(f"Erro na API free CEP: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/free/cnpj/<cnpj>', methods=['GET'])
def api_free_cnpj(cnpj):
    """API gratuita para consulta de CNPJ usando BrasilAPI"""
    try:
        if not cnpj:
            return jsonify({'success': False, 'error': 'CNPJ é obrigatório'}), 400
        
        resultado = brasil_api.consultar_cnpj(cnpj)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Erro na API free CNPJ: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/free/ddd/<ddd>', methods=['GET'])
def api_free_ddd(ddd):
    """API gratuita para consulta de DDD usando BrasilAPI"""
    try:
        if not ddd:
            return jsonify({'success': False, 'error': 'DDD é obrigatório'}), 400
        
        resultado = brasil_api.consultar_ddd(ddd)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Erro na API free DDD: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/free/cpf/<cpf>', methods=['GET'])
def api_free_cpf(cpf):
    """API gratuita para validação de CPF"""
    try:
        if not cpf:
            return jsonify({'success': False, 'error': 'CPF é obrigatório'}), 400
        
        resultado = validar_cpf(cpf)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Erro na API free CPF: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/free/banco/<codigo>', methods=['GET'])
def api_free_banco(codigo):
    """API gratuita para consulta de banco usando BrasilAPI"""
    try:
        if not codigo:
            return jsonify({'success': False, 'error': 'Código do banco é obrigatório'}), 400
        
        resultado = brasil_api.consultar_banco(codigo)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Erro na API free Banco: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/free/endereco/<uf>/<cidade>/<logradouro>', methods=['GET'])
def api_free_endereco(uf, cidade, logradouro):
    """API gratuita para busca reversa de endereço usando ViaCEP"""
    try:
        if not all([uf, cidade, logradouro]):
            return jsonify({'success': False, 'error': 'UF, cidade e logradouro são obrigatórios'}), 400
        
        resultado = viacep_client.buscar_endereco(uf, cidade, logradouro)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Erro na API free Endereço: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/free/status', methods=['GET'])
def api_free_status():
    """Status das APIs gratuitas"""
    try:
        # Testa conectividade
        status_brasil = brasil_api.testar_conectividade()
        status_viacep = viacep_client.testar_conectividade()
        
        return jsonify({
            'success': True,
            'data': {
                'brasilapi': {
                    'status': 'online' if status_brasil.get('sucesso') else 'offline',
                    'teste': status_brasil
                },
                'viacep': {
                    'status': 'online' if status_viacep.get('sucesso') else 'offline',
                    'teste': status_viacep
                },
                'timestamp': datetime.now().isoformat(),
                'apis_disponiveis': [
                    'CEP (BrasilAPI + ViaCEP)',
                    'CNPJ (BrasilAPI)',
                    'DDD (BrasilAPI)',
                    'CPF (Validação Local)',
                    'Bancos (BrasilAPI)',
                    'Busca Endereço (ViaCEP)'
                ]
            }
        })
    
    except Exception as e:
        logger.error(f"Erro na API free Status: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


# ==================== ROTAS DIRECT DATA API ====================

@app.route('/api/directd/consultar-cpf', methods=['POST'])
def api_directd_consultar_cpf():
    """API para consulta de dados pessoais por CPF via Direct Data"""
    try:
        data = request.get_json()
        cpf = data.get('cpf', '').strip()
        
        if not cpf:
            return jsonify({'success': False, 'error': 'CPF é obrigatório'}), 400
        
        resultado = consultar_dados_pessoais_cpf(cpf)
        
        return jsonify({
            'success': resultado.get('success', False),
            'data': resultado if resultado.get('success') else None,
            'error': resultado.get('error') if not resultado.get('success') else None,
            'timestamp': datetime.now().isoformat(),
            'fonte': 'Direct Data API'
        })
    
    except Exception as e:
        logger.error(f"Erro na API Direct Data CPF: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/directd/consultar-nome', methods=['POST'])
def api_directd_consultar_nome():
    """API para consulta de dados pessoais por nome via Direct Data"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        sobrenome = data.get('sobrenome', '').strip()
        data_nascimento = data.get('data_nascimento', '').strip()
        
        if not nome or not sobrenome:
            return jsonify({'success': False, 'error': 'Nome e sobrenome são obrigatórios'}), 400
        
        resultado = consultar_dados_pessoais_nome(nome, sobrenome, data_nascimento)
        
        return jsonify({
            'success': resultado.get('success', False),
            'data': resultado if resultado.get('success') else None,
            'error': resultado.get('error') if not resultado.get('success') else None,
            'timestamp': datetime.now().isoformat(),
            'fonte': 'Direct Data API'
        })
    
    except Exception as e:
        logger.error(f"Erro na API Direct Data Nome: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


@app.route('/api/directd/status', methods=['GET'])
def api_directd_status():
    """Status da integração Direct Data"""
    try:
        status = verificar_directd_config()
        
        return jsonify({
            'success': True,
            'data': {
                'configurado': status.get('configurado', False),
                'status': status.get('status', status.get('erro', 'Status desconhecido')),
                'instrucoes': status.get('instrucoes', ''),
                'timestamp': datetime.now().isoformat()
            }
        })
    
    except Exception as e:
        logger.error(f"Erro na API Direct Data Status: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500


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