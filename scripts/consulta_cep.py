import requests

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        data = response.json()
        if 'erro' in data:
            return f"CEP {cep} não encontrado."
        else:
            return data
    except requests.exceptions.RequestException as e:
        return f"Erro ao consultar o CEP {cep}: {e}"

if __name__ == "__main__":
    cep_input = input("Digite o CEP para consulta: ")
    resultado = consultar_cep(cep_input)
    if isinstance(resultado, dict):
        print("--- Dados do CEP ---")
        for key, value in resultado.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(resultado)

