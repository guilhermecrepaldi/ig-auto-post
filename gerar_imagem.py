"""
Geração de imagem profissional para post do Instagram.
6 templates visuais com paletas de cores, fontes Google e elementos decorativos.
+ Carrossel de notícias (4 slides) para AI NEWS.
"""
import os
import random
import re
import textwrap
from pathlib import Path
from datetime import datetime

PASTA = Path(__file__).parent
TEMPLATES_DIR = PASTA / "templates"
POSTS_DIR = PASTA / "posts"

# ============================================================
# PALETAS DE CORES POR TEMA
# ============================================================
PALETAS = {
    "dica": {
        "bg_top": "#0a1628", "bg_bot": "#1a2a4a",
        "accent": "#00d4ff", "secundaria": "#0088cc",
        "hashtag_cor": "#66e0ff", "box_fill": "#0d1f3d",
    },
    "projeto": {
        "bg_top": "#1a0a2e", "bg_bot": "#2d1b4e",
        "accent": "#a855f7", "secundaria": "#7c3aed",
        "hashtag_cor": "#c084fc", "box_fill": "#1f0f3a",
    },
    "reflexao": {
        "bg_top": "#0a1a0a", "bg_bot": "#1a3a1a",
        "accent": "#22c55e", "secundaria": "#16a34a",
        "hashtag_cor": "#86efac", "box_fill": "#0f2a0f",
    },
    "case": {
        "bg_top": "#1a1410", "bg_bot": "#3a2a1a",
        "accent": "#f59e0b", "secundaria": "#d97706",
        "hashtag_cor": "#fcd34d", "box_fill": "#2a1f10",
    },
    "citacao": {
        "bg_top": "#1a0a0a", "bg_bot": "#3a1a1a",
        "accent": "#ef4444", "secundaria": "#dc2626",
        "hashtag_cor": "#fca5a5", "box_fill": "#2a0f0f",
    },
    "carrossel": {
        "bg_top": "#0a0a1a", "bg_bot": "#1a1a3a",
        "accent": "#06b6d4", "secundaria": "#0891b2",
        "hashtag_cor": "#67e8f9", "box_fill": "#0d0d2b",
    }
}

NOMES_TEMPLATES = list(PALETAS.keys())

EMOJIS_TEMPLATE = {
    "dica": ["💡", "⚡", "🔧", "🛠️", "📌"],
    "projeto": ["🚀", "🔥", "⚙️", "🏗️", "📦"],
    "reflexao": ["💭", "🌱", "🎯", "🧠", "💫"],
    "case": ["📊", "🏆", "🎖️", "💼", "📈"],
    "citacao": ["💬", "✨", "🌟", "📝", "🎭"],
    "carrossel": ["📸", "🎬", "🔄", "1️⃣", "2️⃣"]
}


def carregar_fonte(nome, tamanho):
    caminhos = [
        TEMPLATES_DIR / nome,
        TEMPLATES_DIR / nome.replace("Inter", "Poppins"),
    ]
    for c in caminhos:
        if c.exists():
            try:
                from PIL import ImageFont
                return ImageFont.truetype(str(c), tamanho)
            except Exception:
                pass
    from PIL import ImageFont
    return ImageFont.load_default()


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# ====================================================================
# POST SIMPLES (legenda única com template)
# ====================================================================

def gerar_imagem_post(legenda, config):
    POSTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

    template_escolhido = random.choice(NOMES_TEMPLATES)
    paleta = PALETAS[template_escolhido]
    emoji = random.choice(EMOJIS_TEMPLATE[template_escolhido])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = POSTS_DIR / f"post_{template_escolhido}_{timestamp}.jpg"

    return _gerar_template_post(legenda, caminho, paleta, template_escolhido, emoji, config)


