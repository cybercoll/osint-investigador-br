// Configurações globais
const API_BASE_URL = '';
const LOADING_DELAY = 500;

// Utilitários
function showLoading(elementId) {
    document.getElementById(elementId).style.display = 'block';
}

function hideLoading(elementId) {
    document.getElementById(elementId).style.display = 'none';
}

function showResult(elementId, content) {
    document.getElementById(elementId).innerHTML = content;
}

function formatCEP(value) {
    return value.replace(/\D/g, '').replace(/(\d{5})(\d{3})/, '$1-$2');
}

function formatCNPJ(value) {
    return value.replace(/\D/g, '').replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
}

// Máscaras de input
document.addEventListener('DOMContentLoaded', function() {
    // Máscara para CEP
    const cepInput = document.getElementById('cepInput');
    if (cepInput) {
        cepInput.addEventListener('input', function(e) {
            e.target.value = formatCEP(e.target.value);
        });
    }

    // Máscara para CNPJ
    const cnpjInput = document.getElementById('cnpjInput');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', function(e) {
            e.target.value = formatCNPJ(e.target.value);
        });
    }

    // Máscara para DDD (apenas números, máximo 2)
    const dddInput = document.getElementById('dddInput');
    if (dddInput) {
        dddInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '').substring(0, 2);
        });
    }

    // Carregar estatísticas do cache ao carregar a página
    carregarEstatisticasCache();
});

// Consulta CEP
document.getElementById('cepForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const cep = document.getElementById('cepInput').value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        showResult('cepResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>CEP deve conter 8 dígitos.</p>
            </div>
        `);
        return;
    }

    showLoading('cepLoading');
    showResult('cepResult', '');

    try {
        const response = await fetch(`/api/cep/${cep}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('cepLoading');
            
            if (data.success) {
                const result = data.data;
                showResult('cepResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Resultado da Consulta</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>CEP:</strong> ${result.cep}</p>
                                <p><strong>Logradouro:</strong> ${result.logradouro}</p>
                                <p><strong>Bairro:</strong> ${result.bairro}</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Cidade:</strong> ${result.localidade}</p>
                                <p><strong>UF:</strong> ${result.uf}</p>
                                <p><strong>IBGE:</strong> ${result.ibge}</p>
                            </div>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success btn-sm" onclick="exportarDados('cep', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar JSON
                            </button>
                            <button class="btn btn-success btn-sm" onclick="exportarCSV('cep', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar CSV
                            </button>
                        </div>
                    </div>
                `);
            } else {
                showResult('cepResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.message}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('cepLoading');
        showResult('cepResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar CEP: ${error.message}</p>
            </div>
        `);
    }
});

