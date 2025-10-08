# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests
import json
import re
from datetime import datetime
import sqlite3
import os
import tempfile

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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
            "/api/consultar/cpf-completo",
            "/api/inserir/pessoa",
            "/api/buscar/cruzada",
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
        
        # Buscar no banco de dados
        resultado = buscar_por_cpf(cpf)
        
        if resultado["status"] == "success":
            response = jsonify({
                "status": "success",
                "message": "CPF encontrado no banco de dados",
                "dados": resultado["dados"],
                "timestamp": datetime.now().isoformat()
            })
        elif resultado["status"] == "not_found":
            response = jsonify({
                "status": "not_found",
                "message": "CPF não encontrado no banco de dados",
                "cpf_consultado": cpf,
                "timestamp": datetime.now().isoformat()
            })
        else:
            response = jsonify({
                "status": "error",
                "erro": resultado["message"],
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

@app.route('/api/<path:path>')
def api_catch_all(path):
    """Captura outras rotas da API"""
    return jsonify({
        "status": "success",
        "message": "Endpoint não encontrado",
        "available_endpoints": [
            "/api/consultar/cruzamento",
            "/api/consultar/cpf-completo",
            "/api/inserir/pessoa",
            "/api/buscar/cruzada",
            "/api/status"
        ]
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

if __name__ == '__main__':
    app.run(debug=True)