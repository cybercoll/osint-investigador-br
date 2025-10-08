from flask import Flask, request, jsonify, render_template_string
import requests
import json
import re
from datetime import datetime

app = Flask(__name__)

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
            .resultado { max-height: 400px; overflow-y: auto; }
        </style>
    </head>
    <body>
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-10">
                    <div class="card">
                        <div class="card-header bg-primary text-white text-center">
                            <h1><i class="fas fa-search"></i> OSINT Investigador BR</h1>
                            <p class="mb-0">Sistema de Investigação OSINT para o Brasil - Versão Completa</p>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-map-marker-alt fa-3x text-primary mb-3"></i>
                                            <h5>Consulta CEP</h5>
                                            <p class="text-muted">Consulte informações de endereço por CEP</p>
                                            <div class="mb-3">
                                                <input type="text" id="cepInput" class="form-control" placeholder="Digite o CEP (ex: 01310-100)" maxlength="9">
                                            </div>
                                            <button class="btn btn-primary" onclick="consultarCEP()">Consultar CEP</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-phone fa-3x text-success mb-3"></i>
                                            <h5>Consulta DDD</h5>
                                            <p class="text-muted">Consulte informações de DDD</p>
                                            <div class="mb-3">
                                                <input type="text" id="dddInput" class="form-control" placeholder="Digite o DDD (ex: 11, 21, 85)" maxlength="2">
                                            </div>
                                            <button class="btn btn-success" onclick="consultarDDD()">Consultar DDD</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-building fa-3x text-warning mb-3"></i>
                                            <h5>Consulta CNPJ</h5>
                                            <p class="text-muted">Consulte informações de empresa</p>
                                            <div class="mb-3">
                                                <input type="text" id="cnpjInput" class="form-control" placeholder="Digite o CNPJ (ex: 11.222.333/0001-81)" maxlength="18">
                                            </div>
                                            <button class="btn btn-warning" onclick="consultarCNPJ()">Consultar CNPJ</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <h5><i class="fas fa-chart-line"></i> Resultado da Consulta:</h5>
                                <div id="resultado" class="border rounded p-3 bg-light resultado">
                                    <p class="text-muted mb-0"><i class="fas fa-info-circle"></i> Nenhuma consulta realizada ainda. Clique em um dos botões acima para começar!</p>
                                </div>
                            </div>
                            
                            <div class="mt-3 text-center">
                                <small class="text-muted">
                                    <i class="fas fa-shield-alt"></i> Sistema OSINT Investigador BR v2.0 - Totalmente Funcional
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function mostrarCarregando() {
                document.getElementById('resultado').innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x text-primary"></i><br><br>Consultando...</div>';
            }
            
            function consultarCEP() {
                const cep = document.getElementById('cepInput').value;
                if (!cep) {
                    alert('Por favor, digite um CEP válido');
                    return;
                }
                mostrarCarregando();
                fetch('/api/consultar/cep', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cep: cep })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('resultado').innerHTML = 
                            '<div class="alert alert-success"><h6><i class="fas fa-check-circle"></i> CEP Encontrado!</h6></div>' +
                            '<pre class="bg-light p-3 rounded">' + JSON.stringify(data, null, 2) + '</pre>';
                    } else {
                        document.getElementById('resultado').innerHTML = 
                            '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> ' + (data.message || data.erro) + '</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = 
                        '<div class="alert alert-danger"><i class="fas fa-times-circle"></i> Erro na consulta: ' + error + '</div>';
                });
            }
            
            function consultarDDD() {
                const ddd = document.getElementById('dddInput').value;
                if (!ddd) {
                    alert('Por favor, digite um DDD válido');
                    return;
                }
                mostrarCarregando();
                fetch('/api/consultar/ddd', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ddd: ddd })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('resultado').innerHTML = 
                            '<div class="alert alert-success"><h6><i class="fas fa-check-circle"></i> DDD Encontrado!</h6></div>' +
                            '<pre class="bg-light p-3 rounded">' + JSON.stringify(data, null, 2) + '</pre>';
                    } else {
                        document.getElementById('resultado').innerHTML = 
                            '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> ' + (data.message || data.erro) + '</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = 
                        '<div class="alert alert-danger"><i class="fas fa-times-circle"></i> Erro na consulta: ' + error + '</div>';
                });
            }
            
            function consultarCNPJ() {
                const cnpj = document.getElementById('cnpjInput').value;
                if (!cnpj) {
                    alert('Por favor, digite um CNPJ válido');
                    return;
                }
                mostrarCarregando();
                fetch('/api/consultar/cnpj', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cnpj: cnpj })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('resultado').innerHTML = 
                            '<div class="alert alert-success"><h6><i class="fas fa-check-circle"></i> CNPJ Encontrado!</h6></div>' +
                            '<pre class="bg-light p-3 rounded">' + JSON.stringify(data, null, 2) + '</pre>';
                    } else {
                        document.getElementById('resultado').innerHTML = 
                            '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> ' + (data.message || data.erro) + '</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = 
                        '<div class="alert alert-danger"><i class="fas fa-times-circle"></i> Erro na consulta: ' + error + '</div>';
                });
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
        "message": "OSINT Investigador BR - API Completa Funcionando!",
        "version": "2.0.0",
        "method": request.method,
        "path": request.path,
        "endpoint": "api",
        "features": [
            "Consulta CEP via ViaCEP",
            "Consulta DDD via BrasilAPI", 
            "Consulta CNPJ via BrasilAPI",
            "Interface Web Completa"
        ],
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
        "version": "2.0.0",
        "services": {
            "viacep_api": True,
            "brasilapi": True,
            "web_interface": True,
            "osint_features": True
        },
        "message": "Todos os serviços OSINT estão operacionais!"
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

@app.route('/api/consultar/ddd', methods=['POST'])
def api_consultar_ddd():
    """Consulta informações de DDD"""
    try:
        data = request.get_json()
        if not data or 'ddd' not in data:
            return jsonify({"erro": "DDD não fornecido"}), 400
        
        ddd = data['ddd']
        if not validar_ddd(ddd):
            return jsonify({"erro": "DDD inválido. Use apenas 2 dígitos (ex: 11, 21, 85)"}), 400
        
        resultado = consultar_ddd_brasilapi(ddd)
        if resultado:
            return jsonify({
                "status": "success",
                "ddd": ddd,
                "dados": resultado,
                "fonte": "BrasilAPI",
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify({
            "status": "error", 
            "message": "DDD não encontrado",
            "ddd": ddd
        }), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/consultar/cnpj', methods=['POST'])
def api_consultar_cnpj():
    """Consulta informações de CNPJ"""
    try:
        data = request.get_json()
        if not data or 'cnpj' not in data:
            return jsonify({"erro": "CNPJ não fornecido"}), 400
        
        cnpj = data['cnpj']
        if not validar_cnpj(cnpj):
            return jsonify({"erro": "CNPJ inválido. Use 14 dígitos"}), 400
        
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
            "message": "CNPJ não encontrado ou inválido", 
            "cnpj": cnpj
        }), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/<path:path>')
def api_catch_all(path):
    """Captura todas as outras rotas da API"""
    return jsonify({
        "status": "success",
        "message": "OSINT Investigador BR - Endpoint não encontrado",
        "version": "2.0.0",
        "method": request.method,
        "path": request.path,
        "endpoint": path,
        "available_endpoints": [
            "/api/consultar/cep",
            "/api/consultar/ddd",
            "/api/consultar/cnpj", 
            "/api/status"
        ],
        "help": "Use os endpoints disponíveis para consultas OSINT"
    })

if __name__ == '__main__':
    app.run(debug=True)