// Consulta DDD
document.getElementById('dddForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const ddd = document.getElementById('dddInput').value;
    
    if (ddd.length < 2) {
        showResult('dddResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>DDD deve conter 2 dígitos.</p>
            </div>
        `);
        return;
    }

    showLoading('dddLoading');
    showResult('dddResult', '');

    try {
        const response = await fetch(`/api/ddd/${ddd}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('dddLoading');
            
            if (data.success) {
                const result = data.data;
                showResult('dddResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Resultado da Consulta</h5>
                        <p><strong>Estado:</strong> ${result.state}</p>
                        <p><strong>Cidades:</strong></p>
                        <div class="mt-2">
                            ${result.cities.map(city => `<span class="badge bg-primary me-1 mb-1">${city}</span>`).join('')}
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success btn-sm" onclick="exportarDados('ddd', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar JSON
                            </button>
                            <button class="btn btn-success btn-sm" onclick="exportarCSV('ddd', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar CSV
                            </button>
                        </div>
                    </div>
                `);
            } else {
                showResult('dddResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.message}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('dddLoading');
        showResult('dddResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar DDD: ${error.message}</p>
            </div>
        `);
    }
});

// Consulta CNPJ
document.getElementById('cnpjForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const cnpj = document.getElementById('cnpjInput').value.replace(/\D/g, '');
    const fonte = document.getElementById('fonteSelect').value;
    
    if (cnpj.length !== 14) {
        showResult('cnpjResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>CNPJ deve conter 14 dígitos.</p>
            </div>
        `);
        return;
    }

    showLoading('cnpjLoading');
    showResult('cnpjResult', '');

    try {
        const response = await fetch(`/api/cnpj/${cnpj}?fonte=${fonte}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('cnpjLoading');
            
            if (data.success) {
                const result = data.data;
                let resultHtml = `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Resultado da Consulta</h5>
                        <div class="row">
                `;

                if (fonte === 'brasilapi') {
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj}</p>
                            <p><strong>Razão Social:</strong> ${result.razao_social}</p>
                            <p><strong>Nome Fantasia:</strong> ${result.nome_fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.descricao_situacao_cadastral}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte}</p>
                            <p><strong>Natureza Jurídica:</strong> ${result.natureza_juridica}</p>
                            <p><strong>Capital Social:</strong> R$ ${result.capital_social}</p>
                        </div>
                    `;
                } else {
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj}</p>
                            <p><strong>Nome:</strong> ${result.nome}</p>
                            <p><strong>Fantasia:</strong> ${result.fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.situacao}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte}</p>
                            <p><strong>Natureza:</strong> ${result.natureza_juridica}</p>
                            <p><strong>Capital:</strong> R$ ${result.capital_social}</p>
                        </div>
                    `;
                }

                resultHtml += `
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success btn-sm" onclick="exportarDados('cnpj', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar JSON
                            </button>
                            <button class="btn btn-success btn-sm" onclick="exportarCSV('cnpj', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar CSV
                            </button>
                        </div>
                    </div>
                `;

                showResult('cnpjResult', resultHtml);
            } else {
                showResult('cnpjResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.message}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('cnpjLoading');
        showResult('cnpjResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar CNPJ: ${error.message}</p>
            </div>
        `);
    }
});

// Consulta Municípios
document.getElementById('municipiosForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const uf = document.getElementById('ufSelect').value;
    
    if (!uf) {
        showResult('municipiosResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Selecione um estado.</p>
            </div>
        `);
        return;
    }

    showLoading('municipiosLoading');
    showResult('municipiosResult', '');

    try {
        const response = await fetch(`/api/municipios/${uf}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('municipiosLoading');
            
            if (data.success) {
                const municipios = data.data;
                showResult('municipiosResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Municípios de ${uf}</h5>
                        <p><strong>Total:</strong> ${municipios.length} municípios</p>
                        <div class="table-responsive mt-3" style="max-height: 400px; overflow-y: auto;">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Código IBGE</th>
                                        <th>Nome</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${municipios.map(m => `
                                        <tr>
                                            <td>${m.codigo_ibge}</td>
                                            <td>${m.nome}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success btn-sm" onclick="exportarDados('municipios', ${JSON.stringify(municipios).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar JSON
                            </button>
                            <button class="btn btn-success btn-sm" onclick="exportarCSV('municipios', ${JSON.stringify(municipios).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar CSV
                            </button>
                        </div>
                    </div>
                `);
            } else {
                showResult('municipiosResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.message}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('municipiosLoading');
        showResult('municipiosResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar municípios: ${error.message}</p>
            </div>
        `);
    }
});

// Listar bancos
async function listarBancos() {
    showLoading('bancosLoading');
    showResult('bancosResult', '');

    try {
        const response = await fetch('/api/bancos');
        const data = await response.json();

        setTimeout(() => {
            hideLoading('bancosLoading');
            
            if (data.success) {
                const bancos = data.data;
                showResult('bancosResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Bancos Brasileiros</h5>
                        <p><strong>Total:</strong> ${bancos.length} bancos</p>
                        <div class="table-responsive mt-3" style="max-height: 400px; overflow-y: auto;">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Código</th>
                                        <th>Nome</th>
                                        <th>Nome Completo</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${bancos.map(b => `
                                        <tr>
                                            <td><span class="badge bg-primary">${b.code}</span></td>
                                            <td>${b.name}</td>
                                            <td>${b.fullName}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success btn-sm" onclick="exportarDados('bancos', ${JSON.stringify(bancos).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar JSON
                            </button>
                            <button class="btn btn-success btn-sm" onclick="exportarCSV('bancos', ${JSON.stringify(bancos).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar CSV
                            </button>
                        </div>
                    </div>
                `);
            } else {
                showResult('bancosResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.message}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('bancosLoading');
        showResult('bancosResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao listar bancos: ${error.message}</p>
            </div>
        `);
    }
}

// Buscar banco específico
async function buscarBanco() {
    const codigo = document.getElementById('bancoCodigoInput').value;
    
    if (!codigo) {
        showResult('bancosResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Digite o código do banco.</p>
            </div>
        `);
        return;
    }

    showLoading('bancosLoading');
    showResult('bancosResult', '');

    try {
        const response = await fetch(`/api/bancos/${codigo}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('bancosLoading');
            
            if (data.success) {
                const banco = data.data;
                showResult('bancosResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Banco Encontrado</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Código:</strong> <span class="badge bg-primary">${banco.code}</span></p>
                                <p><strong>Nome:</strong> ${banco.name}</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Nome Completo:</strong> ${banco.fullName}</p>
                            </div>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success btn-sm" onclick="exportarDados('banco', ${JSON.stringify(banco).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar JSON
                            </button>
                            <button class="btn btn-success btn-sm" onclick="exportarCSV('banco', ${JSON.stringify(banco).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar CSV
                            </button>
                        </div>
                    </div>
                `);
            } else {
                showResult('bancosResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.message}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('bancosLoading');
        showResult('bancosResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao buscar banco: ${error.message}</p>
            </div>
        `);
    }
}

// Carregar estatísticas do cache
async function carregarEstatisticasCache() {
    try {
        const response = await fetch('/api/cache/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.data;
            document.getElementById('cacheStats').innerHTML = `
                <div class="row">
                    <div class="col-6">
                        <div class="text-center">
                            <h3 class="text-primary">${stats.total_entries}</h3>
                            <small>Total de Entradas</small>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="text-center">
                            <h3 class="text-success">${stats.valid_entries}</h3>
                            <small>Entradas Válidas</small>
                        </div>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-6">
                        <div class="text-center">
                            <h3 class="text-warning">${stats.expired_entries}</h3>
                            <small>Entradas Expiradas</small>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="text-center">
                            <h3 class="text-info">${(stats.cache_size / 1024).toFixed(2)} KB</h3>
                            <small>Tamanho do Cache</small>
                        </div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('cacheStats').innerHTML = `
            <div class="alert alert-danger">
                Erro ao carregar estatísticas: ${error.message}
            </div>
        `;
    }
}

// Limpar cache
async function limparCache() {
    if (!confirm('Tem certeza que deseja limpar todo o cache?')) {
        return;
    }

    try {
        const response = await fetch('/api/cache/clear', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            document.getElementById('cacheActions').innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> Cache limpo com sucesso!
                </div>
            `;
            carregarEstatisticasCache();
        } else {
            document.getElementById('cacheActions').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> ${data.message}
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('cacheActions').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i> Erro: ${error.message}
            </div>
        `;
    }
}

// Exportar dados
async function exportarDados(tipo, dados) {
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                data: dados,
                format: 'json'
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    } catch (error) {
        alert('Erro ao exportar dados: ' + error.message);
    }
}

// Exportar CSV
async function exportarCSV(tipo, dados) {
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                data: dados,
                format: 'csv'
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    } catch (error) {
        alert('Erro ao exportar CSV: ' + error.message);
    }
}