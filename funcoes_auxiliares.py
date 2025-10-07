"""
Funções auxiliares para simulação de consultas avançadas
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def realizar_cruzamento_dados(resultado: Dict[str, Any]) -> Dict[str, Any]:
    """Realiza cruzamento de dados entre as diferentes fontes consultadas"""
    try:
        dados_encontrados = resultado.get("dados_encontrados", {})
        cruzamento = {}
        
        # Cruza dados de nome
        nomes_encontrados = []
        for fonte, dados in dados_encontrados.items():
            if isinstance(dados, dict) and "nome" in dados:
                nomes_encontrados.append(dados["nome"])
        
        if nomes_encontrados:
            # Verifica consistência dos nomes
            nome_mais_comum = max(set(nomes_encontrados), key=nomes_encontrados.count)
            cruzamento["nome_validado"] = nome_mais_comum
            cruzamento["consistencia_nome"] = nomes_encontrados.count(nome_mais_comum) / len(nomes_encontrados)
        
        # Cruza dados de telefone
        telefones_encontrados = []
        for fonte, dados in dados_encontrados.items():
            if isinstance(dados, dict) and "telefone" in dados:
                telefones_encontrados.append(dados["telefone"])
        
        if telefones_encontrados:
            telefone_mais_comum = max(set(telefones_encontrados), key=telefones_encontrados.count)
            cruzamento["telefone_validado"] = telefone_mais_comum
            cruzamento["consistencia_telefone"] = telefones_encontrados.count(telefone_mais_comum) / len(telefones_encontrados)
        
        # Cruza dados de localização
        localizacoes = []
        for fonte, dados in dados_encontrados.items():
            if isinstance(dados, dict) and "cidade" in dados:
                localizacoes.append(f"{dados.get('cidade', '')}, {dados.get('estado', '')}")
        
        if localizacoes:
            localizacao_mais_comum = max(set(localizacoes), key=localizacoes.count)
            cruzamento["localizacao_validada"] = localizacao_mais_comum
            cruzamento["consistencia_localizacao"] = localizacoes.count(localizacao_mais_comum) / len(localizacoes)
        
        resultado["cruzamento_dados"] = cruzamento
        
    except Exception as e:
        logger.error(f"Erro no cruzamento de dados: {e}")
    
    return resultado

def calcular_confiabilidade(resultado: Dict[str, Any]) -> str:
    """Calcula o nível de confiabilidade baseado na quantidade e consistência dos dados"""
    try:
        dados_encontrados = len(resultado.get("dados_encontrados", {}))
        apis_utilizadas = len(resultado.get("apis_utilizadas", []))
        cruzamento = resultado.get("cruzamento_dados", {})
        
        score = 0
        
        # Pontuação por quantidade de fontes
        if dados_encontrados >= 5:
            score += 3
        elif dados_encontrados >= 3:
            score += 2
        elif dados_encontrados >= 1:
            score += 1
        
        # Pontuação por consistência de dados
        consistencias = [v for k, v in cruzamento.items() if k.startswith("consistencia_")]
        if consistencias:
            media_consistencia = sum(consistencias) / len(consistencias)
            if media_consistencia >= 0.8:
                score += 3
            elif media_consistencia >= 0.6:
                score += 2
            elif media_consistencia >= 0.4:
                score += 1
        
        # Pontuação por diversidade de APIs
        if apis_utilizadas >= 6:
            score += 2
        elif apis_utilizadas >= 3:
            score += 1
        
        # Determina nível de confiabilidade
        if score >= 7:
            return "muito_alta"
        elif score >= 5:
            return "alta"
        elif score >= 3:
            return "media"
        elif score >= 1:
            return "baixa"
        else:
            return "muito_baixa"
            
    except Exception as e:
        logger.error(f"Erro no cálculo de confiabilidade: {e}")
        return "indeterminada"

# Funções de simulação para demonstração
def simular_truecaller(telefone: str) -> Dict[str, Any]:
    """Simula consulta no TrueCaller"""
    return {
        "nome": "João Silva Santos",
        "telefone": telefone,
        "spam_score": 0.1,
        "verificado": True,
        "fonte": "TrueCaller"
    }

def simular_consulta_redes_sociais_telefone(telefone: str) -> Dict[str, Any]:
    """Simula consulta em redes sociais por telefone"""
    return {
        "facebook": {"encontrado": True, "nome": "João Silva", "foto_perfil": "url_foto"},
        "instagram": {"encontrado": True, "usuario": "@joaosilva123"},
        "whatsapp": {"encontrado": True, "nome": "João S.", "foto": "url_foto"}
    }

def simular_consulta_receita_federal(cpf: str) -> Dict[str, Any]:
    """Simula consulta na Receita Federal"""
    return {
        "nome": "João Silva Santos",
        "cpf": cpf,
        "situacao": "Regular",
        "data_nascimento": "1985-03-15",
        "titulo_eleitor": "123456789012"
    }

def simular_consulta_spc_serasa(cpf: str) -> Dict[str, Any]:
    """Simula consulta no SPC/Serasa"""
    return {
        "nome": "João Silva Santos",
        "cpf": cpf,
        "score": 650,
        "restricoes": False,
        "renda_estimada": "R$ 3.500,00",
        "classe_social": "C"
    }

def simular_consulta_tse(cpf: str) -> Dict[str, Any]:
    """Simula consulta no Tribunal Superior Eleitoral"""
    return {
        "nome": "João Silva Santos",
        "titulo": "123456789012",
        "zona": "001",
        "secao": "0001",
        "municipio": "São Paulo",
        "estado": "SP"
    }

def simular_consulta_facebook(nome: str) -> Dict[str, Any]:
    """Simula consulta no Facebook"""
    return {
        "nome": nome,
        "perfil_url": "facebook.com/joaosilva",
        "cidade": "São Paulo, SP",
        "trabalho": "Analista de Sistemas",
        "educacao": "Universidade de São Paulo"
    }

def simular_consulta_linkedin(nome: str) -> Dict[str, Any]:
    """Simula consulta no LinkedIn"""
    return {
        "nome": nome,
        "perfil_url": "linkedin.com/in/joaosilva",
        "cargo": "Analista de Sistemas Sênior",
        "empresa": "Tech Solutions Ltda",
        "localizacao": "São Paulo, Brasil"
    }

def simular_consulta_motores_busca(nome: str) -> Dict[str, Any]:
    """Simula consulta em motores de busca"""
    return {
        "resultados_google": 15,
        "mencoes_noticias": 2,
        "perfis_profissionais": 3,
        "redes_sociais": 5
    }

def simular_bases_comerciais(dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
    """Simula consulta em bases comerciais"""
    return {
        "nome": "João Silva Santos",
        "telefone": dados_entrada.get("telefone", ""),
        "email": "joao.silva@email.com",
        "endereco": "Rua das Flores, 123 - São Paulo/SP",
        "cep": "01234-567",
        "profissao": "Analista de Sistemas"
    }

def simular_registros_publicos(dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
    """Simula consulta em registros públicos"""
    return {
        "cartorio": "1º Cartório de Registro Civil",
        "certidao_nascimento": "123456",
        "filiacao": {
            "pai": "José Santos",
            "mae": "Maria Silva Santos"
        },
        "estado_civil": "Solteiro"
    }

def simular_bases_internacionais(dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
    """Simula consulta em bases internacionais"""
    return {
        "interpol": {"encontrado": False},
        "fbi_most_wanted": {"encontrado": False},
        "sanctions_lists": {"encontrado": False},
        "international_databases": {"mencoes": 0}
    }

def identificar_operadora(telefone: str) -> str:
    """Identifica a operadora do telefone"""
    if len(telefone) >= 3:
        terceiro_digito = telefone[2]
        if terceiro_digito in ['6', '7', '8', '9']:
            return "Vivo"
        elif terceiro_digito in ['1', '2']:
            return "TIM"
        elif terceiro_digito in ['3', '4']:
            return "Claro"
        elif terceiro_digito == '5':
            return "Oi"
    return "Desconhecida"

def obter_regiao_ddd(ddd: str) -> str:
    """Obtém a região do DDD"""
    regioes_ddd = {
        "11": "São Paulo - SP", "12": "São José dos Campos - SP", "13": "Santos - SP",
        "14": "Bauru - SP", "15": "Sorocaba - SP", "16": "Ribeirão Preto - SP",
        "17": "São José do Rio Preto - SP", "18": "Presidente Prudente - SP",
        "19": "Campinas - SP", "21": "Rio de Janeiro - RJ", "22": "Campos dos Goytacazes - RJ",
        "24": "Volta Redonda - RJ", "27": "Vitória - ES", "28": "Cachoeiro de Itapemirim - ES"
    }
    return regioes_ddd.get(ddd, f"Região do DDD {ddd}")