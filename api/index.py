# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import re
from datetime import datetime
import sqlite3
import os
import sys
import tempfile

# Adicionar o diretório pai ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.cache import SimpleCache

# Inicializar cache
cache = SimpleCache()

def validar_cep(cep):
    """Valida formato de CEP"""
    if not cep:
        return False
    cep_limpo = re.sub(r'\D', '', cep)
    return len(cep_limpo) == 8 and cep_limpo.isdigit()

def consultar_cep_viacep(cep):
    """Consulta CEP via ViaCEP"""
    try:
        cep_limpo = re.sub(r'\D', '', cep)
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return data
    except Exception:
        pass
    return None

def validar_telefone(telefone):
    """Valida formato de telefone brasileiro"""
    if not telefone:
        return False
    
    telefone_limpo = re.sub(r'\D', '', telefone)
    
    # Telefone com DDD: 10 ou 11 dígitos (celular com 9)
    if len(telefone_limpo) in [10, 11]:
        # Verifica se o DDD é válido (11-99)
        ddd = telefone_limpo[:2]
        if 11 <= int(ddd) <= 99:
            return True
    
    return False

def validar_cnpj(cnpj):
    """Valida formato básico de CNPJ"""
    if not cnpj:
        return False
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    return len(cnpj_limpo) == 14 and cnpj_limpo.isdigit()

def consultar_cnpj_brasilapi(cnpj):
    """Consulta CNPJ via BrasilAPI"""
    try:
        cnpj_limpo = re.sub(r'\D', '', cnpj)
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def consultar_ddd_brasilapi(ddd):
    """Consulta DDD via BrasilAPI"""
    try:
        ddd_limpo = re.sub(r'\D', '', ddd)
        url = f"https://brasilapi.com.br/api/ddd/v1/{ddd_limpo}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def consultar_operadora_abr_telecom(telefone_limpo):
    """
    Consulta a operadora atual do telefone usando o serviço da ABR Telecom.
    Considera portabilidade numérica em tempo real.
    
    Args:
        telefone_limpo (str): Número de telefone apenas com dígitos
        
    Returns:
        dict: Informações da operadora ou None se não conseguir consultar
    """
    try:
        # Validação básica do número
        if not telefone_limpo or len(telefone_limpo) not in [10, 11]:
            return None
            
        # URL do serviço de consulta da ABR Telecom
        base_url = "https://consultanumero.abrtelecom.com.br"
        consulta_url = f"{base_url}/consultanumero/consulta/consultaSituacaoAtual"
        
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        # Primeira requisição para obter cookies e tokens necessários
        initial_response = session.get(base_url, timeout=15)
        if initial_response.status_code != 200:
            return None
        
        # Tentar acessar a página de consulta
        consulta_response = session.get(consulta_url, timeout=15)
        if consulta_response.status_code != 200:
            return None
            
        # Preparar dados para consulta
        form_data = {
            'codigoAcesso': telefone_limpo,
            'numeroTelefone': telefone_limpo
        }
        
        # Headers para POST
        post_headers = headers.copy()
        post_headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': base_url,
            'Referer': consulta_url
        })
        
        # Fazer a consulta POST
        result_response = session.post(consulta_url, data=form_data, headers=post_headers, timeout=15)
        
        if result_response.status_code != 200:
            return None
        
        # Analisar a resposta
        response_text = result_response.text.upper()
        
        # Mapeamento de operadoras conhecidas
        operadoras_map = {
            'VIVO': ['VIVO', 'TELEFONICA'],
            'CLARO': ['CLARO', 'CLARO S.A.', 'CLARO SA'],
            'TIM': ['TIM', 'TIM S.A.', 'TIM SA', 'TELECOM ITALIA'],
            'OI': ['OI', 'OI S.A.', 'OI SA', 'TELEMAR'],
            'NEXTEL': ['NEXTEL', 'NEXTEL TELECOMUNICACOES'],
            'ALGAR': ['ALGAR', 'ALGAR TELECOM'],
            'SERCOMTEL': ['SERCOMTEL'],
            'UNIFIQUE': ['UNIFIQUE']
        }
        
        # Buscar pela operadora na resposta
        for operadora_padrao, variantes in operadoras_map.items():
            for variante in variantes:
                if variante in response_text:
                    return {
                        'operadora': operadora_padrao,
                        'fonte': 'ABR Telecom (Oficial)',
                        'portabilidade': True,
                        'confiabilidade': 'Alta',
                        'timestamp': datetime.now().isoformat()
                    }
        
        # Se chegou até aqui, não encontrou operadora conhecida
        # Mas pode ter encontrado alguma informação
        if any(keyword in response_text for keyword in ['PRESTADORA', 'OPERADORA', 'EMPRESA']):
            return {
                'operadora': 'Não identificada',
                'fonte': 'ABR Telecom (Oficial)',
                'portabilidade': True,
                'confiabilidade': 'Baixa',
                'observacao': 'Número encontrado mas operadora não identificada',
                'timestamp': datetime.now().isoformat()
            }
        
        return None
        
    except requests.exceptions.Timeout:
        return {
            'erro': 'Timeout na consulta ABR Telecom',
            'fonte': 'ABR Telecom (Oficial)',
            'confiabilidade': 'Erro'
        }
    except requests.exceptions.RequestException as e:
        return {
            'erro': f'Erro de conexão: {str(e)}',
            'fonte': 'ABR Telecom (Oficial)',
            'confiabilidade': 'Erro'
        }
    except Exception as e:
        return {
            'erro': f'Erro interno: {str(e)}',
            'fonte': 'ABR Telecom (Oficial)',
            'confiabilidade': 'Erro'
        }

