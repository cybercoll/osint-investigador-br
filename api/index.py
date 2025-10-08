# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template_string
import requests
import json
import re
from datetime import datetime
import sys
import os

# Adicionar o diretório pai ao path para importar o database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DatabaseManager

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Inicializar o banco de dados
db = DatabaseManager()

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
        resultado = db.buscar_por_cpf(cpf)
        
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
        resultado = db.inserir_pessoa(
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
        resultado = db.buscar_cruzada(**data)
        
        if resultado["status"] == "success":
            response = jsonify({
                "status": "success",
                "message": f"Encontrados {resultado['total_encontrados']} registros",
                "total_encontrados": resultado["total_encontrados"],
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

if __name__ == '__main__':
    app.run(debug=True)