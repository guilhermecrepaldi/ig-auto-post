"""
Geração de legenda para post do Instagram usando DeepSeek API.
"""
import requests
import json

def gerar_legenda(config):
    """Gera legenda criativa para post de tecnologia usando DeepSeek."""
    api_key = config["deepseek"]["api_key"]
    modelo = config["deepseek"]["model"]
    hashtags = " ".join(f"#{h}" for h in config["post"]["hashtags_padrao"])
    
    if not api_key or api_key == "SEU_DEEPSEEK_KEY":
        return fallback_legenda(hashtags)
    
    prompt = f"""Crie uma legenda curta e impactante para Instagram sobre tecnologia e programação.
Máximo 200 caracteres. Inclua estas hashtags: {hashtags}
Tom: motivacional, direto, para desenvolvedores.
Exemplo: "Código que funciona 24/7, pipelines que entregam, agentes que aprendem. 🚀 #dev #python"
---
Legenda:"""
    
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": modelo,
                "messages": [
                    {"role": "system", "content": "Você é um social media de tecnologia. Gera legendas curtas e impactantes para Instagram."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.8
            },
            timeout=30
        )
        legenda = resp.json()["choices"][0]["message"]["content"].strip()
        return legenda[:300]  # Instagram permite até 2200 chars
    except Exception as e:
        print(f"   ⚠️ Erro API legenda: {e}. Usando fallback.")
        return fallback_legenda(hashtags)

def fallback_legenda(hashtags):
    import random
    frases = [
        f"Código que funciona 24/7, pipelines que entregam, agentes que aprendem. 🚀 {hashtags}",
        f"Automação inteligente não é sobre substituir pessoas, é sobre liberar potencial. ⚡ {hashtags}",
        f"Construindo o futuro um commit de cada vez. 🛠️ {hashtags}",
        f"IA local + automação = poder nas suas mãos. 🤖 {hashtags}",
    ]
    return random.choice(frases)
