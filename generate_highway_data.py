import json
import math
from datetime import datetime, timedelta
import random

# Seed para reprodutibilidade
random.seed(42)

# Parâmetros da rodovia
COMPRIMENTO_TOTAL_KM = 100
TAMANHO_MICROTRECHO_M = 500
NUM_MICROTRECHOS = (COMPRIMENTO_TOTAL_KM * 1000) // TAMANHO_MICROTRECHO_M

# Coordenadas iniciais (referência BR-101, Bahia)
LAT_INICIAL = -12.965
LON_INICIAL = -38.510

# Incrementos por microtrecho (~500m)
LAT_INCREMENTO = 500 / 111000  # ~0.0045 por 500m
LON_INCREMENTO = 500 / (111000 * math.cos(math.radians(LAT_INICIAL)))

def definir_zona(km):
    """Define características da zona baseado no km"""
    if km < 15:
        return "urbana"
    elif km < 35:
        return "rural_estavel"
    elif km < 65:
        return "critica"
    elif km < 80:
        return "recuperada"
    else:
        return "monitoramento"

def calcular_evi(km, zona):
    """Calcula EVI realista por zona"""
    base = {
        "urbana": 0.25,
        "rural_estavel": 0.45,
        "critica": 0.65,
        "recuperada": 0.35,
        "monitoramento": 0.50
    }

    valor_base = base.get(zona, 0.45)
    # Adiciona variação sutil
    variacao = random.gauss(0, 0.08)
    return max(0.1, min(0.8, valor_base + variacao))

def calcular_dias_sem_manutencao(km, zona, evi):
    """Calcula dias sem manutenção realista"""
    base = {
        "urbana": random.randint(5, 30),
        "rural_estavel": random.randint(15, 45),
        "critica": random.randint(60, 150),
        "recuperada": random.randint(10, 40),
        "monitoramento": random.randint(20, 60)
    }

    dias = base.get(zona, 30)
    # EVI alto = mais dias sem manutenção
    dias = int(dias * (0.8 + evi * 0.4))
    return min(180, dias)

def calcular_risco_operacional(km, zona, evi, dias_sem_manutencao):
    """Calcula índice de risco operacional"""
    risco_base = {
        "urbana": 15,
        "rural_estavel": 25,
        "critica": 70,
        "recuperada": 35,
        "monitoramento": 40
    }

    risco = risco_base.get(zona, 30)

    # Adiciona fatores
    risco += evi * 15  # EVI alto aumenta risco
    risco += (dias_sem_manutencao / 180) * 20  # Mais dias = mais risco

    # Variação diária
    risco += random.gauss(0, 5)

    return max(0, min(100, risco))

def calcular_previsao_chuva(km, mes_simulado=None):
    """Simula previsão de chuva com sazonalidade"""
    if mes_simulado is None:
        mes_simulado = datetime.now().month

    # Padrão de chuvas (maiores em abril-julho no nordeste)
    base_chuva = {
        1: 0.20, 2: 0.18, 3: 0.25, 4: 0.60,
        5: 0.75, 6: 0.80, 7: 0.70, 8: 0.40,
        9: 0.25, 10: 0.30, 11: 0.20, 12: 0.15
    }

    chuva_mes = base_chuva.get(mes_simulado, 0.3)
    # Pequena variação por localização
    variacao = random.gauss(0, 0.1)
    return max(0, min(1.0, chuva_mes + variacao))

def definir_prioridade(risco_operacional, dias_sem_manutencao, evi):
    """Define prioridade operacional"""
    if risco_operacional > 75 or dias_sem_manutencao > 120 or evi > 0.70:
        return "critica"
    elif risco_operacional > 50 or dias_sem_manutencao > 80:
        return "alta"
    elif risco_operacional > 30 or dias_sem_manutencao > 45:
        return "media"
    else:
        return "baixa"

def definir_status_operacional(risco_operacional, prioridade):
    """Define status operacional"""
    if risco_operacional > 85:
        return "interditado"
    elif risco_operacional > 70:
        return "parcialmente_interditado"
    elif prioridade == "critica":
        return "em_manutencao"
    else:
        return "liberado"