def _gerar_template_post(legenda, caminho, paleta, template_nome, emoji, config):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1080, 1080
    bg_top = hex_to_rgb(paleta["bg_top"])
    bg_bot = hex_to_rgb(paleta["bg_bot"])
    accent = hex_to_rgb(paleta["accent"])
    secundaria = hex_to_rgb(paleta["secundaria"])
    box_fill = hex_to_rgb(paleta["box_fill"])

    img = Image.new("RGB", (W, H), bg_top)
    draw = ImageDraw.Draw(img)

    # Gradiente
    for y in range(H):
        ratio = y / H
        r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * ratio)
        g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * ratio)
        b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Padrão geométrico
    for _ in range(12):
        cx = random.randint(0, W)
        cy = random.randint(0, H)
        raio = random.randint(40, 100)
        draw.ellipse([cx-raio, cy-raio, cx+raio, cy+raio],
                      fill=None, outline=accent + (12,), width=1)

    # Barra superior
    draw.rectangle([(60, 60), (W - 60, 66)], fill=accent)

    # Avatar
    ax, ay = 100, 160
    draw.ellipse([ax-40, ay-40, ax+40, ay+40], fill=accent, outline=secundaria, width=3)
    draw.text((ax, ay), emoji, fill="white", anchor="mm")

    # Tag + subtag
    font_tag = carregar_fonte("Inter-Bold.ttf", 22)
    draw.text((ax + 55, ay - 12), template_nome.upper(), fill=accent, anchor="lm", font=font_tag)
    font_sub = carregar_fonte("Inter-Regular.ttf", 16)
    subtags = {"dica": "DICA RAPIDA", "projeto": "PROJETO", "reflexao": "REFLEXAO",
               "case": "CASE", "citacao": "CITACAO", "carrossel": "CARROSSEL"}
    draw.text((ax + 55, ay + 12), subtags.get(template_nome, "POST"), fill="#888888", anchor="lm", font=font_sub)

    # Box de fundo
    for y in range(260, 780):
        alpha_box = max(0, 40 - int((y - 260) / 520 * 20))
        draw.line([(80, y), (1000, y)], fill=box_fill[:3] + (alpha_box,))

    # Texto
    font_titulo = carregar_fonte("Inter-SemiBold.ttf", 22)
    font_texto = carregar_fonte("Inter-Regular.ttf", 40)
    legenda_limpa = re.sub(r'[^\x00-\x7F]+', '', legenda).strip()
    linhas = textwrap.wrap(legenda_limpa, width=30)

    if linhas:
        titulo = linhas[0]
        if len(titulo) > 35:
            m = re.match(r'^([^.!?]+[.!?])', titulo)
            titulo = m.group(1) if m else titulo[:35] + "\u2026"
        draw.text((W // 2, 290), titulo, fill=accent, anchor="mt", font=font_titulo)
        yt = 350
        for linha in linhas[1:6]:
            draw.text((W // 2, yt), linha, fill="white", anchor="mt", font=font_texto)
            yt += 55

    # Linha inferior
    draw.rectangle([(W//2 - 150, 790), (W//2 + 150, 794)], fill=accent)

    # Credito
    font_cred = carregar_fonte("Inter-Regular.ttf", 18)
    draw.text((W // 2, 830), f"@{config.get('instagram', {}).get('username', 'ig-auto-post')}",
              fill="#666666", anchor="mt", font=font_cred)

    # Hashtags
    font_hash = carregar_fonte("Inter-Regular.ttf", 28)
    hashtags = config.get("post", {}).get("hashtags_padrao", ["dev", "python"])
    hash_text = "  ".join(f"#{h}" for h in hashtags[:4])
    draw.rectangle([(0, H - 100), (W, H)], fill=bg_bot[:3] + (180,))
    draw.text((W // 2, H - 60), hash_text, fill=paleta["hashtag_cor"], anchor="mt", font=font_hash)

    # Data
    font_data = carregar_fonte("Inter-Regular.ttf", 16)
    draw.text((W - 40, H - 30), datetime.now().strftime("%d/%m/%Y - %H:%M"),
              fill="#444444", anchor="rb", font=font_data)

    img.save(caminho, "JPEG", quality=92)
    print(f"   Imagem gerada [{template_nome}]: {caminho.name}")
    return str(caminho)


# ====================================================================
# CARROSSEL DE NOTICIAS (4 slides para AI NEWS)
# ====================================================================

def gerar_carrossel_noticias(noticias, config):
    """Gera 4 imagens de carrossel, uma para cada noticia."""
    POSTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminhos = []

    for i, noticia in enumerate(noticias[:4]):
        paleta = list(PALETAS.values())[i % len(PALETAS)]
        emoji = noticia.get("emoji", "📰")
        caminho = POSTS_DIR / f"carrossel_{i+1}_{timestamp}.jpg"

        from PIL import Image, ImageDraw, ImageFont

        W, H = 1080, 1080
        bg_top = hex_to_rgb(paleta["bg_top"])
        bg_bot = hex_to_rgb(paleta["bg_bot"])
        accent = hex_to_rgb(paleta["accent"])
        secundaria = hex_to_rgb(paleta["secundaria"])
        box_fill = hex_to_rgb(paleta["box_fill"])

        img = Image.new("RGB", (W, H), bg_top)
        draw = ImageDraw.Draw(img)

        # Gradiente
        for y in range(H):
            ratio = y / H
            r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * ratio)
            g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * ratio)
            b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * ratio)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        # Bolinhas indicadoras
        for j in range(4):
            cx = W // 2 - 60 + j * 40
            cy = 50
            cor = accent if j == i else (60, 60, 60)
            draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=cor)

        # Barra decorativa
        draw.rectangle([(60, 80), (W - 60, 86)], fill=accent)

        # Badge AI NEWS
        font_badge = carregar_fonte("Inter-Bold.ttf", 20)
        draw.text((W // 2, 130), f"{emoji}  AI NEWS  {emoji}",
                  fill=accent, anchor="mt", font=font_badge)

        # Numero
        font_num = carregar_fonte("Inter-Bold.ttf", 60)
        draw.text((W // 2, 200), f"0{noticia['numero']}", fill=secundaria,
                  anchor="mt", font=font_num)

        # Fonte
        if noticia.get("fonte"):
            font_fonte = carregar_fonte("Inter-Regular.ttf", 18)
            draw.text((W // 2, 260), f"Fonte: {noticia['fonte']}",
                      fill="#888888", anchor="mt", font=font_fonte)

        # Titulo
        font_tit = carregar_fonte("Inter-SemiBold.ttf", 34)
        tit_linhas = textwrap.wrap(noticia["titulo"], width=28)
        yt = 320
        for linha in tit_linhas[:4]:
            draw.text((W // 2, yt), linha, fill="white", anchor="mt", font=font_tit)
            yt += 46

        # Resumo
        font_res = carregar_fonte("Inter-Regular.ttf", 24)
        res_linhas = textwrap.wrap(noticia["resumo"], width=40)
        yr = yt + 25
        for linha in res_linhas[:3]:
            draw.text((W // 2, yr), linha, fill="#cccccc", anchor="mt", font=font_res)
            yr += 36

        # Linha decorativa
        draw.rectangle([(W//2 - 120, 780), (W//2 + 120, 784)], fill=accent)

        # CTA
        font_cta = carregar_fonte("Inter-Regular.ttf", 22)
        cta_lista = [
            "Saiba mais em crepaldi.ai.news",
            "IA que transforma",
            "Leia o artigo completo",
            "Fique por dentro da IA",
        ]
        draw.text((W // 2, 820), cta_lista[i % 4], fill="#666666", anchor="mt", font=font_cta)

        # Hashtags
        font_hash = carregar_fonte("Inter-Regular.ttf", 26)
        draw.rectangle([(0, H - 100), (W, H)], fill=bg_bot[:3] + (180,))
        draw.text((W // 2, H - 60), "#IA #AI #Noticias #Tecnologia #MachineLearning",
                  fill=paleta["hashtag_cor"], anchor="mt", font=font_hash)

        # Slide
        font_sl = carregar_fonte("Inter-Regular.ttf", 16)
        draw.text((W - 40, H - 30), f"Slide {i+1}/4",
                  fill="#444444", anchor="rb", font=font_sl)

        img.save(caminho, "JPEG", quality=92)
        print(f"   Slide {i+1}/4: {caminho.name}")
        caminhos.append(str(caminho))

    return caminhos
