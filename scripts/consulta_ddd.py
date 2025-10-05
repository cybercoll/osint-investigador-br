import requests

def consultar_ddd(ddd):
    url = f"https://brasilapi.com.br/api/ddd/v1/{ddd}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        data = response.json()
        if 'message' in data and 'DDD não encontrado' in data['message']:
            return f"DDD {ddd} não encontrado."
        else:
            return data
    except requests.exceptions.RequestException as e:
        return f"Erro ao consultar o DDD {ddd}: {e}"

if __name__ == "__main__":
    ddd_input = input("Digite o DDD para consulta: ")
    resultado = consultar_ddd(ddd_input)
    if isinstance(resultado, dict):
        print("--- Dados do DDD ---")
        print(f"Estado: {resultado.get("state", "N/A")}")
        print("Cidades:")
        for cidade in resultado.get("cities", []):
            print(f"- {cidade}")
    else:
        print(resultado)

