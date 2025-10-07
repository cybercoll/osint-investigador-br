// Configurações globais
const API_BASE_URL = '';
const LOADING_DELAY = 500;

// Utilitários
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

function showResult(elementId, content) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = content;
    }
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

    // Máscara para Telefone
    const telefoneInput = document.getElementById('telefoneInput');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            } else {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            }
            e.target.value = value;
        });
    }

    // Máscara para Telefone na aba de Dados Pessoais
    const dadosPessoaisTelefoneInput = document.getElementById('dadosPessoaisTelefoneInput');
    if (dadosPessoaisTelefoneInput) {
        dadosPessoaisTelefoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            } else {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            }
            e.target.value = value;
        });
    }

    // Máscara para CPF na aba Direct Data
    const dadosCpfInput = document.getElementById('dadosCpfInput');
    if (dadosCpfInput) {
        dadosCpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            e.target.value = value;
        });
    }

    // Máscara para CPF
    const cpfInput = document.getElementById('cpfInput');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            e.target.value = value;
        });
    }

    // Máscara para Data de Nascimento
    const dataNascimentoInput = document.getElementById('dataNascimentoInput');
    if (dataNascimentoInput) {
        dataNascimentoInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d{2})(\d{4})/, '$1/$2/$3');
            e.target.value = value;
        });
    }

    // Carregar estatísticas do cache ao carregar a página
    carregarEstatisticasCache();
});