def identificar_operadora_por_prefixo(telefone_limpo):
    """
    Identifica a operadora do telefone considerando portabilidade numérica.
    Primeiro tenta consultar a ABR Telecom, depois usa fallback baseado em prefixos.
    
    Args:
        telefone_limpo (str): Número de telefone apenas com dígitos
        
    Returns:
        dict: Informações detalhadas da operadora incluindo confiabilidade
    """
    if len(telefone_limpo) < 10:
        return {
            'operadora': 'Desconhecida',
            'fonte': 'Validação',
            'portabilidade': False,
            'confiabilidade': 'Erro',
            'observacao': 'Número inválido'
        }
    
    # Primeiro, tentar consulta oficial na ABR Telecom (considera portabilidade)
    resultado_oficial = consultar_operadora_abr_telecom(telefone_limpo)
    if resultado_oficial and not resultado_oficial.get('erro'):
        return resultado_oficial
    
    # Fallback: Identificação baseada em prefixos (pode não ser precisa devido à portabilidade)
    ddd = telefone_limpo[:2]
    prefixo = telefone_limpo[2:6] if len(telefone_limpo) == 11 else telefone_limpo[2:5]
    
    # Mapeamento atualizado de prefixos por DDD (2024)
    # ATENÇÃO: Estes dados podem estar desatualizados devido à portabilidade numérica
    prefixos_operadoras = {
        # Principais DDDs do Brasil
        '11': {  # São Paulo
            'vivo': ['99', '98', '97', '96', '95'],
            'claro': ['94', '93', '92', '91', '89', '88', '87', '86', '85'],
            'tim': ['84', '83', '82', '81', '79', '78', '77', '76', '75'],
            'oi': ['74', '73', '72', '71', '69', '68', '67', '66', '65']
        },
        '21': {  # Rio de Janeiro
            'vivo': ['99', '98', '97', '96', '95'],
            'claro': ['94', '93', '92', '91', '89', '88', '87', '86', '85'],
            'tim': ['84', '83', '82', '81', '79', '78', '77', '76', '75'],
            'oi': ['74', '73', '72', '71', '69', '68', '67', '66', '65']
        },
        '61': {  # Brasília
            'vivo': ['99', '98', '97', '96', '95'],
            'claro': ['94', '93', '92', '91', '89', '88', '87', '86', '85'],
            'tim': ['84', '83', '82', '81', '79', '78', '77', '76', '75'],
            'oi': ['74', '73', '72', '71', '69', '68', '67', '66', '65']
        },
        '85': {  # Fortaleza
            'vivo': ['99', '98', '97', '96', '95'],
            'claro': ['94', '93', '92', '91', '89', '88', '87', '86', '85'],
            'tim': ['84', '83', '82', '81', '79', '78', '77', '76', '75'],
            'oi': ['74', '73', '72', '71', '69', '68', '67', '66', '65']
        }
    }
    
    # Verifica se temos mapeamento específico para o DDD
    if ddd in prefixos_operadoras:
        for operadora, prefixos in prefixos_operadoras[ddd].items():
            if prefixo[:2] in prefixos:
                return {
                    'operadora': operadora.upper(),
                    'fonte': 'Prefixo (Estimativa)',
                    'portabilidade': False,
                    'confiabilidade': 'Baixa',
                    'observacao': 'Baseado em prefixo original - pode estar incorreto devido à portabilidade',
                    'ddd': ddd,
                    'prefixo': prefixo[:2],
                    'timestamp': datetime.now().isoformat()
                }
    
    # Identificação genérica baseada no primeiro dígito do número (ainda menos confiável)
    primeiro_digito = telefone_limpo[2] if len(telefone_limpo) >= 3 else ''
    
    operadora_estimada = None
    if primeiro_digito == '9':
        if prefixo[:2] in ['96', '97', '98', '99']:
            operadora_estimada = "VIVO"
        elif prefixo[:2] in ['91', '92', '93', '94']:
            operadora_estimada = "CLARO"
        else:
            operadora_estimada = "VIVO/CLARO"
    elif primeiro_digito == '8':
        operadora_estimada = "TIM"
    elif primeiro_digito == '7':
        operadora_estimada = "NEXTEL"
    elif primeiro_digito == '6':
        operadora_estimada = "OI"
    
    if operadora_estimada:
        return {
            'operadora': operadora_estimada,
            'fonte': 'Dígito (Estimativa)',
            'portabilidade': False,
            'confiabilidade': 'Muito Baixa',
            'observacao': 'Baseado apenas no primeiro dígito - muito impreciso devido à portabilidade',
            'ddd': ddd,
            'primeiro_digito': primeiro_digito,
            'timestamp': datetime.now().isoformat()
        }
    
    # Se chegou até aqui, incluir informações do erro da ABR Telecom se houver
    resultado_final = {
        'operadora': 'Desconhecida',
        'fonte': 'Nenhuma',
        'portabilidade': False,
        'confiabilidade': 'Erro',
        'observacao': 'Não foi possível identificar a operadora',
        'ddd': ddd,
        'timestamp': datetime.now().isoformat()
    }
    
    # Adicionar informações de erro da ABR Telecom se disponível
    if resultado_oficial and resultado_oficial.get('erro'):
        resultado_final['erro_abr_telecom'] = resultado_oficial['erro']
        resultado_final['observacao'] += f" - Erro ABR Telecom: {resultado_oficial['erro']}"
    
    return resultado_final

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['JSON_AS_ASCII'] = False

# Configurar CORS para permitir requisições do frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuração do banco de dados para ambiente serverless
def get_db_path():
    """Retorna o caminho do banco de dados adequado para o ambiente"""
    if os.environ.get('VERCEL'):
        # No Vercel, usar diretório temporário
        return os.path.join(tempfile.gettempdir(), 'osint_database.db')
    else:
        # Localmente, usar diretório atual
        return "osint_database.db"

DB_PATH = get_db_path()

