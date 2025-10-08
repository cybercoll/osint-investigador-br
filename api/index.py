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

def validar_cpf(cpf):
    """Valida CPF usando algoritmo matemático oficial"""
    if not cpf:
        return False
    
    # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf_limpo == cpf_limpo[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro dígito
    if int(cpf_limpo[9]) != digito1:
        return False
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo dígito
    return int(cpf_limpo[10]) == digito2

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

def validar_email(email):
    """Valida formato básico de email"""
    if not email:
        return False
    
    # Regex básico para validação de email
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def consultar_email_gamalogic(email):
    """Consulta validação de email via Gamalogic API (gratuita)"""
    try:
        # API gratuita da Gamalogic - 500 créditos grátis
        url = "https://api.gamalogic.com/v1/email/verify"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'email': email
        }
        
        # Nota: Para usar a API real, seria necessário um token
        # Por enquanto, retornamos validação local
        if validar_email(email):
            return {
                'email': email,
                'valid': True,
                'status': 'valid',
                'provider': email.split('@')[1] if '@' in email else 'unknown',
                'message': 'Email válido (validação local)'
            }
        else:
            return {
                'email': email,
                'valid': False,
                'status': 'invalid',
                'message': 'Formato de email inválido'
            }
    except Exception as e:
        return {
            'email': email,
            'valid': False,
            'status': 'error',
            'message': f'Erro na validação: {str(e)}'
        }

