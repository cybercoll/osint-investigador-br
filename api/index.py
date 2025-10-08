from flask import Flask, request, jsonify, render_template_string
import os
import sys
import json
import re
from datetime import datetime

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from brasilapi_integration import BrasilAPIClient
    from viacep_integration import ViaCEPClient
    APIS_AVAILABLE = True
except ImportError:
    APIS_AVAILABLE = False

app = Flask(__name__)

# Inicializar clientes das APIs se disponíveis
if APIS_AVAILABLE:
    brasil_api = BrasilAPIClient()
    viacep_client = ViaCEPClient()

def validar_cep(cep):
    """Valida formato de CEP"""
    if not cep:
        return False
    cep_limpo = re.sub(r'\D', '', cep)
    return len(cep_limpo) == 8 and cep_limpo.isdigit()

def validar_ddd(ddd):
    """Valida formato de DDD"""
    if not ddd:
        return False
    ddd_limpo = re.sub(r'\D', '', ddd)
    return len(ddd_limpo) == 2 and ddd_limpo.isdigit()

def validar_cnpj(cnpj):
    """Valida formato básico de CNPJ"""
    if not cnpj:
        return False
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    return len(cnpj_limpo) == 14 and cnpj_limpo.isdigit()

@app.route('/')
def home():
    """Página principal com interface web"""
    html_template = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OSINT Investigador BR</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .card { box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: none; }
            .btn-primary { background: #3498db; border: none; }
            .btn-primary:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white text-center">
                            <h1><i class="fas fa-search"></i> OSINT Investigador BR</h1>
                            <p class="mb-0">Sistema de Investigação OSINT para o Brasil</p>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-map-marker-alt fa-3x text-primary mb-3"></i>
                                            <h5>Consulta CEP</h5>
                                            <p class="text-muted">Consulte informações de endereço por CEP</p>
                                            <button class="btn btn-primary" onclick="consultarCEP()">Consultar</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-phone fa-3x text-success mb-3"></i>
                                            <h5>Consulta DDD</h5>
                                            <p class="text-muted">Consulte informações de DDD</p>
                                            <button class="btn btn-success" onclick="consultarDDD()">Consultar</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-building fa-3x text-warning mb-3"></i>
                                            <h5>Consulta CNPJ</h5>
                                            <p class="text-muted">Consulte informações de empresa</p>
                                            <button class="btn btn-warning" onclick="consultarCNPJ()">Consultar</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <h5>Resultado da Consulta:</h5>
                                <div id="resultado" class="border rounded p-3 bg-light">
                                    <p class="text-muted mb-0">Nenhuma consulta realizada ainda.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function consultarCEP() {
                const cep = prompt("Digite o CEP (apenas números):");
                if (cep) {
                    fetch('/api/consultar/cep', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ cep: cep })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('resultado').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('resultado').innerHTML = '<div class="text-danger">Erro: ' + error + '</div>';
                    });
                }
            }
            
            function consultarDDD() {
                const ddd = prompt("Digite o DDD (apenas números):");
                if (ddd) {
                    fetch('/api/consultar/ddd', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ ddd: ddd })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('resultado').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('resultado').innerHTML = '<div class="text-danger">Erro: ' + error + '</div>';
                    });
                }
            }
            
            function consultarCNPJ() {
                const cnpj = prompt("Digite o CNPJ (apenas números):");
                if (cnpj) {
                    fetch('/api/consultar/cnpj', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ cnpj: cnpj })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('resultado').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('resultado').innerHTML = '<div class="text-danger">Erro: ' + error + '</div>';
                    });
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api')
def api_info():
    """Informações da API"""
    return jsonify({
        "status": "success",
        "message": "OSINT Investigador BR - API Funcionando!",
        "version": "1.0.0",
        "method": request.method,
        "path": request.path,
        "endpoint": "api",
        "apis_available": APIS_AVAILABLE,
        "endpoints": [
            "/api/consultar/cep",
            "/api/consultar/ddd", 
            "/api/consultar/cnpj",
            "/api/status"
        ]
    })

@app.route('/api/status')
def api_status():
    """Status da API e serviços"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "brasil_api": APIS_AVAILABLE,
            "viacep": APIS_AVAILABLE,
            "web_interface": True
        }
    })

@app.route('/api/consultar/cep', methods=['POST'])
def api_consultar_cep():
    """Consulta informações de CEP"""
    try:
        data = request.get_json()
        if not data or 'cep' not in data:
            return jsonify({"erro": "CEP não fornecido"}), 400
        
        cep = data['cep']
        if not validar_cep(cep):
            return jsonify({"erro": "CEP inválido"}), 400
        
        if APIS_AVAILABLE:
            resultado = viacep_client.consultar_cep(cep)
            if resultado:
                return jsonify({
                    "status": "success",
                    "cep": cep,
                    "dados": resultado,
                    "fonte": "ViaCEP"
                })
        
        return jsonify({
            "status": "error",
            "message": "APIs não disponíveis ou CEP não encontrado",
            "cep": cep
        }), 404
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/consultar/ddd', methods=['POST'])
def api_consultar_ddd():
    """Consulta informações de DDD"""
    try:
        data = request.get_json()
        if not data or 'ddd' not in data:
            return jsonify({"erro": "DDD não fornecido"}), 400
        
        ddd = data['ddd']
        if not validar_ddd(ddd):
            return jsonify({"erro": "DDD inválido"}), 400
        
        if APIS_AVAILABLE:
            resultado = brasil_api.consultar_ddd(ddd)
            if resultado:
                return jsonify({
                    "status": "success",
                    "ddd": ddd,
                    "dados": resultado,
                    "fonte": "BrasilAPI"
                })
        
        return jsonify({
            "status": "error", 
            "message": "APIs não disponíveis ou DDD não encontrado",
            "ddd": ddd
        }), 404
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/consultar/cnpj', methods=['POST'])
def api_consultar_cnpj():
    """Consulta informações de CNPJ"""
    try:
        data = request.get_json()
        if not data or 'cnpj' not in data:
            return jsonify({"erro": "CNPJ não fornecido"}), 400
        
        cnpj = data['cnpj']
        if not validar_cnpj(cnpj):
            return jsonify({"erro": "CNPJ inválido"}), 400
        
        if APIS_AVAILABLE:
            resultado = brasil_api.consultar_cnpj(cnpj)
            if resultado:
                return jsonify({
                    "status": "success",
                    "cnpj": cnpj,
                    "dados": resultado,
                    "fonte": "BrasilAPI"
                })
        
        return jsonify({
            "status": "error",
            "message": "APIs não disponíveis ou CNPJ não encontrado", 
            "cnpj": cnpj
        }), 404
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/<path:path>')
def api_catch_all(path):
    """Captura todas as outras rotas da API"""
    return jsonify({
        "status": "success",
        "message": "OSINT Investigador BR - Endpoint não encontrado",
        "version": "1.0.0",
        "method": request.method,
        "path": request.path,
        "endpoint": path,
        "available_endpoints": [
            "/api/consultar/cep",
            "/api/consultar/ddd",
            "/api/consultar/cnpj", 
            "/api/status"
        ]
    })

# Para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True)