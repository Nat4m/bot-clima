"""
Verifica se vai chover ou fazer frio no dia, usando a API gratuita da Open-Meteo.
Não precisa de chave de API.

Como funciona:
1. Pega a latitude/longitude da cidade (usando a API de geocoding da Open-Meteo).
2. Pega a previsão do dia (temperatura máxima/mínima e probabilidade de chuva).
3. Verifica se vai chover (precipitação prevista) e se vai fazer frio (temp < 21°C).
"""

import requests

TEMPERATURA_FRIO = 21  # °C - limite definido pelo usuário


def buscar_coordenadas(cidade: str):
    """Busca latitude e longitude de uma cidade usando a API de geocoding da Open-Meteo."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": cidade, "count": 1, "language": "pt", "format": "json"}

    resposta = requests.get(url, params=params, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()

    if not dados.get("results"):
        raise ValueError(f"Cidade '{cidade}' não encontrada.")

    resultado = dados["results"][0]
    return resultado["latitude"], resultado["longitude"], resultado["name"]


def buscar_previsao(latitude: float, longitude: float):
    """Busca a previsão do dia (temp max/min e probabilidade de chuva) na Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 1,
    }

    resposta = requests.get(url, params=params, timeout=10)
    resposta.raise_for_status()
    return resposta.json()["daily"]


def verificar_clima(cidade: str):
    """Verifica se vai chover e/ou fazer frio hoje na cidade informada."""
    lat, lon, nome_cidade = buscar_coordenadas(cidade)
    previsao = buscar_previsao(lat, lon)

    temp_max = previsao["temperature_2m_max"][0]
    temp_min = previsao["temperature_2m_min"][0]
    prob_chuva = previsao["precipitation_probability_max"][0]
    soma_chuva = previsao["precipitation_sum"][0]

    vai_chover = prob_chuva >= 50 or soma_chuva > 0
    vai_fazer_frio = temp_min < TEMPERATURA_FRIO

    #print(f"\nPrevisão para {nome_cidade} hoje:")
    #print(f"  Temperatura mínima: {temp_min}°C")
    #print(f"  Temperatura máxima: {temp_max}°C")
    #print(f"  Probabilidade de chuva: {prob_chuva}%")
    #print(f"  Volume de chuva previsto: {soma_chuva} mm")
    #print()
    #print(f"  Vai chover? {'Sim' if vai_chover else 'Não'}")
    #print(f"  Vai fazer frio (< {TEMPERATURA_FRIO}°C)? {'Sim' if vai_fazer_frio else 'Não'}")

    return {
        "cidade": nome_cidade,
        "temp_max": temp_max,
        "temp_min": temp_min,
        "prob_chuva": prob_chuva,
        "vai_chover": vai_chover,
        "vai_fazer_frio": vai_fazer_frio,
    }


if __name__ == "__main__":
    cidade = input("Digite o nome da cidade: ")
    verificar_clima(cidade)