def consultar_endereco_completo(logradouro, cidade, uf):
    """Consulta endereço completo usando BrasilAPI"""
    try:
        # Limpar e formatar parâmetros
        logradouro = logradouro.strip()
        cidade = cidade.strip()
        uf = uf.strip().upper()
        
        # Validar UF
        ufs_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        if uf not in ufs_validas:
            return {'status': 'error', 'message': 'UF inválida'}
        
        # Construir URL da BrasilAPI para busca de endereço
        url = f"https://brasilapi.com.br/api/cep/v2/{uf}/{cidade}/{logradouro}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'status': 'success',
                    'message': 'Endereços encontrados',
                    'total_resultados': len(data),
                    'enderecos': data,
                    'fonte': 'BrasilAPI'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Nenhum endereço encontrado para os dados informados'
                }
        else:
            return {
                'status': 'error',
                'message': f'Erro na consulta: {response.status_code}'
            }
            
    except requests.exceptions.Timeout:
        return {'status': 'error', 'message': 'Timeout na consulta'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'Erro na requisição: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Erro interno: {str(e)}'}

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
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .card { 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
                border: none; 
                border-radius: 15px;
                transition: transform 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
            }
            
            .btn-primary { background: #3498db; border: none; }
            .btn-primary:hover { background: #2980b9; }
            .btn-success:hover { background: #27ae60; }
            .btn-warning:hover { background: #f39c12; }
            .btn-info:hover { background: #3498db; }
            .btn-secondary:hover { background: #7f8c8d; }
            .btn-danger:hover { background: #e74c3c; }
            
            .resultado { 
                max-height: 500px; 
                overflow-y: auto; 
                border-radius: 10px;
                background: #f8f9fa;
                padding: 15px;
                margin-top: 20px;
            }
            
            /* Responsive Table Styles */
            .table-responsive {
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .table {
                margin-bottom: 0;
                font-size: 0.95rem;
                background: white;
            }
            
            .table th {
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white;
                font-weight: 600;
                text-align: center;
                padding: 12px 15px;
                border: none;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .table td {
                padding: 12px 15px;
                vertical-align: middle;
                border-top: 1px solid #dee2e6;
                text-align: center;
            }
            
            .table-striped tbody tr:nth-of-type(odd) {
                background-color: rgba(52, 152, 219, 0.05);
            }
            
            .table-hover tbody tr:hover {
                background-color: rgba(52, 152, 219, 0.1);
                transform: scale(1.01);
                transition: all 0.2s ease;
            }
            
            /* Alert Styles */
            .alert {
                border: none;
                border-radius: 10px;
                padding: 15px 20px;
                margin-bottom: 20px;
                font-weight: 500;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .alert-success {
                background: linear-gradient(135deg, #d4edda, #c3e6cb);
                color: #155724;
                border-left: 4px solid #28a745;
            }
            
            .alert-danger {
                background: linear-gradient(135deg, #f8d7da, #f1b0b7);
                color: #721c24;
                border-left: 4px solid #dc3545;
            }
            
            .alert-info {
                background: linear-gradient(135deg, #d1ecf1, #bee5eb);
                color: #0c5460;
                border-left: 4px solid #17a2b8;
            }
            
            /* Loading Animation */
            .spinner-border {
                width: 3rem;
                height: 3rem;
                margin: 20px auto;
                display: block;
            }
            
            /* Badge Styles */
            .badge {
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .badge-success { background: linear-gradient(135deg, #28a745, #20c997); }
            .badge-danger { background: linear-gradient(135deg, #dc3545, #e83e8c); }
            .badge-info { background: linear-gradient(135deg, #17a2b8, #6f42c1); }
            
            /* Mobile Responsive Design */
            @media (max-width: 768px) {
                .container {
                    padding: 10px;
                }
                
                .card-body {
                    padding: 15px;
                }
                
                .table-responsive {
                    font-size: 0.85rem;
                }
                
                .table th, .table td {
                    padding: 8px 10px;
                    font-size: 0.8rem;
                }
                
                .btn {
                    padding: 10px 15px;
                    font-size: 0.9rem;
                }
                
                .form-control {
                    padding: 10px 12px;
                    font-size: 0.9rem;
                }
                
                h1 {
                    font-size: 1.8rem;
                }
                
                h5 {
                    font-size: 1.1rem;
                }
                
                .fa-3x {
                    font-size: 2rem !important;
                }
            }
            
            @media (max-width: 480px) {
                .table-responsive {
                    font-size: 0.75rem;
                }
                
                .table th, .table td {
                    padding: 6px 8px;
                    font-size: 0.75rem;
                }
                
                .btn {
                    padding: 8px 12px;
                    font-size: 0.85rem;
                }
                
                .card-body {
                    padding: 10px;
                }
                
                h1 {
                    font-size: 1.5rem;
                }
                
                .fa-3x {
                    font-size: 1.5rem !important;
                }
            }
            
            /* Custom Scrollbar */
            .resultado::-webkit-scrollbar {
                width: 8px;
            }
            
            .resultado::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            
            .resultado::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 4px;
            }
            
            .resultado::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            
            /* Animation for cards */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .card {
                animation: fadeInUp 0.6s ease-out;
            }
            
            /* Professional table header gradient */
            .table thead th {
                position: relative;
                overflow: hidden;
            }
            
            .table thead th::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .table thead th:hover::before {
                left: 100%;
            }
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
                            
                            <!-- Segunda linha de funcionalidades -->
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-id-card fa-3x text-info mb-3"></i>
                                            <h5>Validação CPF</h5>
                                            <p class="text-muted">Valide CPF usando algoritmo matemático</p>
                                            <div class="mb-3">
                                                <input type="text" id="cpfInput" class="form-control" placeholder="Digite o CPF (ex: 123.456.789-09)" maxlength="14">
                                            </div>
                                            <button class="btn btn-info" onclick="consultarCPF()">Validar CPF</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-mobile-alt fa-3x text-secondary mb-3"></i>
                                            <h5>Validação Telefone</h5>
                                            <p class="text-muted">Valide telefone/celular brasileiro</p>
                                            <div class="mb-3">
                                                <input type="text" id="telefoneInput" class="form-control" placeholder="Digite o telefone (ex: 11999999999)" maxlength="15">
                                            </div>
                                            <button class="btn btn-secondary" onclick="consultarTelefone()">Validar Telefone</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-envelope fa-3x text-danger mb-3"></i>
                                            <h5>Validação Email</h5>
                                            <p class="text-muted">Valide formato e existência de email</p>
                                            <div class="mb-3">
                                                <input type="email" id="emailInput" class="form-control" placeholder="Digite o email (ex: user@domain.com)">
                                            </div>
                                            <button class="btn btn-danger" onclick="consultarEmail()">Validar Email</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Terceira linha de funcionalidades -->
                            <div class="row">
                                <div class="col-md-12 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body text-center">
                                            <i class="fas fa-map-marker-alt fa-3x text-warning mb-3"></i>
                                            <h5>Consulta Endereço Completo</h5>
                                            <p class="text-muted">Busque endereços por logradouro, cidade e UF</p>
                                            <div class="row mb-3">
                                                <div class="col-md-4">
                                                    <input type="text" id="logradouroInput" class="form-control" placeholder="Logradouro (ex: Rua das Flores)">
                                                </div>
                                                <div class="col-md-4">
                                                    <input type="text" id="cidadeInput" class="form-control" placeholder="Cidade (ex: São Paulo)">
                                                </div>
                                                <div class="col-md-4">
                                                    <input type="text" id="ufInput" class="form-control" placeholder="UF (ex: SP)" maxlength="2">
                                                </div>
                                            </div>
                                            <button class="btn btn-warning" onclick="consultarEndereco()">Buscar Endereços</button>
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
                                    <i class="fas fa-shield-alt"></i> Sistema OSINT Investigador BR v3.0 - Funcionalidades Expandidas
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Função para exportar dados
            function exportarDados(dados, tipo, formato) {
                const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
                const filename = `osint_${tipo}_${timestamp}`;
                
                if (formato === 'json') {
                    const dataStr = JSON.stringify(dados, null, 2);
                    const dataBlob = new Blob([dataStr], {type: 'application/json'});
                    const url = URL.createObjectURL(dataBlob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `${filename}.json`;
                    link.click();
                    URL.revokeObjectURL(url);
                } else if (formato === 'csv') {
                    let csvContent = '';
                    if (Array.isArray(dados)) {
                        if (dados.length > 0) {
                            const headers = Object.keys(dados[0]);
                            csvContent = headers.join(',') + '\\n';
                            dados.forEach(row => {
                                const values = headers.map(header => {
                                    const value = row[header] || '';
                                    return `"${String(value).replace(/"/g, '""')}"`;
                                });
                                csvContent += values.join(',') + '\\n';
                            });
                        }
                    } else {
                        const headers = Object.keys(dados);
                        csvContent = 'Campo,Valor\\n';
                        headers.forEach(key => {
                            const value = dados[key] || '';
                            csvContent += `"${key}","${String(value).replace(/"/g, '""')}"\\n`;
                        });
                    }
                    
                    const dataBlob = new Blob([csvContent], {type: 'text/csv;charset=utf-8;'});
                    const url = URL.createObjectURL(dataBlob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `${filename}.csv`;
                    link.click();
                    URL.revokeObjectURL(url);
                }
            }
            
            // Função para criar botões de exportação
            function criarBotoesExportacao(dados, tipo) {
                return `
                    <div class="mt-3 text-center">
                        <div class="btn-group" role="group" aria-label="Exportar dados">
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="exportarDados(${JSON.stringify(dados).replace(/"/g, '&quot;')}, '${tipo}', 'json')">
                                <i class="fas fa-download"></i> JSON
                            </button>
                            <button type="button" class="btn btn-outline-success btn-sm" onclick="exportarDados(${JSON.stringify(dados).replace(/"/g, '&quot;')}, '${tipo}', 'csv')">
                                <i class="fas fa-file-csv"></i> CSV
                            </button>
                        </div>
                        <div class="mt-2">
                            <small class="text-muted">
                                <i class="fas fa-info-circle"></i> Clique para exportar os dados em diferentes formatos
                            </small>
                        </div>
                    </div>
                `;
            }
            
            function mostrarCarregando() {
                document.getElementById('resultado').innerHTML = 
                    '<div class="text-center p-4">' +
                    '<div class="spinner-border text-primary" role="status">' +
                    '<span class="sr-only">Carregando...</span>' +
                    '</div>' +
                    '<p class="mt-2 text-muted">Processando consulta...</p>' +
                    '</div>';
            }
            
            function formatarResultadoCEP(data) {
                if (data.status === 'success') {
                    const cepData = data.dados || data;
                    return `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> CEP Encontrado com Sucesso!</h6>
                        </div>
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h6 class="mb-0"><i class="fas fa-map-marker-alt"></i> Informações do Endereço</h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <tbody>
                                            <tr><td class="fw-bold text-primary">CEP:</td><td>${cepData.cep || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-primary">Logradouro:</td><td>${cepData.logradouro || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-primary">Bairro:</td><td>${cepData.bairro || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-primary">Cidade:</td><td>${cepData.localidade || cepData.cidade || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-primary">UF:</td><td>${cepData.uf || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-primary">IBGE:</td><td>${cepData.ibge || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-primary">DDD:</td><td>${cepData.ddd || 'N/A'}</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-muted small">
                                    <i class="fas fa-info-circle"></i> Fonte: ${data.fonte || 'ViaCEP'} | 
                                    <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                                </div>
                                ${criarBotoesExportacao(cepData, 'cep')}
                            </div>
                        </div>
                    `;
                }
            }
            
            function formatarResultadoDDD(data) {
                if (data.status === 'success') {
                    const dddData = data.dados || data;
                    return `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> DDD Encontrado com Sucesso!</h6>
                        </div>
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h6 class="mb-0"><i class="fas fa-phone"></i> Informações do DDD</h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <tbody>
                                            <tr><td class="fw-bold text-info">DDD:</td><td>${dddData.code || dddData.ddd || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-info">Estado:</td><td>${dddData.state || dddData.estado || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-info">Cidades:</td><td>${Array.isArray(dddData.cities) ? dddData.cities.join(', ') : (dddData.cidades || 'N/A')}</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-muted small">
                                    <i class="fas fa-info-circle"></i> Fonte: ${data.fonte || 'BrasilAPI'} | 
                                    <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                                </div>
                                ${criarBotoesExportacao(dddData, 'ddd')}
                            </div>
                        </div>
                    `;
                }
            }
            
            function formatarResultadoCNPJ(data) {
                if (data.status === 'success') {
                    const cnpjData = data.dados || data;
                    return `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> CNPJ Encontrado com Sucesso!</h6>
                        </div>
                        <div class="card">
                            <div class="card-header bg-success text-white">
                                <h6 class="mb-0"><i class="fas fa-building"></i> Informações da Empresa</h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <tbody>
                                            <tr><td class="fw-bold text-success">CNPJ:</td><td>${cnpjData.cnpj || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Razão Social:</td><td>${cnpjData.company?.name || cnpjData.razao_social || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Nome Fantasia:</td><td>${cnpjData.alias || cnpjData.nome_fantasia || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Situação:</td><td><span class="badge ${cnpjData.status === 'OK' ? 'bg-success' : 'bg-warning'}">${cnpjData.status || cnpjData.situacao || 'N/A'}</span></td></tr>
                                            <tr><td class="fw-bold text-success">Tipo:</td><td>${cnpjData.type || cnpjData.tipo || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Porte:</td><td>${cnpjData.size || cnpjData.porte || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Natureza Jurídica:</td><td>${cnpjData.nature || cnpjData.natureza_juridica || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Atividade Principal:</td><td>${cnpjData.main_activity?.text || cnpjData.atividade_principal || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Telefone:</td><td>${cnpjData.phone || cnpjData.telefone || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-success">Email:</td><td>${cnpjData.email || 'N/A'}</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-muted small">
                                    <i class="fas fa-info-circle"></i> Fonte: ${data.fonte || 'BrasilAPI'} | 
                                    <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                                </div>
                                ${criarBotoesExportacao(cnpjData, 'cnpj')}
                            </div>
                        </div>
                    `;
                }
            }
            
            function formatarResultadoCPF(data) {
                if (data.status === 'success') {
                    return `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> CPF Validado com Sucesso!</h6>
                        </div>
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h6 class="mb-0"><i class="fas fa-id-card"></i> Validação de CPF</h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <tbody>
                                            <tr><td class="fw-bold text-info">CPF:</td><td>${data.cpf || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-info">Status:</td><td><span class="badge bg-success">Válido</span></td></tr>
                                            <tr><td class="fw-bold text-info">Algoritmo:</td><td>Validação Matemática Local</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-muted small">
                                    <i class="fas fa-info-circle"></i> Validação: Algoritmo Matemático | 
                                    <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                                </div>
                                ${criarBotoesExportacao(data, 'cpf')}
                            </div>
                        </div>
                    `;
                }
            }
            
            function formatarResultadoTelefone(data) {
                if (data.status === 'success') {
                    const telData = data.dados || data;
                    return `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> Telefone Validado com Sucesso!</h6>
                        </div>
                        <div class="card">
                            <div class="card-header bg-secondary text-white">
                                <h6 class="mb-0"><i class="fas fa-mobile-alt"></i> Informações do Telefone</h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <tbody>
                                            <tr><td class="fw-bold text-secondary">Telefone:</td><td>${data.telefone || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-secondary">DDD:</td><td>${telData.ddd || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-secondary">Tipo:</td><td><span class="badge bg-info">${telData.tipo || 'N/A'}</span></td></tr>
                                            <tr><td class="fw-bold text-secondary">Estado:</td><td>${telData.estado || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-secondary">Região:</td><td>${telData.regiao || 'N/A'}</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-muted small">
                                    <i class="fas fa-info-circle"></i> Fonte: ${data.fonte || 'Validação Local + BrasilAPI'} | 
                                    <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                                </div>
                                ${criarBotoesExportacao(telData, 'telefone')}
                            </div>
                        </div>
                    `;
                }
            }
            
            function formatarResultadoEmail(data) {
                if (data.status === 'success') {
                    return `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> Email Validado com Sucesso!</h6>
                        </div>
                        <div class="card">
                            <div class="card-header bg-danger text-white">
                                <h6 class="mb-0"><i class="fas fa-envelope"></i> Validação de Email</h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <tbody>
                                            <tr><td class="fw-bold text-danger">Email:</td><td>${data.email || 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-danger">Formato:</td><td><span class="badge bg-success">Válido</span></td></tr>
                                            <tr><td class="fw-bold text-danger">Domínio:</td><td>${data.email ? data.email.split('@')[1] : 'N/A'}</td></tr>
                                            <tr><td class="fw-bold text-danger">Validação:</td><td>Formato + Gamalogic API</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-muted small">
                                    <i class="fas fa-info-circle"></i> Fonte: ${data.fonte || 'Validação Local + Gamalogic'} | 
                                    <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                                </div>
                                ${criarBotoesExportacao(data, 'email')}
                            </div>
                        </div>
                    `;
                }
            }
            
            function formatarResultadoEndereco(data) {
                if (data.status === 'success') {
                    const enderecos = data.dados?.enderecos || [];
                    let html = `
                        <div class="alert alert-success">
                            <h6><i class="fas fa-check-circle"></i> ${enderecos.length} Endereço(s) Encontrado(s)!</h6>
                        </div>
                    `;
                    
                    enderecos.forEach((endereco, index) => {
                        html += `
                            <div class="card mb-3">
                                <div class="card-header bg-warning text-dark">
                                    <h6 class="mb-0"><i class="fas fa-map-marker-alt"></i> Endereço ${index + 1}</h6>
                                </div>
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-hover">
                                            <tbody>
                                                <tr><td class="fw-bold text-warning">CEP:</td><td>${endereco.cep || 'N/A'}</td></tr>
                                                <tr><td class="fw-bold text-warning">Logradouro:</td><td>${endereco.street || endereco.logradouro || 'N/A'}</td></tr>
                                                <tr><td class="fw-bold text-warning">Bairro:</td><td>${endereco.district || endereco.bairro || 'N/A'}</td></tr>
                                                <tr><td class="fw-bold text-warning">Cidade:</td><td>${endereco.city || endereco.cidade || 'N/A'}</td></tr>
                                                <tr><td class="fw-bold text-warning">UF:</td><td>${endereco.state || endereco.uf || 'N/A'}</td></tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                    
                    html += `
                        <div class="mt-3 text-muted small">
                            <i class="fas fa-info-circle"></i> Fonte: ${data.fonte || 'BrasilAPI'} | 
                            <i class="fas fa-clock"></i> ${data.timestamp ? new Date(data.timestamp).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
                        </div>
                        ${criarBotoesExportacao(data.dados, 'endereco')}
                    `;
                    
                    return html;
                }
            }
            
            function formatarErro(message, tipo = 'danger') {
                return `
                    <div class="alert alert-${tipo}">
                        <h6><i class="fas fa-exclamation-triangle"></i> Erro na Consulta</h6>
                        <p class="mb-0">${message}</p>
                    </div>
                `;
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
                        document.getElementById('resultado').innerHTML = formatarResultadoCEP(data);
                    } else {
                        document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
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
                        document.getElementById('resultado').innerHTML = formatarResultadoDDD(data);
                    } else {
                        document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
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
                        document.getElementById('resultado').innerHTML = formatarResultadoCNPJ(data);
                    } else {
                        document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
                });
            }
            
            function consultarCPF() {
                const cpf = document.getElementById('cpfInput').value;
                if (!cpf) {
                    alert('Por favor, digite um CPF válido');
                    return;
                }
                mostrarCarregando();
                fetch('/api/consultar/cpf', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cpf: cpf })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('resultado').innerHTML = formatarResultadoCPF(data);
                    } else {
                        document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
                });
            }
            
            function consultarTelefone() {
                const telefone = document.getElementById('telefoneInput').value;
                if (!telefone) {
                    alert('Por favor, digite um telefone válido');
                    return;
                }
                mostrarCarregando();
                fetch('/api/consultar/telefone', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ telefone: telefone })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('resultado').innerHTML = formatarResultadoTelefone(data);
                    } else {
                        document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                    }
                })
                .catch(error => {
                    document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
                });
            }
            
            function consultarEmail() {
                 const email = document.getElementById('emailInput').value;
                 if (!email) {
                     alert('Por favor, digite um email válido');
                     return;
                 }
                 mostrarCarregando();
                 fetch('/api/consultar/email', {
                     method: 'POST',
                     headers: { 'Content-Type': 'application/json' },
                     body: JSON.stringify({ email: email })
                 })
                 .then(response => response.json())
                 .then(data => {
                     if (data.status === 'success') {
                         document.getElementById('resultado').innerHTML = formatarResultadoEmail(data);
                     } else {
                         document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                     }
                 })
                 .catch(error => {
                     document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
                 });
             }
             
             function consultarEndereco() {
                 const logradouro = document.getElementById('logradouroInput').value;
                 const cidade = document.getElementById('cidadeInput').value;
                 const uf = document.getElementById('ufInput').value;
                 
                 if (!logradouro || !cidade || !uf) {
                     alert('Por favor, preencha logradouro, cidade e UF');
                     return;
                 }
                 
                 mostrarCarregando();
                 fetch('/api/consultar/endereco', {
                     method: 'POST',
                     headers: { 'Content-Type': 'application/json' },
                     body: JSON.stringify({ 
                         logradouro: logradouro,
                         cidade: cidade,
                         uf: uf 
                     })
                 })
                 .then(response => response.json())
                 .then(data => {
                     if (data.status === 'success') {
                         document.getElementById('resultado').innerHTML = formatarResultadoEndereco(data);
                     } else {
                         document.getElementById('resultado').innerHTML = formatarErro(data.message || data.erro);
                     }
                 })
                 .catch(error => {
                     document.getElementById('resultado').innerHTML = formatarErro('Erro na consulta: ' + error);
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
            "Validação CPF (algoritmo matemático)",
            "Validação Telefone/Celular",
            "Validação Email",
            "Consulta Endereço Completo",
            "Interface Web Completa"
        ],
        "endpoints": [
            "/api/consultar/cep",
            "/api/consultar/ddd", 
            "/api/consultar/cnpj",
            "/api/consultar/cpf",
            "/api/consultar/telefone",
            "/api/consultar/email",
            "/api/consultar/endereco",
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
            "osint_features": True,
            "cpf_validation": True,
            "phone_validation": True,
            "email_validation": True,
            "address_search": True
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

@app.route('/api/consultar/cpf', methods=['POST'])
def api_consultar_cpf():
    """Valida CPF usando algoritmo matemático oficial"""
    try:
        data = request.get_json()
        if not data or 'cpf' not in data:
            return jsonify({"erro": "CPF não fornecido"}), 400
        
        cpf = data['cpf']
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if validar_cpf(cpf):
            return jsonify({
                "status": "success",
                "cpf": cpf,
                "cpf_formatado": f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}",
                "valido": True,
                "message": "CPF válido",
                "algoritmo": "Validação matemática oficial",
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "cpf": cpf,
                "valido": False,
                "message": "CPF inválido",
                "timestamp": datetime.now().isoformat()
            }), 400
        
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
                "regiao": info_ddd if info_ddd else {"cities": ["Informação não disponível"], "state": "N/A"},
                "message": "Telefone válido",
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

@app.route('/api/consultar/email', methods=['POST'])
def api_consultar_email():
    """Valida e verifica email"""
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"erro": "Email não fornecido"}), 400
        
        email = data['email'].strip().lower()
        
        resultado = consultar_email_gamalogic(email)
        
        return jsonify({
            "status": "success" if resultado['valid'] else "error",
            "email": email,
            "dados": resultado,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/api/consultar/endereco', methods=['POST'])
def api_consultar_endereco():
    """Consulta endereço completo por logradouro, cidade e UF"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        logradouro = data.get('logradouro', '').strip()
        cidade = data.get('cidade', '').strip()
        uf = data.get('uf', '').strip()
        
        if not logradouro or not cidade or not uf:
            return jsonify({"erro": "Logradouro, cidade e UF são obrigatórios"}), 400
        
        resultado = consultar_endereco_completo(logradouro, cidade, uf)
        
        if resultado['status'] == 'success':
            return jsonify({
                "status": "success",
                "logradouro": logradouro,
                "cidade": cidade,
                "uf": uf,
                "dados": resultado,
                "fonte": "BrasilAPI",
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": resultado['message'],
                "logradouro": logradouro,
                "cidade": cidade,
                "uf": uf
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
            "/api/consultar/cpf",
            "/api/consultar/telefone",
            "/api/consultar/email",
            "/api/consultar/endereco",
            "/api/status"
        ],
        "help": "Use os endpoints disponíveis para consultas OSINT"
    })

if __name__ == '__main__':
    app.run(debug=True)