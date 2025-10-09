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
                
                if (data.status === 'success' && data.data) {
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
                            <p>${data.erro || data.message || 'Erro ao consultar telefone'}</p>
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

// Funções para consulta de documentos individuais
async function consultarTituloEleitor() {
    const titulo = document.getElementById('dadosPessoaisTituloEleitorInput').value.trim();
    const nome = document.getElementById('dadosPessoaisNomeInput').value.trim();
    
    if (!titulo) {
        alert('Por favor, informe o número do título de eleitor.');
        return;
    }
    
    showLoading('dadosPessoaisLoading');
    
    try {
        const response = await fetch('/api/documentos/titulo-eleitor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                titulo: titulo,
                nome: nome
            })
        });
        
        const data = await response.json();
        
        setTimeout(() => {
            hideLoading('dadosPessoaisLoading');
            
            if (data.success && data.data) {
                showResult('dadosPessoaisResult', `
                    <div class="result-card success-card">
                        <h5><i class="fas fa-vote-yea text-success"></i> Título de Eleitor</h5>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>Título:</strong> ${data.data.titulo_eleitor || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Status:</strong> ${data.data.status || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Formato:</strong> ${data.data.formato_valido ? 'Válido' : 'Inválido'}
                            </div>
                            <div class="info-item">
                                <strong>Observação:</strong> ${data.data.observacao || 'N/A'}
                            </div>
                        </div>
                        <div class="metadata">
                            <small><strong>Fonte:</strong> ${data.metadata.fonte || 'N/A'}</small><br>
                            <small><strong>Timestamp:</strong> ${data.metadata.timestamp || 'N/A'}</small>
                        </div>
                    </div>
                `);
            } else {
                showResult('dadosPessoaisResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.error || 'Erro ao consultar título de eleitor'}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('dadosPessoaisLoading');
        showResult('dadosPessoaisResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar título de eleitor: ${error.message}</p>
            </div>
        `);
    }
}

async function consultarCNS() {
    const cns = document.getElementById('dadosPessoaisCnsInput').value.trim();
    const nome = document.getElementById('dadosPessoaisNomeInput').value.trim();
    
    if (!cns) {
        alert('Por favor, informe o número do CNS.');
        return;
    }
    
    showLoading('dadosPessoaisLoading');
    
    try {
        const response = await fetch('/api/documentos/cns', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cns: cns,
                nome: nome
            })
        });
        
        const data = await response.json();
        
        setTimeout(() => {
            hideLoading('dadosPessoaisLoading');
            
            if (data.success && data.data) {
                showResult('dadosPessoaisResult', `
                    <div class="result-card success-card">
                        <h5><i class="fas fa-id-card text-success"></i> CNS - Cartão Nacional de Saúde</h5>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>CNS:</strong> ${data.data.cns || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Status:</strong> ${data.data.status || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Formato:</strong> ${data.data.formato_valido ? 'Válido' : 'Inválido'}
                            </div>
                            <div class="info-item">
                                <strong>Observação:</strong> ${data.data.observacao || 'N/A'}
                            </div>
                        </div>
                        <div class="metadata">
                            <small><strong>Fonte:</strong> ${data.metadata.fonte || 'N/A'}</small><br>
                            <small><strong>Timestamp:</strong> ${data.metadata.timestamp || 'N/A'}</small>
                        </div>
                    </div>
                `);
            } else {
                showResult('dadosPessoaisResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.error || 'Erro ao consultar CNS'}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('dadosPessoaisLoading');
        showResult('dadosPessoaisResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar CNS: ${error.message}</p>
            </div>
        `);
    }
}

async function consultarPIS() {
    const pis = document.getElementById('dadosPessoaisPisInput').value.trim();
    const nome = document.getElementById('dadosPessoaisNomeInput').value.trim();
    
    if (!pis) {
        alert('Por favor, informe o número do PIS.');
        return;
    }
    
    showLoading('dadosPessoaisLoading');
    
    try {
        const response = await fetch('/api/documentos/pis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pis: pis,
                nome: nome
            })
        });
        
        const data = await response.json();
        
        setTimeout(() => {
            hideLoading('dadosPessoaisLoading');
            
            if (data.success && data.data) {
                showResult('dadosPessoaisResult', `
                    <div class="result-card success-card">
                        <h5><i class="fas fa-id-badge text-success"></i> PIS/PASEP</h5>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>PIS:</strong> ${data.data.pis || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Status:</strong> ${data.data.status || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Formato:</strong> ${data.data.formato_valido ? 'Válido' : 'Inválido'}
                            </div>
                            <div class="info-item">
                                <strong>Observação:</strong> ${data.data.observacao || 'N/A'}
                            </div>
                        </div>
                        <div class="metadata">
                            <small><strong>Fonte:</strong> ${data.metadata.fonte || 'N/A'}</small><br>
                            <small><strong>Timestamp:</strong> ${data.metadata.timestamp || 'N/A'}</small>
                        </div>
                    </div>
                `);
            } else {
                showResult('dadosPessoaisResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.error || 'Erro ao consultar PIS'}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('dadosPessoaisLoading');
        showResult('dadosPessoaisResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar PIS: ${error.message}</p>
            </div>
        `);
    }
}

async function consultarRG() {
    const rg = document.getElementById('dadosPessoaisRgInput').value.trim();
    
    showLoading('dadosPessoaisLoading');
    
    try {
        const response = await fetch('/api/documentos/rg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                rg: rg,
                estado: 'SP' // Padrão
            })
        });
        
        const data = await response.json();
        
        setTimeout(() => {
            hideLoading('dadosPessoaisLoading');
            
            if (data.success && data.data) {
                showResult('dadosPessoaisResult', `
                    <div class="result-card warning-card">
                        <h5><i class="fas fa-id-card text-warning"></i> RG - Registro Geral</h5>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>RG:</strong> ${data.data.rg || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Estado:</strong> ${data.data.estado || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Status:</strong> ${data.data.status || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Observação:</strong> ${data.data.observacao || 'N/A'}
                            </div>
                        </div>
                        <div class="metadata">
                            <small><strong>Fonte:</strong> ${data.metadata.fonte || 'N/A'}</small><br>
                            <small><strong>Timestamp:</strong> ${data.metadata.timestamp || 'N/A'}</small>
                        </div>
                    </div>
                `);
            } else {
                showResult('dadosPessoaisResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.error || 'Erro ao consultar RG'}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('dadosPessoaisLoading');
        showResult('dadosPessoaisResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar RG: ${error.message}</p>
            </div>
        `);
    }
}

async function consultarCNH() {
    const cnh = document.getElementById('dadosPessoaisCnhInput').value.trim();
    
    showLoading('dadosPessoaisLoading');
    
    try {
        const response = await fetch('/api/documentos/cnh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cnh: cnh
            })
        });
        
        const data = await response.json();
        
        setTimeout(() => {
            hideLoading('dadosPessoaisLoading');
            
            if (data.success && data.data) {
                showResult('dadosPessoaisResult', `
                    <div class="result-card warning-card">
                        <h5><i class="fas fa-car text-warning"></i> CNH - Carteira Nacional de Habilitação</h5>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>CNH:</strong> ${data.data.cnh || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Status:</strong> ${data.data.status || 'N/A'}
                            </div>
                            <div class="info-item">
                                <strong>Observação:</strong> ${data.data.observacao || 'N/A'}
                            </div>
                        </div>
                        <div class="metadata">
                            <small><strong>Fonte:</strong> ${data.metadata.fonte || 'N/A'}</small><br>
                            <small><strong>Timestamp:</strong> ${data.metadata.timestamp || 'N/A'}</small>
                        </div>
                    </div>
                `);
            } else {
                showResult('dadosPessoaisResult', `
                    <div class="result-card error-card">
                        <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                        <p>${data.error || 'Erro ao consultar CNH'}</p>
                    </div>
                `);
            }
        }, LOADING_DELAY);
    } catch (error) {
        hideLoading('dadosPessoaisLoading');
        showResult('dadosPessoaisResult', `
            <div class="result-card error-card">
                <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                <p>Erro ao consultar CNH: ${error.message}</p>
            </div>
        `);
    }
}

// Funções para menus interativos das tabelas
function createTableMenu(rowData, rowType) {
    const menuId = `menu-${Math.random().toString(36).substr(2, 9)}`;
    
    let menuItems = '';
    
    // Itens comuns para todos os tipos
    menuItems += `
        <button class="table-menu-item" onclick="copyToClipboard('${JSON.stringify(rowData).replace(/'/g, "\\'")}')">
            <i class="fas fa-copy"></i> Copiar Dados
        </button>
        <button class="table-menu-item" onclick="exportSingleItem('${rowType}', '${JSON.stringify(rowData).replace(/'/g, "\\'")}')">
            <i class="fas fa-download"></i> Exportar Item
        </button>
        <div class="table-menu-divider"></div>
    `;
    
    // Itens específicos por tipo
    switch(rowType) {
        case 'municipio':
            menuItems += `
                <button class="table-menu-item" onclick="searchRelatedData('municipio', '${rowData.codigo_ibge}')">
                    <i class="fas fa-search"></i> Buscar Dados Relacionados
                </button>
                <button class="table-menu-item" onclick="viewOnMap('${rowData.nome}')">
                    <i class="fas fa-map-marker-alt"></i> Ver no Mapa
                </button>
            `;
            break;
        case 'banco':
            menuItems += `
                <button class="table-menu-item" onclick="searchBankDetails('${rowData.code}')">
                    <i class="fas fa-info-circle"></i> Detalhes do Banco
                </button>
                <button class="table-menu-item" onclick="searchBankAgencies('${rowData.code}')">
                    <i class="fas fa-building"></i> Buscar Agências
                </button>
            `;
            break;
        case 'cache':
            menuItems += `
                <button class="table-menu-item" onclick="viewCacheDetails('${rowData.data_execucao}')">
                    <i class="fas fa-eye"></i> Ver Detalhes
                </button>
                <button class="table-menu-item" onclick="deleteCacheEntry('${rowData.data_execucao}')">
                    <i class="fas fa-trash text-danger"></i> Remover Entrada
                </button>
            `;
            break;
        case 'pessoa':
            menuItems += `
                <button class="table-menu-item" onclick="viewPersonDetails('${rowData.cpf || rowData.nome}')">
                    <i class="fas fa-user"></i> Ver Perfil Completo
                </button>
                <button class="table-menu-item" onclick="searchRelatedPersons('${rowData.cpf || rowData.nome}')">
                    <i class="fas fa-users"></i> Buscar Relacionados
                </button>
                <button class="table-menu-item" onclick="addToFavorites('${JSON.stringify(rowData).replace(/'/g, "\\'")}')">
                    <i class="fas fa-star"></i> Adicionar aos Favoritos
                </button>
            `;
            break;
        default:
            menuItems += `
                <button class="table-menu-item" onclick="viewItemDetails('${JSON.stringify(rowData).replace(/'/g, "\\'")}')">
                    <i class="fas fa-eye"></i> Ver Detalhes
                </button>
            `;
    }
    
    return `
        <div class="table-menu">
            <button class="table-menu-btn table-tooltip" data-tooltip="Ações" onclick="toggleTableMenu('${menuId}')">
                <i class="fas fa-ellipsis-v"></i>
            </button>
            <div class="table-menu-dropdown" id="${menuId}">
                ${menuItems}
            </div>
        </div>
    `;
}

function toggleTableMenu(menuId) {
    // Fechar todos os outros menus
    document.querySelectorAll('.table-menu-dropdown').forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove('show');
        }
    });
    
    // Toggle do menu atual
    const menu = document.getElementById(menuId);
    if (menu) {
        menu.classList.toggle('show');
    }
}

// Fechar menus quando clicar fora
document.addEventListener('click', function(event) {
    if (!event.target.closest('.table-menu')) {
        document.querySelectorAll('.table-menu-dropdown').forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

// Funções de ação dos menus
function copyToClipboard(data) {
    try {
        const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
        const text = JSON.stringify(parsedData, null, 2);
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Dados copiados para a área de transferência!', 'success');
            });
        } else {
            // Fallback para navegadores mais antigos
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Dados copiados para a área de transferência!', 'success');
        }
    } catch (error) {
        showNotification('Erro ao copiar dados', 'error');
    }
}

function exportSingleItem(type, data) {
    try {
        const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
        const blob = new Blob([JSON.stringify(parsedData, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${type}_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showNotification('Item exportado com sucesso!', 'success');
    } catch (error) {
        showNotification('Erro ao exportar item', 'error');
    }
}

function searchRelatedData(type, id) {
    showNotification(`Buscando dados relacionados para ${type}: ${id}`, 'info');
    // Implementar lógica específica de busca relacionada
}

function viewOnMap(location) {
    const url = `https://www.google.com/maps/search/${encodeURIComponent(location)}`;
    window.open(url, '_blank');
}

function searchBankDetails(bankCode) {
    // Implementar busca de detalhes do banco
    showNotification(`Buscando detalhes do banco: ${bankCode}`, 'info');
}

function searchBankAgencies(bankCode) {
    // Implementar busca de agências do banco
    showNotification(`Buscando agências do banco: ${bankCode}`, 'info');
}

function viewCacheDetails(timestamp) {
    // Implementar visualização de detalhes do cache
    showNotification(`Visualizando detalhes do cache: ${timestamp}`, 'info');
}

function deleteCacheEntry(timestamp) {
    if (confirm('Tem certeza que deseja remover esta entrada do cache?')) {
        // Implementar remoção da entrada do cache
        showNotification(`Removendo entrada do cache: ${timestamp}`, 'info');
    }
}

function viewPersonDetails(identifier) {
    // Implementar visualização de detalhes da pessoa
    showNotification(`Visualizando perfil: ${identifier}`, 'info');
}

function searchRelatedPersons(identifier) {
    // Implementar busca de pessoas relacionadas
    showNotification(`Buscando pessoas relacionadas: ${identifier}`, 'info');
}

function addToFavorites(data) {
    try {
        const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
        let favorites = JSON.parse(localStorage.getItem('osint_favorites') || '[]');
        
        // Verificar se já existe nos favoritos
        const exists = favorites.some(fav => 
            (fav.cpf && fav.cpf === parsedData.cpf) || 
            (fav.nome && fav.nome === parsedData.nome)
        );
        
        if (!exists) {
            favorites.push({
                ...parsedData,
                added_at: new Date().toISOString()
            });
            localStorage.setItem('osint_favorites', JSON.stringify(favorites));
            showNotification('Adicionado aos favoritos!', 'success');
        } else {
            showNotification('Item já está nos favoritos', 'warning');
        }
    } catch (error) {
        showNotification('Erro ao adicionar aos favoritos', 'error');
    }
}

function viewItemDetails(data) {
    try {
        const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
        
        // Criar modal para exibir detalhes
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Detalhes do Item</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <pre class="bg-light p-3 rounded">${JSON.stringify(parsedData, null, 2)}</pre>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        <button type="button" class="btn btn-primary" onclick="copyToClipboard('${JSON.stringify(parsedData).replace(/'/g, "\\'")}')">
                            <i class="fas fa-copy"></i> Copiar
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Remover modal após fechar
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    } catch (error) {
        showNotification('Erro ao exibir detalhes', 'error');
    }
}

function showNotification(message, type = 'info') {
    // Criar notificação toast
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'info'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-circle' : 'info-circle'}"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Adicionar container de toasts se não existir
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
    
    // Remover toast após ocultar
    toast.addEventListener('hidden.bs.toast', () => {
        toastContainer.removeChild(toast);
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
            const response = await fetch(`/api/consultar/cpf-completo`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cpf: cpf })
            });
            const data = await response.json();
            
            setTimeout(() => {
                hideLoading('dadosPessoaisLoading');
                
                if (data.status === 'success' && data.dados) {
                    const pessoaData = data.dados;
                    
                    showResult('dadosPessoaisResult', `
                        <div class="result-card success-card">
                            <h5><i class="fas fa-user-check text-success"></i> Dados Pessoais Encontrados</h5>
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong>Nome:</strong> ${pessoaData.nome || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CPF:</strong> ${pessoaData.cpf || 'N/A'}
                                </div>
                                ${pessoaData.idade ? `<div class="info-item">
                                    <strong>Idade:</strong> ${pessoaData.idade} anos
                                </div>` : ''}
                                ${pessoaData.sexo ? `<div class="info-item">
                                    <strong>Sexo:</strong> ${pessoaData.sexo}
                                </div>` : ''}
                                ${pessoaData.mae ? `<div class="info-item">
                                    <strong>Nome da Mãe:</strong> ${pessoaData.mae}
                                </div>` : ''}
                                ${pessoaData.data_nascimento ? `<div class="info-item">
                                    <strong>Data de Nascimento:</strong> ${pessoaData.data_nascimento}
                                </div>` : ''}
                                ${pessoaData.telefones && pessoaData.telefones.length > 0 ? `<div class="info-item">
                                    <strong>Telefones:</strong> ${pessoaData.telefones.join(', ')}
                                </div>` : ''}
                                ${pessoaData.emails && pessoaData.emails.length > 0 ? `<div class="info-item">
                                    <strong>Emails:</strong> ${pessoaData.emails.join(', ')}
                                </div>` : ''}
                                ${pessoaData.enderecos && pessoaData.enderecos.length > 0 ? `<div class="info-item">
                                    <strong>Endereços:</strong><br>
                                    ${pessoaData.enderecos.map(endereco => 
                                        `${endereco.endereco}, ${endereco.bairro}, ${endereco.cidade}/${endereco.estado} - CEP: ${endereco.cep}`
                                    ).join('<br>')}
                                </div>` : ''}
                                <div class="info-item">
                                    <strong>RG:</strong> ${pessoaData.rg || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CNH:</strong> ${pessoaData.cnh || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>Título Eleitor:</strong> ${pessoaData.titulo_eleitor || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>PIS:</strong> ${pessoaData.pis || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong>CNS:</strong> ${pessoaData.cns || 'N/A'}
                                </div>
                            </div>
                            
                            <div class="mt-3">
                                <small class="text-muted">Fonte: ${data.fonte || 'API Externa'}</small><br>
                                <button class="btn btn-sm btn-outline-primary mt-2" onclick="exportarDados('cpf-completo', ${JSON.stringify(data).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-download"></i> Exportar JSON
                                </button>
                            </div>
                        </div>
                    `);
                } else if (data.status === 'not_found') {
                    showResult('dadosPessoaisResult', `
                        <div class="result-card warning-card">
                            <h5><i class="fas fa-info-circle text-warning"></i> CPF não encontrado</h5>
                            <p>${data.message}</p>
                        </div>
                    `);
                } else {
                    showResult('dadosPessoaisResult', `
                        <div class="result-card error-card">
                            <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                            <p>${data.erro || data.message || 'Erro desconhecido'}</p>
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
                
                if (data.success && data.data && data.data.data) {
                    const pessoaData = data.data.data;
                    const metaDados = data.data.metadata;
                    
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
                                                ${phone.phoneType ? `<small class="text-muted">(${phone.phoneType})</small>` : ''}
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
                                                    <strong>Endereço:</strong> ${address.street || 'N/A'}, ${address.number || 'N/A'}
                                                    ${address.complement ? ` - ${address.complement}` : ''}
                                                </div>
                                                <div>
                                                    <strong>Bairro:</strong> ${address.neighborhood || 'N/A'}
                                                </div>
                                                <div>
                                                    <strong>Cidade:</strong> ${address.city || 'N/A'} - ${address.state || 'N/A'}
                                                </div>
                                                <div>
                                                    <strong>CEP:</strong> ${address.postalCode || 'N/A'}
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
                                    <strong>Fonte:</strong> ${data.fonte || 'Direct Data API'} | 
                                    <strong>Timestamp:</strong> ${data.timestamp}
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
            
            if (data.status === 'success' && data.dados) {
                const result = data.dados;
                const fonte = data.fonte ? ` (via ${data.fonte})` : '';
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
                        <p>${data.erro || data.message || 'CEP não encontrado'}</p>
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
            
            if (data && data.status === 'success' && data.dados) {
                const result = data.dados;
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
                            <p><strong>Nome Fantasia:</strong> ${result.nome_fantasia || 'Não informado'}</p>
                            <p><strong>Situação:</strong> ${result.descricao_situacao_cadastral || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Data de Abertura:</strong> ${result.data_inicio_atividade || 'N/A'}</p>
                            <p><strong>Porte:</strong> ${result.porte || 'N/A'}</p>
                            <p><strong>Natureza Jurídica:</strong> ${result.natureza_juridica || 'N/A'}</p>
                            <p><strong>Capital Social:</strong> R$ ${result.capital_social ? Number(result.capital_social).toLocaleString('pt-BR') : 'N/A'}</p>
                        </div>
                    `;
                    
                    // Adicionar informações de endereço
                    if (result.logradouro || result.bairro || result.municipio) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-map-marker-alt"></i> Endereço</h6>
                                <p><strong>Logradouro:</strong> ${result.descricao_tipo_de_logradouro || ''} ${result.logradouro || 'N/A'}, ${result.numero || 'S/N'}</p>
                                ${result.complemento ? `<p><strong>Complemento:</strong> ${result.complemento}</p>` : ''}
                                <p><strong>Bairro:</strong> ${result.bairro || 'N/A'}</p>
                                <p><strong>Cidade/UF:</strong> ${result.municipio || 'N/A'}/${result.uf || 'N/A'}</p>
                                <p><strong>CEP:</strong> ${result.cep || 'N/A'}</p>
                            </div>
                        `;
                    }
                    
                    // Adicionar telefones se disponível
                    if (result.ddd_telefone_1) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-phone"></i> Telefones</h6>
                                <p><strong>Telefone 1:</strong> ${result.ddd_telefone_1}</p>
                                ${result.ddd_telefone_2 ? `<p><strong>Telefone 2:</strong> ${result.ddd_telefone_2}</p>` : ''}
                            </div>
                        `;
                    }
                    
                    // Adicionar atividades se disponível
                    if (result.cnae_fiscal_descricao) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-briefcase"></i> Atividade Principal</h6>
                                <p><strong>CNAE:</strong> ${result.cnae_fiscal} - ${result.cnae_fiscal_descricao}</p>
                            </div>
                        `;
                    }
                    
                    // Adicionar atividades secundárias se disponível
                    if (result.cnaes_secundarios && result.cnaes_secundarios.length > 0) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-briefcase"></i> Atividades Secundárias</h6>
                                ${result.cnaes_secundarios.map(cnae => `<p><strong>CNAE:</strong> ${cnae.codigo} - ${cnae.descricao}</p>`).join('')}
                            </div>
                        `;
                    }
                } else if (fonte === 'cnpja') {
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj || data.cnpj || 'N/A'}</p>
                            <p><strong>Razão Social:</strong> ${result.razao_social || 'N/A'}</p>
                            <p><strong>Nome Fantasia:</strong> ${result.nome_fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.descricao_situacao_cadastral || result.situacao || 'N/A'}</p>
                            <p><strong>Data de Abertura:</strong> ${result.data_inicio_atividade || result.data_abertura || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte || 'N/A'}</p>
                            <p><strong>Natureza Jurídica:</strong> ${result.natureza_juridica || 'N/A'}</p>
                            <p><strong>Capital Social:</strong> R$ ${result.capital_social ? Number(result.capital_social).toLocaleString('pt-BR') : 'N/A'}</p>
                            <p><strong>Fonte:</strong> ${data.fonte || 'N/A'}</p>
                        </div>
                    `;
                    
                    // Adicionar informações de endereço se disponível
                    if (result.logradouro || result.bairro || result.municipio) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-map-marker-alt"></i> Endereço</h6>
                                <p><strong>Logradouro:</strong> ${result.descricao_tipo_de_logradouro || ''} ${result.logradouro || 'N/A'}, ${result.numero || 'S/N'}</p>
                                ${result.complemento ? `<p><strong>Complemento:</strong> ${result.complemento}</p>` : ''}
                                <p><strong>Bairro:</strong> ${result.bairro || 'N/A'}</p>
                                <p><strong>Cidade/UF:</strong> ${result.municipio || 'N/A'}/${result.uf || 'N/A'}</p>
                                <p><strong>CEP:</strong> ${result.cep || 'N/A'}</p>
                            </div>
                        `;
                    }
                    
                    // Adicionar telefones se disponível
                    if (result.ddd_telefone_1) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-phone"></i> Telefones</h6>
                                <p>${result.ddd_telefone_1}</p>
                                ${result.ddd_telefone_2 ? `<p>${result.ddd_telefone_2}</p>` : ''}
                            </div>
                        `;
                    }
                    
                    // Adicionar atividades se disponível
                    if (result.cnae_fiscal_descricao) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-briefcase"></i> Atividade Principal</h6>
                                <p><strong>CNAE:</strong> ${result.cnae_fiscal} - ${result.cnae_fiscal_descricao}</p>
                            </div>
                        `;
                    }
                    
                    // Adicionar atividades secundárias se disponível
                    if (result.cnaes_secundarios && result.cnaes_secundarios.length > 0) {
                        resultHtml += `
                            <div class="col-12 mt-3">
                                <h6><i class="fas fa-briefcase"></i> Atividades Secundárias</h6>
                                ${result.cnaes_secundarios.map(cnae => `<p><strong>CNAE:</strong> ${cnae.codigo} - ${cnae.descricao}</p>`).join('')}
                            </div>
                        `;
                    }
                } else {
                    // Para outras fontes (receitaws, etc.)
                    resultHtml += `
                        <div class="col-md-6">
                            <p><strong>CNPJ:</strong> ${result.cnpj || data.cnpj || 'N/A'}</p>
                            <p><strong>Nome:</strong> ${result.nome || result.razao_social || 'N/A'}</p>
                            <p><strong>Fantasia:</strong> ${result.fantasia || result.nome_fantasia || 'N/A'}</p>
                            <p><strong>Situação:</strong> ${result.descricao_situacao_cadastral || result.situacao || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Porte:</strong> ${result.porte || 'N/A'}</p>
                            <p><strong>Natureza:</strong> ${result.natureza_juridica || 'N/A'}</p>
                            <p><strong>Capital:</strong> R$ ${result.capital_social ? Number(result.capital_social).toLocaleString('pt-BR') : 'N/A'}</p>
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
                                        <th class="table-actions">Ações</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${municipios.map(m => `
                                        <tr>
                                            <td>${m.codigo_ibge || 'N/A'}</td>
                                            <td>${m.nome || 'N/A'}</td>
                                            <td class="table-actions">
                                                ${createTableMenu(m, 'municipio')}
                                            </td>
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
                                        <th class="table-actions">Ações</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${bancos.map(b => `
                                        <tr>
                                            <td><span class="badge bg-primary">${b.code || 'N/A'}</span></td>
                                            <td>${b.name || 'N/A'}</td>
                                            <td>${b.fullName || 'N/A'}</td>
                                            <td class="table-actions">
                                                ${createTableMenu(b, 'banco')}
                                            </td>
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

// Carregar histórico de cache
async function carregarHistoricoCache() {
    try {
        showLoading('cacheHistory');
        
        const response = await fetch('/api/cache/history');
        const data = await response.json();

        if (data.status === 'success') {
            let html = '';
            
            if (data.total === 0) {
                html = '<p class="text-muted">Nenhuma limpeza de cache registrada.</p>';
            } else {
                html = `
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Data/Hora</th>
                                    <th>Ação</th>
                                    <th>Itens Removidos</th>
                                    <th>IP do Usuário</th>
                                    <th>Detalhes</th>
                                    <th class="table-actions">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                data.historico.forEach(item => {
                    const dataFormatada = new Date(item.data_execucao).toLocaleString('pt-BR');
                    html += `
                        <tr>
                            <td>${dataFormatada}</td>
                            <td><span class="badge bg-warning">Limpeza</span></td>
                            <td>${item.items_removidos}</td>
                            <td>${item.usuario_ip}</td>
                            <td>${item.detalhes}</td>
                            <td class="table-actions">
                                ${createTableMenu(item, 'cache')}
                            </td>
                        </tr>
                    `;
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                    <p class="text-muted mt-2">Total de registros: ${data.total}</p>
                `;
            }
            
            document.getElementById('cacheHistory').innerHTML = html;
        } else {
            document.getElementById('cacheHistory').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> Erro ao carregar histórico: ${data.message}
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('cacheHistory').innerHTML = `
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
        const rg = document.getElementById('dadosPessoaisRgInput') ? document.getElementById('dadosPessoaisRgInput').value.replace(/\D/g, '') : '';
        const cnh = document.getElementById('dadosPessoaisCnhInput') ? document.getElementById('dadosPessoaisCnhInput').value.replace(/\D/g, '') : '';
        const email = document.getElementById('dadosPessoaisEmailInput') ? document.getElementById('dadosPessoaisEmailInput').value.trim() : '';
        const tituloEleitor = document.getElementById('dadosPessoaisTituloEleitorInput') ? document.getElementById('dadosPessoaisTituloEleitorInput').value.replace(/\D/g, '') : '';
        const pis = document.getElementById('dadosPessoaisPisInput') ? document.getElementById('dadosPessoaisPisInput').value.replace(/\D/g, '') : '';
        const cns = document.getElementById('dadosPessoaisCnsInput') ? document.getElementById('dadosPessoaisCnsInput').value.replace(/\D/g, '') : '';
        const dataNascimento = document.getElementById('dadosPessoaisDataNascInput') ? document.getElementById('dadosPessoaisDataNascInput').value.replace(/\D/g, '') : '';
        
        // Verificar se pelo menos um campo foi preenchido
        if (!telefone && !cpf && !nome && !rg && !cnh && !email && !tituloEleitor && !pis && !cns && !dataNascimento) {
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
        
        if (tituloEleitor && tituloEleitor.length !== 12) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>Título de eleitor deve ter 12 dígitos</p>
                </div>
            `);
            return;
        }
        
        if (pis && pis.length !== 11) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>PIS deve ter 11 dígitos</p>
                </div>
            `);
            return;
        }
        
        if (cns && cns.length !== 15) {
            showResult('dadosPessoaisResult', `
                <div class="result-card error-card">
                    <h5><i class="fas fa-exclamation-triangle text-danger"></i> Erro</h5>
                    <p>CNS deve ter 15 dígitos</p>
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
            // Usar a nova API de busca cruzada
            const requestData = {};
            if (telefone) requestData.telefone = telefone;
            if (cpf) requestData.cpf = cpf;
            if (nome) requestData.nome = nome;
            if (rg) requestData.rg = rg;
            if (cnh) requestData.cnh = cnh;
            if (email) requestData.email = email;
            if (tituloEleitor) requestData.titulo_eleitor = tituloEleitor;
            if (pis) requestData.pis = pis;
            if (cns) requestData.cns = cns;
            if (dataNascimento) {
                // Converter para formato YYYY-MM-DD
                const day = dataNascimento.substring(0, 2);
                const month = dataNascimento.substring(2, 4);
                const year = dataNascimento.substring(4, 8);
                requestData.data_nascimento = `${year}-${month}-${day}`;
            }
            
            const response = await fetch('/api/buscar/cruzada', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            setTimeout(() => {
                hideLoading('dadosPessoaisLoading');
                
                if (data.dados && data.dados.length > 0) {
                    // Exibir resultados da busca cruzada
                    const resultados = data.dados.map(pessoa => `
                        <div class="result-card success-card mb-3">
                            <h5><i class="fas fa-user-check text-success"></i> Registro Encontrado</h5>
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong><i class="fas fa-user"></i> Nome:</strong> ${pessoa.nome || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-id-card"></i> CPF:</strong> ${pessoa.cpf || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-address-card"></i> RG:</strong> ${pessoa.rg || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-car"></i> CNH:</strong> ${pessoa.cnh || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-envelope"></i> Email:</strong> ${pessoa.email || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-phone"></i> Telefone:</strong> ${pessoa.telefone || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-vote-yea"></i> Título de Eleitor:</strong> ${pessoa.titulo_eleitor || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-briefcase"></i> PIS:</strong> ${pessoa.pis || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-hospital"></i> CNS:</strong> ${pessoa.cns || 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-calendar-plus"></i> Data de Criação:</strong> ${pessoa.data_criacao ? new Date(pessoa.data_criacao).toLocaleDateString('pt-BR') : 'N/A'}
                                </div>
                                <div class="info-item">
                                    <strong><i class="fas fa-calendar-check"></i> Última Atualização:</strong> ${pessoa.data_atualizacao ? new Date(pessoa.data_atualizacao).toLocaleDateString('pt-BR') : 'N/A'}
                                </div>
                            </div>
                            <div class="mt-3">
                                <button class="btn btn-outline-primary btn-sm me-2" onclick="exportarJSON(${JSON.stringify(pessoa).replace(/"/g, '&quot;')})">
                                    <i class="fas fa-download"></i> Exportar JSON
                                </button>
                                <button class="btn btn-outline-success btn-sm" onclick="exportarCSV([${JSON.stringify(pessoa).replace(/"/g, '&quot;')}])">
                                    <i class="fas fa-file-csv"></i> Exportar CSV
                                </button>
                            </div>
                        </div>
                    `).join('');
                    
                    showResult('dadosPessoaisResult', `
                        <div class="alert alert-success">
                            <i class="fas fa-check-circle"></i>
                            <strong>Busca Avançada Concluída!</strong> Encontrados ${data.dados.length} registro(s) no banco de dados.
                        </div>
                        ${resultados}
                        <div class="mt-3 text-center">
                            <button class="btn btn-primary me-2" onclick="exportarJSON(${JSON.stringify(data.dados).replace(/"/g, '&quot;')})">
                                <i class="fas fa-download"></i> Exportar Todos (JSON)
                            </button>
                            <button class="btn btn-success" onclick="exportarCSV(${JSON.stringify(data.dados).replace(/"/g, '&quot;')})">
                                <i class="fas fa-file-csv"></i> Exportar Todos (CSV)
                            </button>
                        </div>
                    `);
                } else if ((data.success && data.data) || (!data.erro && data.dados_encontrados)) {
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
                        <div class="result-card warning-card">
                            <h5><i class="fas fa-search text-warning"></i> Nenhum resultado encontrado</h5>
                            <p class="mb-3">${data.erro || data.error || 'Não foram encontrados dados pessoais com os critérios informados na busca avançada.'}</p>
                            <div class="alert alert-info">
                                <h6><i class="fas fa-lightbulb"></i> Sugestões para melhorar sua busca:</h6>
                                <ul class="mb-0">
                                    <li>Verifique se os dados informados estão corretos</li>
                                    <li>Tente usar menos campos para ampliar a busca</li>
                                    <li>Experimente variações do nome (com/sem acentos, abreviações)</li>
                                    <li>Confirme se o CPF ou telefone estão no formato correto</li>
                                    <li>Tente a busca individual por CPF ou Nome nas outras abas</li>
                                </ul>
                            </div>
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