// Consulta Telefone
const telefoneForm = document.getElementById('telefoneForm');
if (telefoneForm) {
    telefoneForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const telefoneInput = document.getElementById('telefoneInput');
        if (!telefoneInput) return;
        
        const telefone = telefoneInput.value.replace(/\D/g, '');
        
        if (telefone.length < 10 || telefone.length > 11) {
            showResult('telefoneResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Telefone deve ter 10 ou 11 dígitos (com DDD)</p>
                </div>
            `);
            return;
        }
        
        showLoading('telefoneLoading');
        
        try {
            const response = await fetch(`/api/telefone/${telefone}`);
            const data = await response.json();
            
            setTimeout(() => {
                hideLoading('telefoneLoading');
                
                if (data.success && data.data && data.data.sucesso) {
                    const telefoneData = data.data;
                    
                    // Determinar qual operadora mostrar
                    let operadoraInfo = '';
                    if (telefoneData.operadora) {
                        operadoraInfo = `
                            <div class="info-item">
                                <strong>Operadora:</strong> 
                                <span class="badge bg-success">${telefoneData.operadora}</span>
                                <small class="text-muted">(Confiança: ${telefoneData.confianca_operadora})</small>
                            </div>
                        `;
                    } else if (telefoneData.operadoras_possiveis) {
                        operadoraInfo = `
                            <div class="info-item">
                                <strong>Operadoras Possíveis:</strong> 
                                <span class="badge bg-warning text-dark">${telefoneData.operadoras_possiveis.join(', ')}</span>
                                <small class="text-muted">(Confiança: ${telefoneData.confianca_operadora})</small>
                            </div>
                        `;
                    }
                    
                    showResult('telefoneResult', `
                        <div class="result-card success-card">
                            <h5><i class="fas fa-mobile-alt text-success"></i> Informações do Telefone</h5>
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong>Telefone:</strong> ${telefoneData.telefone_formatado || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Tipo:</strong> 
                                    <span class="badge ${telefoneData.tipo === 'Celular' ? 'bg-success' : 'bg-info'}">${telefoneData.tipo || 'N/A'}</span>
                                </div>
                                <div class="info-item">
                                    <strong>DDD:</strong> ${telefoneData.ddd || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Estado:</strong> ${telefoneData.estado || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Região:</strong> ${telefoneData.regiao || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Válido:</strong> 
                                    <span class="badge ${telefoneData.valido ? 'bg-success' : 'bg-danger'}">${telefoneData.valido ? 'Sim' : 'Não'}</span>
                                </div>
                                ${operadoraInfo}
                            </div>
                            ${telefoneData.observacoes && Array.isArray(telefoneData.observacoes) && telefoneData.observacoes.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Observações:</strong>
                                    <ul class="list-unstyled mt-2">
                                        ${telefoneData.observacoes.map(obs => `<li><i class="fas fa-info-circle text-info"></i> ${obs}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            <div class="mt-3">
                                <button class="btn btn-sm btn-outline-primary" onclick="exportarDados('telefone', ${JSON.stringify(telefoneData).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-download"></i> Exportar JSON
                                </button>
                            </div>
                        </div>
                    `);
                } else {
                    showResult('telefoneResult', `
                        <div class="result-card error-card">
                            <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                            <p>${data.error || 'Erro ao consultar telefone'}</p>
                        </div>
                    `);
                }
            }, LOADING_DELAY);
        } catch (error) {
            hideLoading('telefoneLoading');
            showResult('telefoneResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Erro ao consultar telefone: ${error.message}</p>
                </div>
            `);
        }
    });
}

// Consulta Direct Data por CPF
const dadosCpfForm = document.getElementById('dadosCpfForm');
if (dadosCpfForm) {
    dadosCpfForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const cpfInput = document.getElementById('dadosCpfInput');
        if (!cpfInput) return;
        
        const cpf = cpfInput.value.replace(/\D/g, '');
        
        if (cpf.length !== 11) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>CPF deve ter 11 dígitos</p>
                </div>
            `);
            return;
        }
        
        showLoading('dadosPessoaisLoading');
        
        try {
            const response = await fetch(`/api/directd/consultar-cpf`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cpf: cpf })
            });
            const data = await response.json();
            
            setTimeout(() => {
                hideLoading('dadosPessoaisLoading');
                
                if (data.success && data.data && data.data.retorno) {
                    const pessoaData = data.data.retorno;
                    const metaDados = data.data.metaDados;
                    
                    showResult('dadosPessoaisResult', `
                        <div class="result-card success-card">
                            <h5><i class="fas fa-user-check text-success"></i> Dados Pessoais Encontrados</h5>
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong>Nome:</strong> ${pessoaData.name || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CPF:</strong> ${pessoaData.cpf || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Data de Nascimento:</strong> ${pessoaData.dateOfBirth || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Idade:</strong> ${pessoaData.age || 'N/A'} anos
                                </div>
                                <div class="info-item">
                                    <strong>Gênero:</strong> ${pessoaData.gender || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Nome da Mãe:</strong> ${pessoaData.nameMother || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Faixa Salarial:</strong> ${pessoaData.salaryRange || 'N/A'}
                                </div>
                            </div>
                            
                            ${pessoaData.phones && pessoaData.phones.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Telefones:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.phones.map(phone => `
                                            <div class="info-item">
                                                <span class="badge bg-primary">${phone.phoneNumber}</span>
                                                <small class="text-muted">(${phone.phoneType})</small>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${pessoaData.addresses && pessoaData.addresses.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Endereços:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.addresses.map(address => `
                                            <div class="info-item">
                                                <div>
                                                    <strong>Endereço:</strong> ${address.street}, ${address.number}
                                                    ${address.complement ? ` - ${address.complement}` : ''}
                                                </div>
                                                <div>
                                                    <strong>Bairro:</strong> ${address.neighborhood}
                                                </div>
                                                <div>
                                                    <strong>Cidade:</strong> ${address.city} - ${address.state}
                                                </div>
                                                <div>
                                                    <strong>CEP:</strong> ${address.postalCode}
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${pessoaData.emails && pessoaData.emails.length > 0 ? `
                                <div class="mt-3">
                                    <strong>E-mails:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.emails.map(email => `
                                            <div class="info-item">
                                                <span class="badge bg-info">${email.emailAddress}</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            <div class="mt-3">
                                <small class="text-muted">
                                    <strong>Consulta:</strong> ${metaDados.consultaNome} | 
                                    <strong>Tempo:</strong> ${metaDados.tempoExecucaoMs}ms | 
                                    <strong>API:</strong> ${metaDados.apiVersao}
                                </small>
                            </div>
                            
                            <div class="mt-3">
                                <button class="btn btn-sm btn-outline-primary" onclick="exportarDados('direct-data-cpf', ${JSON.stringify(data.data).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-download"></i> Exportar JSON
                                </button>
                            </div>
                        </div>
                    `);
                } else {
                    showResult('dadosPessoaisResult', `
                        <div class="result-card error-card">
                            <h5><i class="fas fa-exclamation-triangle text-danger"></i> Nenhum dado encontrado</h5>
                            <p>${data.erro || data.error || 'Não foram encontrados dados para o CPF informado'}</p>
                        </div>
                    `);
                }
            }, LOADING_DELAY);
        } catch (error) {
            hideLoading('dadosPessoaisLoading');
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Erro ao consultar dados por CPF: ${error.message}</p>
                </div>
            `);
        }
    });
}

// Consulta Direct Data por Nome
const dadosNomeForm = document.getElementById('dadosNomeForm');
if (dadosNomeForm) {
    dadosNomeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const nomeInput = document.getElementById('dadosNomeInput');
        const sobrenomeInput = document.getElementById('dadosSobrenomeInput');
        const dataNascInput = document.getElementById('dadosDataNascInput');
        
        if (!nomeInput || !sobrenomeInput) return;
        
        const nome = nomeInput.value.trim();
        const sobrenome = sobrenomeInput.value.trim();
        const dataNasc = dataNascInput ? dataNascInput.value : '';
        
        if (!nome || !sobrenome) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Nome e sobrenome são obrigatórios</p>
                </div>
            `);
            return;
        }
        
        showLoading('dadosPessoaisLoading');
        
        try {
            const requestBody = {
                nome: nome,
                sobrenome: sobrenome
            };
            
            if (dataNasc) {
                requestBody.data_nascimento = dataNasc;
            }
            
            const response = await fetch(`/api/directd/consultar-nome`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });
            const data = await response.json();
            
            setTimeout(() => {
                hideLoading('dadosPessoaisLoading');
                
                if (data.success && data.data && data.data.retorno) {
                    const pessoaData = data.data.retorno;
                    const metaDados = data.data.metaDados;
                    
                    showResult('dadosPessoaisResult', `
                        <div class="result-card success-card">
                            <h5><i class="fas fa-user-check text-success"></i> Dados Pessoais Encontrados</h5>
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong>Nome:</strong> ${pessoaData.name || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CPF:</strong> ${pessoaData.cpf || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Data de Nascimento:</strong> ${pessoaData.dateOfBirth || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Idade:</strong> ${pessoaData.age || 'N/A'} anos
                                </div>
                                <div class="info-item">
                                    <strong>Gênero:</strong> ${pessoaData.gender || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Nome da Mãe:</strong> ${pessoaData.nameMother || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Faixa Salarial:</strong> ${pessoaData.salaryRange || 'N/A'}
                                </div>
                            </div>
                            
                            ${pessoaData.phones && pessoaData.phones.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Telefones:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.phones.map(phone => `
                                            <div class="info-item">
                                                <span class="badge bg-primary">${phone.phoneNumber}</span>
                                                <small class="text-muted">(${phone.phoneType})</small>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${pessoaData.addresses && pessoaData.addresses.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Endereços:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.addresses.map(address => `
                                            <div class="info-item">
                                                <div>
                                                    <strong>Endereço:</strong> ${address.street}, ${address.number}
                                                    ${address.complement ? ` - ${address.complement}` : ''}
                                                </div>
                                                <div>
                                                    <strong>Bairro:</strong> ${address.neighborhood}
                                                </div>
                                                <div>
                                                    <strong>Cidade:</strong> ${address.city} - ${address.state}
                                                </div>
                                                <div>
                                                    <strong>CEP:</strong> ${address.postalCode}
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${pessoaData.emails && pessoaData.emails.length > 0 ? `
                                <div class="mt-3">
                                    <strong>E-mails:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.emails.map(email => `
                                            <div class="info-item">
                                                <span class="badge bg-info">${email.emailAddress}</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            <div class="mt-3">
                                <small class="text-muted">
                                    <strong>Consulta:</strong> ${metaDados.consultaNome} | 
                                    <strong>Tempo:</strong> ${metaDados.tempoExecucaoMs}ms | 
                                    <strong>API:</strong> ${metaDados.apiVersao}
                                </small>
                            </div>
                            
                            <div class="mt-3">
                                <button class="btn btn-sm btn-outline-primary" onclick="exportarDados('direct-data-nome', ${JSON.stringify(data.data).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-download"></i> Exportar JSON
                                </button>
                            </div>
                        </div>
                    `);
                } else {
                    showResult('dadosPessoaisResult', `
                        <div class="result-card error-card">
                            <h5><i class="fas fa-exclamation-triangle text-danger"></i> Nenhum dado encontrado</h5>
                            <p>${data.erro || data.error || 'Não foram encontrados dados para o nome informado'}</p>
                        </div>
                    `);
                }
            }, LOADING_DELAY);
        } catch (error) {
            hideLoading('dadosPessoaisLoading');
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Erro ao consultar dados por nome: ${error.message}</p>
                </div>
            `);
        }
    });
}

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
                const fonte = result.fonte ? ` (via ${result.fonte})` : '';
                showResult('cepResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Resultado da Consulta${fonte}</h5>
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
                                ${result.coordenadas && result.coordenadas.coordinates ? 
                                    `<p><strong>Coordenadas:</strong> ${result.coordenadas.coordinates.lat}, ${result.coordenadas.coordinates.lng}</p>` : ''}
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
                        <p>${data.error || data.message || 'Erro desconhecido'}</p>
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
                        <p><strong>Estado:</strong> ${result.estado || 'N/A'}</p>
                        <p><strong>Cidades:</strong></p>
                        <div class="mt-2">
                            ${(result.cidades || []).map(city => `<span class="badge bg-primary me-1 mb-1">${city}</span>`).join('')}
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
                        <p>${data.error || data.message || 'Erro ao consultar DDD'}</p>
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
            
            if (data && !data.erro) {
                const result = data;
                let resultHtml = `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Resultado da Consulta</h5>
                        <div class="row">
                `;

                if (fonte === 'brasilapi') {
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj || 'N/A'}</p>
                            <p><strong>Razão Social:</strong> ${result.razao_social || 'N/A'}</p>
                            <p><strong>Nome Fantasia:</strong> ${result.nome_fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.situacao || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte || 'N/A'}</p>
                            <p><strong>Natureza Jurídica:</strong> ${result.natureza_juridica || 'N/A'}</p>
                            <p><strong>Capital Social:</strong> R$ ${result.capital_social || 'N/A'}</p>
                        </div>
                    `;
                } else if (fonte === 'cnpja') {
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj || 'N/A'}</p>
                            <p><strong>Razão Social:</strong> ${result.razao_social || 'N/A'}</p>
                            <p><strong>Nome Fantasia:</strong> ${result.nome_fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.situacao || 'N/A'}</p>
                            <p><strong>Data de Abertura:</strong> ${result.data_abertura || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte || 'N/A'}</p>
                            <p><strong>Natureza Jurídica:</strong> ${result.natureza_juridica || 'N/A'}</p>
                            <p><strong>Capital Social:</strong> R$ ${result.capital_social ? Number(result.capital_social).toLocaleString('pt-BR') : 'N/A'}</p>
                            <p><strong>Fonte:</strong> ${result.fonte || 'N/A'}</p>
                        </div>
                    `;
                    
                    // Adicionar informações de endereço se disponível
                    if (result.endereco && Object.keys(result.endereco).length > 0) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-map-marker-alt"></i> Endereço</h6>
                                <p><strong>Logradouro:</strong> ${result.endereco.logradouro || 'N/A'}, ${result.endereco.numero || 'S/N'}</p>
                                <p><strong>Bairro:</strong> ${result.endereco.bairro || 'N/A'}</p>
                                <p><strong>Cidade/UF:</strong> ${result.endereco.municipio || 'N/A'}/${result.endereco.uf || 'N/A'}</p>
                                <p><strong>CEP:</strong> ${result.endereco.cep || 'N/A'}</p>
                            </div>
                        `;
                    }
                    
                    // Adicionar telefones se disponível
                    if (result.telefones && result.telefones.length > 0) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-phone"></i> Telefones</h6>
                                ${result.telefones.map(tel => `<p>(${tel.area}) ${tel.number}</p>`).join('')}
                            </div>
                        `;
                    }
                    
                    // Adicionar atividades se disponível
                    if (result.atividade_principal && result.atividade_principal.length > 0) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-briefcase"></i> Atividade Principal</h6>
                                <p>${result.atividade_principal[0].text || 'N/A'}</p>
                            </div>
                        `;
                    }
                } else {
                    // Para outras fontes (receitaws, etc.)
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj || 'N/A'}</p>
                            <p><strong>Nome:</strong> ${result.nome || result.razao_social || 'N/A'}</p>
                            <p><strong>Fantasia:</strong> ${result.fantasia || result.nome_fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.situacao || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte || 'N/A'}</p>
                            <p><strong>Natureza:</strong> ${result.natureza_juridica || 'N/A'}</p>
                            <p><strong>Capital:</strong> R$ ${result.capital_social || 'N/A'}</p>
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
                        <p>${data.erro || data.message || 'Erro ao consultar CNPJ'}</p>
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
        const response = await fetch(`/api/consultar/municipios/${uf}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('municipiosLoading');
            
            if (data && data.municipios && Array.isArray(data.municipios)) {
                const municipios = data.municipios;
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
                                            <td>${m.codigo_ibge || 'N/A'}</td>
                                            <td>${m.nome || 'N/A'}</td>
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
                        <p>${data.erro || data.message || 'Erro ao consultar municípios'}</p>
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
        const response = await fetch('/api/consultar/bancos');
        const data = await response.json();

        setTimeout(() => {
            hideLoading('bancosLoading');
            
            if (data.bancos && Array.isArray(data.bancos)) {
                const bancos = data.bancos;
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
                                            <td><span class="badge bg-primary">${b.code || 'N/A'}</span></td>
                                            <td>${b.name || 'N/A'}</td>
                                            <td>${b.fullName || 'N/A'}</td>
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
                        <p>${data.erro || 'Erro ao carregar dados dos bancos'}</p>
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
        const response = await fetch(`/api/consultar/banco/${codigo}`);
        const data = await response.json();

        setTimeout(() => {
            hideLoading('bancosLoading');
            
            if (data.banco) {
                const banco = data.banco;
                showResult('bancosResult', `
                    <div class="result-card">
                        <h5><i class="fas fa-check-circle text-success"></i> Banco Encontrado</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Código:</strong> <span class="badge bg-primary">${banco.codigo || 'N/A'}</span></p>
                                <p><strong>Nome:</strong> ${banco.nome || 'N/A'}</p>
                                <p><strong>Nome Completo:</strong> ${banco.nome_completo || 'N/A'}</p>
                            </div>
                            <div class="col-md-6">
                                ${banco.ispb ? `<p><strong>ISPB:</strong> ${banco.ispb}</p>` : ''}
                                ${banco.swift ? `<p><strong>SWIFT:</strong> ${banco.swift}</p>` : ''}
                                ${banco.cidade ? `<p><strong>Cidade:</strong> ${banco.cidade}</p>` : ''}
                                ${banco.pais ? `<p><strong>País:</strong> ${banco.pais}</p>` : ''}
                                <p><strong>Fonte:</strong> <span class="badge bg-info">${banco.fonte || 'N/A'}</span></p>
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
                        <p>${data.erro || 'Banco não encontrado'}</p>
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
            
            // Reload da página após 2 segundos para garantir que o cache foi limpo
            setTimeout(() => {
                location.reload();
            }, 2000);
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

// Consulta Dados Pessoais
const dadosPessoaisForm = document.getElementById('dadosPessoaisForm');
if (dadosPessoaisForm) {
    dadosPessoaisForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const telefone = document.getElementById('dadosPessoaisTelefoneInput').value.replace(/\D/g, '');
        const cpf = document.getElementById('dadosPessoaisCpfInput') ? document.getElementById('dadosPessoaisCpfInput').value.replace(/\D/g, '') : '';
        const nome = document.getElementById('dadosPessoaisNomeInput') ? document.getElementById('dadosPessoaisNomeInput').value.trim() : '';
        const dataNascimento = document.getElementById('dadosPessoaisDataNascInput') ? document.getElementById('dadosPessoaisDataNascInput').value.replace(/\D/g, '') : '';
        
        // Verificar se pelo menos um campo foi preenchido
        if (!telefone && !cpf && !nome && !dataNascimento) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Preencha pelo menos um campo para realizar a consulta</p>
                </div>
            `);
            return;
        }
        
        // Validações específicas
        if (telefone && (telefone.length < 10 || telefone.length > 11)) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Telefone deve ter 10 ou 11 dígitos (com DDD)</p>
                </div>
            `);
            return;
        }
        
        if (cpf && cpf.length !== 11) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>CPF deve ter 11 dígitos</p>
                </div>
            `);
            return;
        }
        
        if (dataNascimento && dataNascimento.length !== 8) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Data de nascimento deve estar no formato DD/MM/AAAA</p>
                </div>
            `);
            return;
        }
        
        showLoading('dadosPessoaisLoading');
        
        try {
            // Usar a API avançada se houver múltiplos campos ou usar a API simples para telefone apenas
            let response;
            if (cpf || nome || dataNascimento || (telefone && (cpf || nome || dataNascimento))) {
                // Consulta avançada
                const requestData = {};
                if (telefone) requestData.telefone = telefone;
                if (cpf) requestData.cpf = cpf;
                if (nome) requestData.nome = nome;
                if (dataNascimento) {
                    // Converter para formato YYYY-MM-DD
                    const day = dataNascimento.substring(0, 2);
                    const month = dataNascimento.substring(2, 4);
                    const year = dataNascimento.substring(4, 8);
                    requestData.data_nascimento = `${year}-${month}-${day}`;
                }
                
                response = await fetch('/api/consultar/dados-pessoais-avancado', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });
            } else {
                // Consulta simples por telefone
                response = await fetch(`/api/dados-pessoais/${telefone}`);
            }
            
            const data = await response.json();
            
            setTimeout(() => {
                hideLoading('dadosPessoaisLoading');
                
                if ((data.success && data.data) || (!data.erro && data.dados_encontrados)) {
                    const pessoaData = data.data || data;
                    
                    showResult('dadosPessoaisResult', `
                        <div class="result-card success-card">
                            <h5><i class="fas fa-user text-success"></i> Dados Pessoais Encontrados</h5>
                            ${pessoaData.nivel_confiabilidade ? `
                                <div class="alert alert-info">
                                    <strong>Nível de Confiabilidade:</strong> ${pessoaData.nivel_confiabilidade}
                                </div>
                            ` : ''}
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong>Nome:</strong> ${pessoaData.dados_pessoais?.nome || pessoaData.nome || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Telefone:</strong> ${pessoaData.telefone || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Email:</strong> ${pessoaData.dados_pessoais?.email || pessoaData.email || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CPF:</strong> ${pessoaData.dados_pessoais?.cpf || pessoaData.cpf || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Data de Nascimento:</strong> ${pessoaData.dados_pessoais?.data_nascimento || pessoaData.data_nascimento || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Endereço:</strong> ${pessoaData.dados_pessoais?.endereco || pessoaData.endereco || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Cidade:</strong> ${pessoaData.dados_pessoais?.cidade || pessoaData.cidade || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Estado:</strong> ${pessoaData.dados_pessoais?.estado || pessoaData.estado || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CEP:</strong> ${pessoaData.dados_pessoais?.cep || pessoaData.cep || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Renda Estimada:</strong> ${pessoaData.dados_pessoais?.renda_estimada || pessoaData.renda_estimada || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Profissão:</strong> ${pessoaData.dados_pessoais?.profissao || pessoaData.profissao || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Estado Civil:</strong> ${pessoaData.dados_pessoais?.estado_civil || pessoaData.estado_civil || 'N/A'}
                                </div>
                            </div>
                            ${pessoaData.redes_sociais && Object.keys(pessoaData.redes_sociais).length > 0 ? `
                                <div class="mt-3">
                                    <strong>Redes Sociais:</strong>
                                    <div class="mt-2">
                                        ${Object.entries(pessoaData.redes_sociais).map(([rede, perfil]) => `
                                            <div class="info-item">
                                                <strong>${rede.charAt(0).toUpperCase() + rede.slice(1)}:</strong> 
                                                <a href="${perfil}" target="_blank" class="text-primary">${perfil}</a>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            ${pessoaData.observacoes && Array.isArray(pessoaData.observacoes) && pessoaData.observacoes.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Observações:</strong>
                                    <ul class="list-unstyled mt-2">
                                        ${pessoaData.observacoes.map(obs => `<li><i class="fas fa-info-circle text-info"></i> ${obs}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            ${pessoaData.fontes_consultadas && Array.isArray(pessoaData.fontes_consultadas) && pessoaData.fontes_consultadas.length > 0 ? `
                                <div class="mt-3">
                                    <strong>Fontes Consultadas:</strong>
                                    <div class="mt-2">
                                        ${pessoaData.fontes_consultadas.map(fonte => `
                                            <span class="badge badge-secondary mr-1">${fonte}</span>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            ${pessoaData.cruzamento_dados && Object.keys(pessoaData.cruzamento_dados).length > 0 ? `
                                <div class="mt-3">
                                    <strong>Cruzamento de Dados:</strong>
                                    <div class="mt-2">
                                        ${Object.entries(pessoaData.cruzamento_dados).map(([campo, status]) => `
                                            <div class="info-item">
                                                <strong>${campo}:</strong> 
                                                <span class="badge ${status === 'Confirmado' ? 'badge-success' : status === 'Conflito' ? 'badge-warning' : 'badge-secondary'}">${status}</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            <div class="mt-3">
                                <button class="btn btn-sm btn-outline-primary" onclick="exportarDados('dados-pessoais', ${JSON.stringify(pessoaData).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-download"></i> Exportar JSON
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="exportarCSV('dados-pessoais', ${JSON.stringify(pessoaData).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-file-csv"></i> Exportar CSV
                                </button>
                            </div>
                        </div>
                    `);
                } else {
                    showResult('dadosPessoaisResult', `
                        <div class="result-card error-card">
                            <h5><i class="fas fa-exclamation-triangle text-danger"></i> Nenhum dado encontrado</h5>
                            <p>${data.erro || data.error || 'Não foram encontrados dados pessoais com os critérios informados'}</p>
                        </div>
                    `);
                }
            }, LOADING_DELAY);
        } catch (error) {
            hideLoading('dadosPessoaisLoading');
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Erro ao consultar dados pessoais: ${error.message}</p>
                </div>
            `);
        }
    });
}