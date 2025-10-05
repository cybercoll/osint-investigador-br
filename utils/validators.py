"""
Módulo de validação para dados de entrada
"""
import re


def validar_cep(cep: str) -> bool:
    """
    Valida formato de CEP brasileiro
    
    Args:
        cep (str): CEP a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cep:
        return False
    
    # Remove caracteres não numéricos
    cep_limpo = re.sub(r'\D', '', cep)
    
    # Verifica se tem 8 dígitos
    return len(cep_limpo) == 8 and cep_limpo.isdigit()


def validar_ddd(ddd: str) -> bool:
    """
    Valida código DDD brasileiro
    
    Args:
        ddd (str): DDD a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not ddd:
        return False
    
    # Remove caracteres não numéricos
    ddd_limpo = re.sub(r'\D', '', ddd)
    
    # Lista de DDDs válidos no Brasil
    ddds_validos = [
        '11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
        '21', '22', '24',  # RJ
        '27', '28',  # ES
        '31', '32', '33', '34', '35', '37', '38',  # MG
        '41', '42', '43', '44', '45', '46',  # PR
        '47', '48', '49',  # SC
        '51', '53', '54', '55',  # RS
        '61',  # DF/GO
        '62', '64',  # GO
        '63',  # TO
        '65', '66',  # MT
        '67',  # MS
        '68',  # AC
        '69',  # RO/AC
        '71', '73', '74', '75', '77',  # BA
        '79',  # SE
        '81', '87',  # PE
        '82',  # AL
        '83',  # PB
        '84',  # RN
        '85', '88',  # CE
        '86', '89',  # PI
        '91', '93', '94',  # PA
        '92', '97',  # AM
        '95',  # RR
        '96',  # AP
        '98', '99'   # MA
    ]
    
    return ddd_limpo in ddds_validos


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ brasileiro
    
    Args:
        cnpj (str): CNPJ a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cnpj:
        return False
    
    # Remove caracteres não numéricos
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj_limpo) != 14:
        return False
    
    # Verifica se não são todos os dígitos iguais
    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False
    
    # Validação dos dígitos verificadores
    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito1 = calcular_digito(cnpj_limpo[:12], pesos1)
    
    # Segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito2 = calcular_digito(cnpj_limpo[:13], pesos2)
    
    return int(cnpj_limpo[12]) == digito1 and int(cnpj_limpo[13]) == digito2


def limpar_cep(cep: str) -> str:
    """
    Remove formatação do CEP
    
    Args:
        cep (str): CEP com ou sem formatação
        
    Returns:
        str: CEP apenas com números
    """
    return re.sub(r'\D', '', cep) if cep else ""


def limpar_ddd(ddd: str) -> str:
    """
    Remove formatação do DDD
    
    Args:
        ddd (str): DDD com ou sem formatação
        
    Returns:
        str: DDD apenas com números
    """
    return re.sub(r'\D', '', ddd) if ddd else ""


def limpar_cnpj(cnpj: str) -> str:
    """
    Remove formatação do CNPJ
    
    Args:
        cnpj (str): CNPJ com ou sem formatação
        
    Returns:
        str: CNPJ apenas com números
    """
    return re.sub(r'\D', '', cnpj) if cnpj else ""


def formatar_cep(cep: str) -> str:
    """
    Formata CEP no padrão XXXXX-XXX
    
    Args:
        cep (str): CEP sem formatação
        
    Returns:
        str: CEP formatado
    """
    cep_limpo = limpar_cep(cep)
    if len(cep_limpo) == 8:
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
    return cep


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX
    
    Args:
        cnpj (str): CNPJ sem formatação
        
    Returns:
        str: CNPJ formatado
    """
    cnpj_limpo = limpar_cnpj(cnpj)
    if len(cnpj_limpo) == 14:
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    return cnpj