def calcular_historico_rocadas(km, zona, evi, dias_sem_manutencao):
    """Simula histórico de roçadas nos últimos 12 meses"""
    # Zonas críticas com EVI alto são roçadas mais frequentemente
    base = {
        "urbana": random.randint(8, 12),
        "rural_estavel": random.randint(6, 10),
        "critica": random.randint(10, 16),
        "recuperada": random.randint(7, 11),
        "monitoramento": random.randint(8, 12)
    }

    rocadas = base.get(zona, 8)
    # Correlação com EVI
    rocadas = int(rocadas * (0.7 + evi * 0.6))
    # Correlação com dias sem manutenção
    rocadas = max(rocadas - (dias_sem_manutencao // 20), 0)

    return rocadas

def _gerar_observacoes(zona, risco, evi):
    """Gera observações realistas"""
    observacoes = []

    if zona == "critica":
        observacoes.append("Zona de vegetação densa - priorizar roçada")
    if evi > 0.65:
        observacoes.append("EVI elevado - monitorar inundações sazonais")
    if risco > 75:
        observacoes.append("Risco operacional crítico")
    if zona == "urbana":
        observacoes.append("Próximo a zona urbana - trânsito intenso")

    return observacoes if observacoes else ["Situação normal"]

# Gerar dados
microtrechos = []

for i in range(NUM_MICROTRECHOS):
    km_inicial = i * 0.5
    km_final = km_inicial + 0.5
    km_medio = (km_inicial + km_final) / 2

    # Calcular coordenadas (aproximação simples)
    latitude = LAT_INICIAL - (i * LAT_INCREMENTO)
    longitude = LON_INICIAL + (i * LON_INCREMENTO)

    # Definir zona e características
    zona = definir_zona(km_medio)
    evi = calcular_evi(km_medio, zona)
    dias_sem_manutencao = calcular_dias_sem_manutencao(km_medio, zona, evi)
    risco_operacional = calcular_risco_operacional(km_medio, zona, evi, dias_sem_manutencao)
    previsao_chuva = calcular_previsao_chuva(km_medio)
    prioridade = definir_prioridade(risco_operacional, dias_sem_manutencao, evi)
    status = definir_status_operacional(risco_operacional, prioridade)
    historico_rocadas = calcular_historico_rocadas(km_medio, zona, evi, dias_sem_manutencao)

    microtrecho = {
        "id": f"MT-{i+1:03d}",
        "km_inicial": round(km_inicial, 2),
        "km_final": round(km_final, 2),
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "zona": zona,
        "valor_evi": round(evi, 3),
        "dias_sem_manutencao": dias_sem_manutencao,
        "indice_risco_operacional": round(risco_operacional, 2),
        "previsao_chuva": round(previsao_chuva * 100, 1),
        "prioridade_operacional": prioridade,
        "status_operacional": status,
        "historico_rocadas": historico_rocadas,
        "metadata": {
            "data_coleta": datetime.now().isoformat(),
            "observacoes": _gerar_observacoes(zona, risco_operacional, evi)
        }
    }

    microtrechos.append(microtrecho)

# Recalcular com função de observações definida
for i, mt in enumerate(microtrechos):
    mt["metadata"]["observacoes"] = _gerar_observacoes(
        mt["zona"],
        mt["indice_risco_operacional"],
        mt["valor_evi"]
    )

# Estrutura final
dados_rodovia = {
    "rodovia": {
        "nome": "BR-101 Trecho Monitorado",
        "comprimento_km": COMPRIMENTO_TOTAL_KM,
        "tamanho_microtrecho_m": TAMANHO_MICROTRECHO_M,
        "total_microtrechos": NUM_MICROTRECHOS
    },
    "data_geracao": datetime.now().isoformat(),
    "microtrechos": microtrechos,
    "resumo": {
        "trechos_criticos": len([m for m in microtrechos if m["prioridade_operacional"] == "critica"]),
        "trechos_em_manutencao": len([m for m in microtrechos if m["status_operacional"] == "em_manutencao"]),
        "evi_medio": round(sum(m["valor_evi"] for m in microtrechos) / len(microtrechos), 3),
        "risco_medio": round(sum(m["indice_risco_operacional"] for m in microtrechos) / len(microtrechos), 2)
    }
}

# Salvar JSON
with open('c:/Users/jv921/OneDrive/Área de Trabalho/protipo challnege/highway_data.json', 'w', encoding='utf-8') as f:
    json.dump(dados_rodovia, f, ensure_ascii=False, indent=2)

print("[OK] Arquivo gerado com sucesso!")
print(f"[INFO] Total de microtrechos: {NUM_MICROTRECHOS}")
print(f"[INFO] Trechos críticos: {dados_rodovia['resumo']['trechos_criticos']}")
print(f"[INFO] Trechos em manutenção: {dados_rodovia['resumo']['trechos_em_manutencao']}")
print(f"[INFO] EVI médio: {dados_rodovia['resumo']['evi_medio']}")
print(f"[INFO] Risco operacional médio: {dados_rodovia['resumo']['risco_medio']}")
