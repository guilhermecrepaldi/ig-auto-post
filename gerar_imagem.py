"""
Geração de imagem para post do Instagram.
Usa Pillow para criar templates com texto + Ollama para geração via IA.
"""
import os
from pathlib import Path
from datetime import datetime

PASTA = Path(__file__).parent
TEMPLATES_DIR = PASTA / "templates"
POSTS_DIR = PASTA / "posts"

def gerar_imagem_post(legenda, config):
    """Gera imagem para o post. Tenta Ollama/local, fallback para template Pillow."""
    POSTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = POSTS_DIR / f"post_{timestamp}.jpg"
    
    # Tenta Ollama (imagem via prompt)
    imagem_ollama = gerar_com_ollama(config, timestamp)
    if imagem_ollama and os.path.exists(imagem_ollama):
        return imagem_ollama
    
    # Fallback: template Pillow
    return gerar_template_pillow(legenda, caminho, config)

def gerar_com_ollama(config, timestamp):
    """Tenta gerar imagem via Ollama + llava."""
    try:
        import requests
        prompt = config.get("templates", [{}])[0].get("descricao", " tecnologia código")
        
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava:7b",
                "prompt": f"Crie uma descrição detalhada de uma imagem profissional para post de Instagram sobre: {prompt}. Deve ser moderna, clean, com tons escuros e azuis.",
                "stream": False
            },
            timeout=60
        )
        descricao = resp.json().get("response", "")
        
        # llava não gera imagens, só descreve. Usamos como prompt para template
        print(f"   ℹ️ Ollama descreveu: {descricao[:80]}...")
        return None  # fallback para Pillow
        
    except Exception as e:
        print(f"   ℹ️ Ollama não disponível: {e}")
        return None

def gerar_template_pillow(legenda, caminho, config):
    """Cria imagem estilizada com Pillow."""
    from PIL import Image, ImageDraw, ImageFont
    
    # Dimensões Instagram (1080x1080 quadrado)
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), "#0a0a1a")
    draw = ImageDraw.Draw(img)
    
    # Gradiente simples (topo → base)
    for y in range(H):
        r = int(10 + (y / H) * 20)
        g = int(10 + (y / H) * 15)
        b = int(26 + (y / H) * 30)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Linha decorativa
    draw.rectangle([(80, 100), (1000, 104)], fill="#00d4ff")
    
    # Título
    try:
        font_titulo = ImageFont.truetype("arialbd.ttf", 48)
        font_legenda = ImageFont.truetype("arial.ttf", 36)
    except:
        font_titulo = ImageFont.load_default()
        font_legenda = ImageFont.load_default()
    
    titulo = "⚡ IG AUTO POST"
    draw.text((W // 2, 200), titulo, fill="#00d4ff", anchor="mt", font=font_titulo)
    
    # Legenda formatada
    import textwrap
    linhas = textwrap.wrap(legenda, width=35)
    y_texto = 320
    for linha in linhas[:6]:  # máximo 6 linhas
        draw.text((W // 2, y_texto), linha, fill="white", anchor="mt", font=font_legenda)
        y_texto += 50
    
    # Hashtags no rodapé
    draw.text((W // 2, H - 120), "#dev #python #automation", fill="#00d4ff", anchor="mt", font=font_legenda)
    
    # Timestamp
    draw.text((W // 2, H - 60), datetime.now().strftime("%d/%m/%Y"), fill="gray", anchor="mt", font=font_legenda)
    
    img.save(caminho, "JPEG", quality=95)
    print(f"   ✅ Imagem gerada: {caminho}")
    return str(caminho)