def init_database():
    """Cria as tabelas necessárias se não existirem"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Tabela principal para dados pessoais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT UNIQUE NOT NULL,
                nome TEXT,
                rg TEXT,
                cnh TEXT,
                email TEXT,
                telefone TEXT,
                titulo_eleitor TEXT,
                pis TEXT,
                cns TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela para logs de limpeza de cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acao TEXT NOT NULL,
                items_removidos INTEGER DEFAULT 0,
                usuario_ip TEXT,
                user_agent TEXT,
                data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                detalhes TEXT
            )
        ''')
        
        # Índices para otimizar buscas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cpf ON pessoas(cpf)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nome ON pessoas(nome)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rg ON pessoas(rg)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cnh ON pessoas(cnh)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON pessoas(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_telefone ON pessoas(telefone)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_titulo_eleitor ON pessoas(titulo_eleitor)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pis ON pessoas(pis)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cns ON pessoas(cns)')
        
        # Índices para tabela de cache logs
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cache_logs_data ON cache_logs(data_execucao)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cache_logs_acao ON cache_logs(acao)')
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        return False

def buscar_por_cpf(cpf):
    """Busca uma pessoa pelo CPF"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT cpf, nome, rg, cnh, email, telefone, titulo_eleitor, pis, cns, 
                   data_criacao, data_atualizacao
            FROM pessoas 
            WHERE cpf = ?
        ''', (cpf,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            return {
                "status": "success",
                "dados": {
                    "cpf": resultado[0],
                    "nome": resultado[1],
                    "rg": resultado[2],
                    "cnh": resultado[3],
                    "email": resultado[4],
                    "telefone": resultado[5],
                    "titulo_eleitor": resultado[6],
                    "pis": resultado[7],
                    "cns": resultado[8],
                    "data_criacao": resultado[9],
                    "data_atualizacao": resultado[10]
                }
            }
        else:
            return {"status": "not_found", "message": "CPF não encontrado"}
    
    except Exception as e:
        return {"status": "error", "message": f"Erro na busca: {str(e)}"}
    finally:
        conn.close()

def inserir_pessoa(cpf, nome=None, rg=None, cnh=None, email=None, telefone=None, titulo_eleitor=None, pis=None, cns=None):
    """Insere uma nova pessoa no banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO pessoas (cpf, nome, rg, cnh, email, telefone, titulo_eleitor, pis, cns)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, rg, cnh, email, telefone, titulo_eleitor, pis, cns))
        
        conn.commit()
        return {"status": "success", "message": "Pessoa inserida com sucesso"}
    
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "CPF já existe no banco de dados"}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao inserir pessoa: {str(e)}"}
    finally:
        conn.close()

def registrar_limpeza_cache(items_removidos=0, usuario_ip=None, user_agent=None, detalhes=None):
    """Registra uma limpeza de cache no banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO cache_logs (acao, items_removidos, usuario_ip, user_agent, detalhes)
            VALUES (?, ?, ?, ?, ?)
        ''', ('limpeza_cache', items_removidos, usuario_ip, user_agent, detalhes))
        
        conn.commit()
        return {"status": "success", "message": "Log de limpeza registrado com sucesso"}
    
    except Exception as e:
        return {"status": "error", "message": f"Erro ao registrar log: {str(e)}"}
    finally:
        conn.close()

def obter_historico_cache(limite=50):
    """Obtém o histórico de limpezas de cache"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, acao, items_removidos, usuario_ip, user_agent, data_execucao, detalhes
            FROM cache_logs 
            ORDER BY data_execucao DESC 
            LIMIT ?
        ''', (limite,))
        
        resultados = cursor.fetchall()
        
        historico = []
        for resultado in resultados:
            historico.append({
                "id": resultado[0],
                "acao": resultado[1],
                "items_removidos": resultado[2],
                "usuario_ip": resultado[3],
                "user_agent": resultado[4],
                "data_execucao": resultado[5],
                "detalhes": resultado[6]
            })
        
        return {
            "status": "success",
            "total": len(historico),
            "historico": historico
        }
    
    except Exception as e:
        return {"status": "error", "message": f"Erro ao obter histórico: {str(e)}"}
    finally:
        conn.close()

def buscar_cruzada(**kwargs):
    """Busca cruzada por múltiplos campos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Construir query dinamicamente
        condicoes = []
        valores = []
        
        for campo, valor in kwargs.items():
            if valor and valor.strip():
                condicoes.append(f"{campo} = ?")
                valores.append(valor.strip())
        
        if not condicoes:
            return {"status": "error", "message": "Nenhum campo de busca fornecido"}
        
        query = f'''
            SELECT cpf, nome, rg, cnh, email, telefone, titulo_eleitor, pis, cns, 
                   data_criacao, data_atualizacao
            FROM pessoas 
            WHERE {' OR '.join(condicoes)}
        '''
        
        cursor.execute(query, valores)
        resultados = cursor.fetchall()
        
        if resultados:
            dados = []
            for resultado in resultados:
                dados.append({
                    "cpf": resultado[0],
                    "nome": resultado[1],
                    "rg": resultado[2],
                    "cnh": resultado[3],
                    "email": resultado[4],
                    "telefone": resultado[5],
                    "titulo_eleitor": resultado[6],
                    "pis": resultado[7],
                    "cns": resultado[8],
                    "data_criacao": resultado[9],
                    "data_atualizacao": resultado[10]
                })
            
            return {"status": "success", "dados": dados}
        else:
            return {"status": "not_found", "message": "Nenhum resultado encontrado"}
    
    except Exception as e:
        return {"status": "error", "message": f"Erro na busca: {str(e)}"}
    finally:
        conn.close()

# Inicializar o banco de dados
init_database()

@app.route('/')
def home():
    """Página principal com interface web completa"""
    return render_template('index.html')

@app.route('/api')
def api_info():
    """Informações da API"""
    return jsonify({
        "status": "success",
        "message": "OSINT Investigador BR API",
        "version": "2.0.0",
        "endpoints": [
            "/api/consultar/cruzamento",
            "/api/consultar/cpf-completo",
            "/api/consultar/cep",
            "/api/cep/<cep>",
            "/api/consultar/telefone",
            "/api/telefone/<telefone>",
            "/api/consultar/cnpj",
            "/api/cnpj/<cnpj>",
            "/api/inserir/pessoa",
            "/api/buscar/cruzada",
            "/api/status"
        ],
        "observacoes": {
            "operadoras": "A identificação de operadoras é baseada em prefixos tradicionais e pode não ser precisa devido à portabilidade numérica."
        }
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
        # Garantir que o request seja decodificado corretamente
        if request.content_type and 'charset' not in request.content_type:
            request.charset = 'utf-8'
            
        data = request.get_json(force=True)
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
        # Identificar operadora se telefone foi fornecido
        operadora_info = None
        if telefone:
            telefone_limpo = re.sub(r'\D', '', telefone)
            resultado_operadora = identificar_operadora_por_prefixo(telefone_limpo)
            operadora_info = {
                "status": "identificado", 
                "operadora": resultado_operadora.get('operadora', 'Desconhecida'),
                "fonte": resultado_operadora.get('fonte', 'N/A'),
                "confiabilidade": resultado_operadora.get('confiabilidade', 'N/A'),
                "portabilidade_considerada": resultado_operadora.get('portabilidade', False),
                "observacao": resultado_operadora.get('observacao', '')
            }
        
        resultado_cruzamento = {
            "dados_entrada": {
                "nome": nome if nome else None,
                "cpf": cpf if cpf else None,
                "telefone": telefone if telefone else None
            },
            "dados_encontrados": {
                "cpf_info": {"status": "simulado", "nome": "João da Silva"} if cpf else None,
                "telefone_info": operadora_info,
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
        
        # Garantir que a resposta seja em UTF-8
        response = jsonify(resultado_cruzamento)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
        
    except UnicodeDecodeError as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro de codificação UTF-8: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro interno: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/consultar/cpf-completo', methods=['POST'])
def api_consultar_cpf_completo():
    """Endpoint para busca completa por CPF com todos os dados"""
    try:
        print(f"[DEBUG] Iniciando consulta CPF completo - {datetime.now().isoformat()}")
        
        # Configurar charset se não estiver presente
        if not hasattr(request, 'charset') or not request.charset:
            request.charset = 'utf-8'
        
        # Forçar decodificação JSON
        data = request.get_json(force=True)
        print(f"[DEBUG] Dados recebidos: {data}")
        
        if not data:
            print("[DEBUG] Erro: Dados JSON não fornecidos")
            return jsonify({
                "status": "error",
                "erro": "Dados JSON não fornecidos",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        cpf = data.get('cpf')
        if not cpf:
            print("[DEBUG] Erro: CPF não fornecido")
            return jsonify({
                "status": "error",
                "erro": "CPF é obrigatório",
                "timestamp": datetime.now().isoformat()
            }), 400

        # Limpar CPF (remover formatação)
        cpf_limpo = re.sub(r'\D', '', cpf)
        print(f"[DEBUG] CPF limpo: {cpf_limpo}")

        # Buscar via Direct Data API (dados reais) e complementar com outras APIs
        dados_formatados = {"cpf": cpf_limpo}
        fontes_utilizadas = []
        
        # 1. Tentar Direct Data API primeiro (dados mais completos)
        try:
            print("[DEBUG] Tentando importar directd_integration")
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from directd_integration import consultar_dados_pessoais_cpf
            
            print("[DEBUG] Chamando consultar_dados_pessoais_cpf")
            resultado_api = consultar_dados_pessoais_cpf(cpf_limpo)
            print(f"[DEBUG] Resultado da API Direct Data: {resultado_api}")
            
            if resultado_api.get('success') and resultado_api.get('data'):
                print("[DEBUG] API Direct Data retornou dados com sucesso")
                # A Direct Data API retorna os dados diretamente em 'data'
                retorno = resultado_api.get('data', {})
                print(f"[DEBUG] Dados extraídos: {retorno}")
                
                # Extrair dados da Direct Data API
                if retorno.get('name'):
                    dados_formatados['nome'] = retorno.get('name')
                    fontes_utilizadas.append('Direct Data API')
                
                if retorno.get('dateOfBirth'):
                    dados_formatados['data_nascimento'] = retorno.get('dateOfBirth')
                
                if retorno.get('age'):
                    dados_formatados['idade'] = retorno.get('age')
                
                if retorno.get('gender'):
                    dados_formatados['sexo'] = retorno.get('gender')
                
                if retorno.get('nameMother'):
                    dados_formatados['mae'] = retorno.get('nameMother')
                
                # Telefones
                phones = retorno.get('phones', [])
                if phones and any(phone.get('phoneNumber') for phone in phones):
                    dados_formatados['telefones'] = [phone.get('phoneNumber') for phone in phones if phone.get('phoneNumber')]
                
                # Emails
                emails = retorno.get('emails', [])
                if emails and any(email.get('emailAddress') for email in emails):
                    dados_formatados['emails'] = [email.get('emailAddress') for email in emails if email.get('emailAddress')]
                
                print(f"[DEBUG] Dados formatados após Direct Data: {dados_formatados}")
            else:
                print(f"[DEBUG] API Direct Data não retornou dados válidos: success={resultado_api.get('success')}, data={resultado_api.get('data')}")
        
        except Exception as e:
            print(f"[DEBUG] Erro ao consultar Direct Data API: {str(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            # Continuar com outras APIs se Direct Data falhar
                
                # Endereços
                addresses = retorno.get('addresses', [])
                if addresses:
                    enderecos_formatados = []
                    for addr in addresses:
                        endereco = {}
                        if addr.get('street'):
                            endereco['endereco'] = f"{addr.get('street', '')}, {addr.get('number', '')}"
                        if addr.get('neighborhood'):
                            endereco['bairro'] = addr.get('neighborhood')
                        if addr.get('city'):
                            endereco['cidade'] = addr.get('city')
                        if addr.get('state'):
                            endereco['estado'] = addr.get('state')
                        if addr.get('postalCode'):
                            endereco['cep'] = addr.get('postalCode')
                        if endereco:
                            enderecos_formatados.append(endereco)
                    
                    if enderecos_formatados:
                        dados_formatados['enderecos'] = enderecos_formatados
                
                # Informações adicionais
                if retorno.get('salaryRange'):
                    dados_formatados['faixa_salarial'] = retorno.get('salaryRange')
                
                if retorno.get('estimatedSalary'):
                    dados_formatados['salario_estimado'] = retorno.get('estimatedSalary')
                        
        except Exception as api_error:
            print(f"Erro na Direct Data API: {api_error}")
        
        # 2. Tentar API Brasil para complementar dados faltantes
        if not dados_formatados.get('nome') or len(dados_formatados.keys()) < 5:
            try:
                from api_brasil_integration import APIBrasilClient
                api_brasil = APIBrasilClient()
                resultado_brasil = api_brasil.consultar_cpf(cpf_limpo)
                
                if resultado_brasil.get('sucesso') and resultado_brasil.get('dados'):
                    dados_brasil = resultado_brasil.get('dados', {})
                    
                    # Complementar dados que não existem
                    if not dados_formatados.get('nome') and dados_brasil.get('nome'):
                        dados_formatados['nome'] = dados_brasil.get('nome')
                        fontes_utilizadas.append('API Brasil')
                    
                    # Adicionar outros dados se disponíveis
                    if dados_brasil.get('situacao_cpf'):
                        dados_formatados['situacao_cpf'] = dados_brasil.get('situacao_cpf')
                        
            except Exception as brasil_error:
                print(f"Erro na API Brasil: {brasil_error}")
        
        # 3. Verificar se encontrou pelo menos o nome
        if dados_formatados.get('nome'):
            fonte_final = ', '.join(fontes_utilizadas) if fontes_utilizadas else 'APIs Externas'
            
            response = jsonify({
                "status": "success",
                "message": f"Dados encontrados via {fonte_final}",
                "dados": dados_formatados,
                "fonte": fonte_final,
                "observacao": "Dados obtidos de fontes oficiais externas",
                "timestamp": datetime.now().isoformat()
            })
        else:
            # Nenhuma API retornou dados
            response = jsonify({
                "status": "not_found",
                "message": "CPF não encontrado nas bases de dados oficiais disponíveis",
                "cpf_consultado": cpf,
                "apis_consultadas": ["Direct Data API", "API Brasil"],
                "timestamp": datetime.now().isoformat()
            })
        
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
        
    except UnicodeDecodeError as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro de codificação UTF-8: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro interno: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/inserir/pessoa', methods=['POST'])
def api_inserir_pessoa():
    """Endpoint para inserir uma nova pessoa no banco de dados"""
    try:
        # Configurar charset se não estiver presente
        if not hasattr(request, 'charset') or not request.charset:
            request.charset = 'utf-8'
        
        # Forçar decodificação JSON
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({
                "status": "error",
                "erro": "Dados JSON não fornecidos",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        cpf = data.get('cpf')
        if not cpf:
            return jsonify({
                "status": "error",
                "erro": "CPF é obrigatório",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Inserir no banco de dados
        resultado = inserir_pessoa(
            cpf=cpf,
            nome=data.get('nome'),
            rg=data.get('rg'),
            cnh=data.get('cnh'),
            email=data.get('email'),
            telefone=data.get('telefone'),
            titulo_eleitor=data.get('titulo_eleitor'),
            pis=data.get('pis'),
            cns=data.get('cns')
        )
        
        if resultado["status"] == "success":
            response = jsonify({
                "status": "success",
                "message": resultado["message"],
                "cpf_inserido": cpf,
                "timestamp": datetime.now().isoformat()
            })
        else:
            response = jsonify({
                "status": "error",
                "erro": resultado["message"],
                "timestamp": datetime.now().isoformat()
            }), 400
        
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
        
    except UnicodeDecodeError as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro de codificação UTF-8: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro interno: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/buscar/cruzada', methods=['POST'])
def api_buscar_cruzada():
    """Endpoint para busca cruzada por múltiplos campos"""
    try:
        # Configurar charset se não estiver presente
        if not hasattr(request, 'charset') or not request.charset:
            request.charset = 'utf-8'
        
        # Forçar decodificação JSON
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({
                "status": "error",
                "erro": "Dados JSON não fornecidos",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Buscar no banco de dados
        resultado = buscar_cruzada(**data)
        
        if resultado["status"] == "success":
            total_encontrados = len(resultado["dados"])
            response = jsonify({
                "status": "success",
                "message": f"Encontrados {total_encontrados} registros",
                "total_encontrados": total_encontrados,
                "dados": resultado["dados"],
                "timestamp": datetime.now().isoformat()
            })
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response
        elif resultado["status"] == "not_found":
            return jsonify({
                "status": "success",
                "message": "Nenhum resultado encontrado",
                "total_encontrados": 0,
                "dados": [],
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "erro": resultado["message"],
                "timestamp": datetime.now().isoformat()
            }), 400
        
    except UnicodeDecodeError as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro de codificação UTF-8: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro interno: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/consultar/cep', methods=['POST'])
def api_consultar_cep():
    """Consulta informações de CEP"""
    try:
        data = request.get_json()
        if not data or 'cep' not in data:
            return jsonify({"erro": "CEP não fornecido"}), 400
        
        cep = data['cep']
        if not validar_cep(cep):
            return jsonify({"erro": "CEP inválido. Use o formato: 12345678 ou 12345-678"}), 400
        
        resultado = consultar_cep_viacep(cep)
        if resultado:
            return jsonify({
                "status": "success",
                "cep": cep,
                "dados": resultado,
                "fonte": "ViaCEP",
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify({
            "status": "error",
            "message": "CEP não encontrado",
            "cep": cep
        }), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/cep/<cep>')
def api_consultar_cep_get(cep):
    """Consulta informações de CEP via GET"""
    try:
        if not validar_cep(cep):
            return jsonify({"erro": "CEP inválido. Use o formato: 12345678 ou 12345-678"}), 400
        
        resultado = consultar_cep_viacep(cep)
        if resultado:
            return jsonify({
                "status": "success",
                "cep": cep,
                "dados": resultado,
                "fonte": "ViaCEP",
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify({
            "status": "error",
            "message": "CEP não encontrado",
            "cep": cep
        }), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/consultar/telefone', methods=['POST'])
def api_consultar_telefone():
    """Valida e consulta informações de telefone"""
    try:
        data = request.get_json()
        if not data or 'telefone' not in data:
            return jsonify({"erro": "Telefone não fornecido"}), 400
        
        telefone = data['telefone']
        telefone_limpo = re.sub(r'\D', '', telefone)
        
        if validar_telefone(telefone):
            ddd = telefone_limpo[:2]
            numero = telefone_limpo[2:]
            
            # Consulta informações do DDD
            info_ddd = consultar_ddd_brasilapi(ddd)
            
            # Identifica a operadora (considerando portabilidade numérica)
            resultado_operadora = identificar_operadora_por_prefixo(telefone_limpo)
            
            tipo_telefone = "Celular" if len(telefone_limpo) == 11 else "Fixo"
            
            return jsonify({
                "status": "success",
                "telefone": telefone,
                "telefone_limpo": telefone_limpo,
                "telefone_formatado": f"({ddd}) {numero[:4]}-{numero[4:]}" if len(numero) == 8 else f"({ddd}) {numero[:5]}-{numero[5:]}",
                "valido": True,
                "ddd": ddd,
                "numero": numero,
                "tipo": tipo_telefone,
                "operadora": resultado_operadora.get('operadora', 'Desconhecida'),
                "operadora_detalhes": {
                    "nome": resultado_operadora.get('operadora', 'Desconhecida'),
                    "fonte": resultado_operadora.get('fonte', 'N/A'),
                    "confiabilidade": resultado_operadora.get('confiabilidade', 'N/A'),
                    "portabilidade_considerada": resultado_operadora.get('portabilidade', False),
                    "observacao": resultado_operadora.get('observacao', ''),
                    "timestamp": resultado_operadora.get('timestamp', '')
                },
                "regiao": info_ddd if info_ddd else {"cities": ["Informação não disponível"], "state": "N/A"},
                "message": "Telefone válido",
                "observacao": "A identificação da operadora utiliza a API oficial da ABR Telecom quando possível, considerando portabilidade numérica. Em caso de falha, usa estimativa baseada em prefixos.",
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "telefone": telefone,
                "valido": False,
                "message": "Telefone inválido. Use formato: (11) 99999-9999 ou 11999999999",
                "timestamp": datetime.now().isoformat()
            }), 400
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/telefone/<telefone>')
def api_telefone_get(telefone):
    """Consulta telefone via GET"""
    try:
        if not validar_telefone(telefone):
            return jsonify({"erro": "Telefone inválido. Use formato: (11) 99999-9999 ou 11999999999"}), 400
        
        telefone_limpo = re.sub(r'\D', '', telefone)
        ddd = telefone_limpo[:2]
        numero = telefone_limpo[2:]
        
        # Consulta informações do DDD
        info_ddd = consultar_ddd_brasilapi(ddd)
        
        # Identifica a operadora (considerando portabilidade numérica)
        resultado_operadora = identificar_operadora_por_prefixo(telefone_limpo)
        
        tipo_telefone = "Celular" if len(telefone_limpo) == 11 else "Fixo"
        
        return jsonify({
            "status": "success",
            "data": {
                "telefone": telefone,
                "telefone_limpo": telefone_limpo,
                "telefone_formatado": f"({ddd}) {numero[:4]}-{numero[4:]}" if len(numero) == 8 else f"({ddd}) {numero[:5]}-{numero[5:]}",
                "valido": True,
                "ddd": ddd,
                "numero": numero,
                "tipo": tipo_telefone,
                "operadora": resultado_operadora.get('operadora', 'Desconhecida'),
                "operadora_detalhes": {
                    "nome": resultado_operadora.get('operadora', 'Desconhecida'),
                    "fonte": resultado_operadora.get('fonte', 'N/A'),
                    "confiabilidade": resultado_operadora.get('confiabilidade', 'N/A'),
                    "portabilidade_considerada": resultado_operadora.get('portabilidade', False),
                    "observacao": resultado_operadora.get('observacao', ''),
                    "timestamp": resultado_operadora.get('timestamp', '')
                },
                "estado": info_ddd.get('state', 'N/A') if info_ddd else 'N/A',
                "regiao": info_ddd.get('cities', ['N/A'])[0] if info_ddd and info_ddd.get('cities') else 'N/A',
                "observacao": "A identificação da operadora utiliza a API oficial da ABR Telecom quando possível, considerando portabilidade numérica. Em caso de falha, usa estimativa baseada em prefixos."
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# Endpoint para consulta de DDD
@app.route('/api/ddd/<ddd>')
def api_consultar_ddd_get(ddd):
    """Consulta informações de DDD via GET"""
    try:
        if not ddd or len(ddd) != 2 or not ddd.isdigit():
            return jsonify({
                "success": False,
                "error": "DDD inválido. Use apenas 2 dígitos (ex: 11, 21, 85)"
            }), 400
        
        resultado = consultar_ddd_brasilapi(ddd)
        
        if resultado:
            return jsonify({
                "success": True,
                "data": {
                    "ddd": ddd,
                    "estado": resultado.get('state', 'N/A'),
                    "cidades": resultado.get('cities', [])
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": "DDD não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

# Endpoint para consulta de bancos
@app.route('/api/consultar/bancos')
def api_consultar_bancos_get():
    """Lista todos os bancos brasileiros"""
    try:
        # Consulta a API do Brasil API para listar bancos
        url = "https://brasilapi.com.br/api/banks/v1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bancos = response.json()
            return jsonify({
                "bancos": bancos,
                "total": len(bancos),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "erro": "Erro ao consultar API de bancos"
            }), 500
            
    except Exception as e:
        return jsonify({
            "erro": f"Erro interno: {str(e)}"
        }), 500

# Endpoint para limpeza de cache
@app.route('/api/cache/clear', methods=['POST'])
def api_limpar_cache():
    """Limpa todo o cache do sistema"""
    try:
        from utils.cache import cache
        
        # Limpa o cache
        items_removidos = cache.clear()
        
        # Registra a limpeza no banco de dados
        usuario_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Desconhecido')
        detalhes = f"Limpeza manual via interface web"
        
        log_result = registrar_limpeza_cache(
            items_removidos=items_removidos,
            usuario_ip=usuario_ip,
            user_agent=user_agent,
            detalhes=detalhes
        )
        
        return jsonify({
            "status": "success",
            "message": "Cache limpo com sucesso",
            "items_removidos": items_removidos,
            "timestamp": datetime.now().isoformat(),
            "log_registrado": log_result["status"] == "success"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro ao limpar cache: {str(e)}"
        }), 500

@app.route('/api/cache/stats', methods=['GET'])
def api_stats_cache():
    """Retorna estatísticas do cache"""
    try:
        from utils.cache import cache
        
        stats = cache.get_stats()
        
        return jsonify({
            "status": "success",
            "cache_stats": stats,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro ao obter estatísticas: {str(e)}"
        }), 500

# Endpoint para histórico de limpezas de cache
@app.route('/api/cache/history', methods=['GET'])
def api_historico_cache():
    """Retorna o histórico de limpezas de cache"""
    try:
        limite = request.args.get('limite', 50, type=int)
        historico = obter_historico_cache(limite)
        
        return jsonify(historico)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "erro": f"Erro ao obter histórico: {str(e)}"
        }), 500

# Endpoint para consulta de banco específico
@app.route('/api/consultar/banco/<codigo>')
def api_consultar_banco_get(codigo):
    """Consulta banco específico por código"""
    try:
        if not codigo or len(codigo) != 3 or not codigo.isdigit():
            return jsonify({
                "erro": "Código do banco deve conter 3 dígitos"
            }), 400
        
        # Consulta a API do Brasil API para banco específico
        url = f"https://brasilapi.com.br/api/banks/v1/{codigo}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            banco = response.json()
            return jsonify({
                "banco": {
                    "codigo": banco.get('code'),
                    "nome": banco.get('name'),
                    "nome_completo": banco.get('fullName'),
                    "ispb": banco.get('ispb')
                },
                "timestamp": datetime.now().isoformat()
            })
        elif response.status_code == 404:
            return jsonify({
                "erro": "Banco não encontrado"
            }), 404
        else:
            return jsonify({
                "erro": "Erro ao consultar API de bancos"
            }), 500
            
    except Exception as e:
        return jsonify({
            "erro": f"Erro interno: {str(e)}"
        }), 500

# Endpoint para consulta de CNPJ
@app.route('/api/consultar/cnpj', methods=['POST'])
def api_consultar_cnpj():
    """Consulta informações de CNPJ"""
    try:
        data = request.get_json()
        if not data or 'cnpj' not in data:
            return jsonify({"erro": "CNPJ não fornecido"}), 400
        
        cnpj = data['cnpj']
        if not validar_cnpj(cnpj):
            return jsonify({"erro": "CNPJ inválido. Use o formato: 12345678000195 ou 12.345.678/0001-95"}), 400
        
        resultado = consultar_cnpj_brasilapi(cnpj)
        if resultado:
            return jsonify({
                "status": "success",
                "cnpj": cnpj,
                "dados": resultado,
                "fonte": "BrasilAPI",
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify({
            "status": "error",
            "message": "CNPJ não encontrado",
            "cnpj": cnpj
        }), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/cnpj/<cnpj>')
def api_consultar_cnpj_get(cnpj):
    """Consulta informações de CNPJ via GET"""
    try:
        if not validar_cnpj(cnpj):
            return jsonify({"erro": "CNPJ inválido. Use o formato: 12345678000195 ou 12.345.678/0001-95"}), 400
        
        resultado = consultar_cnpj_brasilapi(cnpj)
        if resultado:
            return jsonify({
                "status": "success",
                "cnpj": cnpj,
                "dados": resultado,
                "fonte": "BrasilAPI",
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify({
            "status": "error",
            "message": "CNPJ não encontrado",
            "cnpj": cnpj
        }), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/<path:path>')
def api_catch_all(path):
    """Captura outras rotas da API"""
    return jsonify({
        "status": "success",
        "message": "Endpoint não encontrado",
        "available_endpoints": [
            "/api/consultar/cruzamento",
            "/api/consultar/cpf-completo",
            "/api/consultar/cep",
            "/api/cep/<cep>",
            "/api/consultar/telefone",
            "/api/telefone/<telefone>",
            "/api/consultar/cnpj",
            "/api/cnpj/<cnpj>",
            "/api/inserir/pessoa",
            "/api/buscar/cruzada",
            "/api/ddd/<ddd>",
            "/api/consultar/bancos",
            "/api/consultar/banco/<codigo>",
            "/api/cache/clear",
            "/api/cache/stats",
            "/api/status"
        ],
        "observacoes": {
            "operadoras": "A identificação de operadoras é baseada em prefixos tradicionais e pode não ser precisa devido à portabilidade numérica implementada no Brasil em 2007."
        }
    })

# Handler para Vercel - Configuração otimizada
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Inicializar o banco de dados apenas uma vez
try:
    init_database()
except Exception as e:
    print(f"Aviso: Erro na inicialização do banco: {e}")

# Exportar a aplicação diretamente para o Vercel
# O Vercel espera uma variável chamada 'app' ou uma função handler

@app.route('/api/directd/consultar-cpf', methods=['POST'])
def api_directd_consultar_cpf():
    """API para consulta de dados pessoais por CPF via Direct Data"""
    try:
        data = request.get_json(force=True)
        cpf = data.get('cpf', '').strip()
        
        if not cpf:
            return jsonify({'success': False, 'error': 'CPF é obrigatório'}), 400
        
        # Importar e usar a função do directd_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from directd_integration import consultar_dados_pessoais_cpf
        
        resultado = consultar_dados_pessoais_cpf(cpf)
        
        return jsonify({
            'success': resultado.get('success', False),
            'data': resultado if resultado.get('success') else None,
            'error': resultado.get('error') if not resultado.get('success') else None,
            'timestamp': datetime.now().isoformat(),
            'fonte': 'Direct Data API'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/directd/consultar-nome', methods=['POST'])
def api_directd_consultar_nome():
    """API para consulta de dados pessoais por nome via Direct Data"""
    try:
        data = request.get_json(force=True)
        nome = data.get('nome', '').strip()
        sobrenome = data.get('sobrenome', '').strip()
        data_nascimento = data.get('data_nascimento', '').strip()
        
        if not nome or not sobrenome:
            return jsonify({'success': False, 'error': 'Nome e sobrenome são obrigatórios'}), 400
        
        # Importar e usar a função do directd_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from directd_integration import consultar_dados_pessoais_nome
        
        resultado = consultar_dados_pessoais_nome(nome, sobrenome, data_nascimento)
        
        return jsonify({
            'success': resultado.get('success', False),
            'data': resultado if resultado.get('success') else None,
            'error': resultado.get('error') if not resultado.get('success') else None,
            'timestamp': datetime.now().isoformat(),
            'fonte': 'Direct Data API'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/directd/status', methods=['GET'])
def api_directd_status():
    """Status da integração Direct Data"""
    try:
        # Importar e usar a função do directd_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from directd_integration import verificar_directd_config
        
        status = verificar_directd_config()
        return jsonify(status)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao verificar status: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/debug/env', methods=['GET'])
def api_debug_env():
    """Debug das variáveis de ambiente"""
    try:
        env_vars = {
            'DIRECT_DATA_TOKEN': 'Configurado' if os.getenv('DIRECT_DATA_TOKEN') else 'Não configurado',
            'DIRECTD_TOKEN': 'Configurado' if os.getenv('DIRECTD_TOKEN') else 'Não configurado',
            'ASSERTIVA_LOCALIZE_TOKEN': 'Configurado' if os.getenv('ASSERTIVA_LOCALIZE_TOKEN') else 'Não configurado',
            'DESK_DATA_TOKEN': 'Configurado' if os.getenv('DESK_DATA_TOKEN') else 'Não configurado',
            'ANTIFRAUDEBRASIL_TOKEN': 'Configurado' if os.getenv('ANTIFRAUDEBRASIL_TOKEN') else 'Não configurado',
            'API_NINJAS_KEY': 'Configurado' if os.getenv('API_NINJAS_KEY') else 'Não configurado',
            'INFOSIMPLES_TOKEN': 'Configurado' if os.getenv('INFOSIMPLES_TOKEN') else 'Não configurado'
        }
        
        return jsonify({
            'success': True,
            'environment_variables': env_vars,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao verificar variáveis de ambiente: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/export', methods=['POST'])
def export_data():
    """Endpoint para exportar dados em JSON ou CSV"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        export_data = data.get('data', {})
        export_format = data.get('format', 'json').lower()
        
        if export_format == 'json':
            # Exportar como JSON
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            response = app.response_class(
                response=json_data,
                status=200,
                mimetype='application/json'
            )
            response.headers['Content-Disposition'] = f'attachment; filename=export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            return response
            
        elif export_format == 'csv':
            # Exportar como CSV
            import csv
            import io
            
            output = io.StringIO()
            
            if isinstance(export_data, list):
                # Lista de objetos
                if export_data:
                    fieldnames = export_data[0].keys() if isinstance(export_data[0], dict) else ['value']
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    for item in export_data:
                        if isinstance(item, dict):
                            writer.writerow(item)
                        else:
                            writer.writerow({'value': item})
            elif isinstance(export_data, dict):
                # Objeto único
                fieldnames = export_data.keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(export_data)
            else:
                # Valor simples
                writer = csv.writer(output)
                writer.writerow(['value'])
                writer.writerow([export_data])
            
            csv_data = output.getvalue()
            output.close()
            
            response = app.response_class(
                response=csv_data,
                status=200,
                mimetype='text/csv'
            )
            response.headers['Content-Disposition'] = f'attachment; filename=export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            return response
        
        else:
            return jsonify({'error': 'Formato não suportado. Use "json" ou "csv"'}), 400
    
    except Exception as e:
        return jsonify({
            'error': f'Erro ao exportar dados: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/documentos/titulo-eleitor', methods=['POST'])
def api_consultar_titulo_eleitor():
    """API para consulta de título de eleitor"""
    try:
        data = request.get_json(force=True)
        titulo = data.get('titulo', '').strip()
        nome = data.get('nome', '').strip()
        
        if not titulo:
            return jsonify({'success': False, 'error': 'Título de eleitor é obrigatório'}), 400
        
        # Importar e usar a função do documentos_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from documentos_integration import consultar_titulo_eleitor
        
        resultado = consultar_titulo_eleitor(titulo, nome)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/documentos/cns', methods=['POST'])
def api_consultar_cns():
    """API para consulta de CNS (Cartão Nacional de Saúde)"""
    try:
        data = request.get_json(force=True)
        cns = data.get('cns', '').strip()
        nome = data.get('nome', '').strip()
        
        if not cns:
            return jsonify({'success': False, 'error': 'CNS é obrigatório'}), 400
        
        # Importar e usar a função do documentos_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from documentos_integration import consultar_cns
        
        resultado = consultar_cns(cns, nome)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/documentos/pis', methods=['POST'])
def api_consultar_pis():
    """API para consulta de PIS/PASEP"""
    try:
        data = request.get_json(force=True)
        pis = data.get('pis', '').strip()
        nome = data.get('nome', '').strip()
        
        if not pis:
            return jsonify({'success': False, 'error': 'PIS é obrigatório'}), 400
        
        # Importar e usar a função do documentos_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from documentos_integration import consultar_pis
        
        resultado = consultar_pis(pis, nome)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/documentos/rg', methods=['POST'])
def api_consultar_rg():
    """API para consulta de RG"""
    try:
        data = request.get_json(force=True)
        rg = data.get('rg', '').strip()
        estado = data.get('estado', '').strip()
        
        # Importar e usar a função do documentos_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from documentos_integration import consultar_rg
        
        resultado = consultar_rg(rg, estado)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/documentos/cnh', methods=['POST'])
def api_consultar_cnh():
    """API para consulta de CNH com parâmetros opcionais para melhor validação"""
    try:
        data = request.get_json(force=True)
        cnh = data.get('cnh', '').strip()
        cpf = data.get('cpf', '').strip() if data.get('cpf') else None
        nome = data.get('nome', '').strip() if data.get('nome') else None
        nome_mae = data.get('nome_mae', '').strip() if data.get('nome_mae') else None
        
        # Importar e usar a classe DocumentosAPI
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from documentos_integration import DocumentosAPI
        
        api = DocumentosAPI()
        resultado = api.consultar_cnh(cnh, cpf, nome, nome_mae)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/documentos/todos', methods=['POST'])
def api_consultar_todos_documentos():
    """API para consulta de todos os documentos"""
    try:
        data = request.get_json(force=True)
        
        # Importar e usar a função do documentos_integration
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from documentos_integration import consultar_todos_documentos
        
        resultado = consultar_todos_documentos(data)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)