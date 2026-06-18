"""
Geração de imagem profissional para post do Instagram.
6 templates visuais com paletas de cores, fontes Google e elementos decorativos.
"""
import os
import random
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
        "titulo_cor": "#00d4ff", "texto_cor": "#ffffff",
        "hashtag_cor": "#66e0ff", "box_fill": "#0d1f3d",
        "barra": "#00d4ff", "nome": "Ocean Tech"
    },
    "projeto": {
        "bg_top": "#1a0a2e", "bg_bot": "#2d1b4e",
        "accent": "#a855f7", "secundaria": "#7c3aed",
        "titulo_cor": "#a855f7", "texto_cor": "#ffffff",
        "hashtag_cor": "#c084fc", "box_fill": "#1f0f3a",
        "barra": "#a855f7", "nome": "Neon Purple"
    },
    "reflexao": {
        "bg_top": "#0a1a0a", "bg_bot": "#1a3a1a",
        "accent": "#22c55e", "secundaria": "#16a34a",
        "titulo_cor": "#4ade80", "texto_cor": "#ffffff",
        "hashtag_cor": "#86efac", "box_fill": "#0f2a0f",
        "barra": "#22c55e", "nome": "Forest Green"
    },
    "case": {
        "bg_top": "#1a1410", "bg_bot": "#3a2a1a",
        "accent": "#f59e0b", "secundaria": "#d97706",
        "titulo_cor": "#fbbf24", "texto_cor": "#ffffff",
        "hashtag_cor": "#fcd34d", "box_fill": "#2a1f10",
        "barra": "#f59e0b", "nome": "Amber Dark"
    },
    "citacao": {
        "bg_top": "#1a0a0a", "bg_bot": "#3a1a1a",
        "accent": "#ef4444", "secundaria": "#dc2626",
        "titulo_cor": "#f87171", "texto_cor": "#ffffff",
        "hashtag_cor": "#fca5a5", "box_fill": "#2a0f0f",
        "barra": "#ef4444", "nome": "Ruby Red"
    },
    "carrossel": {
        "bg_top": "#0a0a1a", "bg_bot": "#1a1a3a",
        "accent": "#06b6d4", "secundaria": "#0891b2",
        "titulo_cor": "#22d3ee", "texto_cor": "#ffffff",
        "hashtag_cor": "#67e8f9", "box_fill": "#0d0d2b",
        "barra": "#06b6d4", "nome": "Cyan Dark"
    }
}

# Nomes dos templates para seleção
NOMES_TEMPLATES = list(PALETAS.keys())

# Emojis por template
EMOJIS_TEMPLATE = {
    "dica": ["💡", "⚡", "🔧", "🛠️", "📌"],
    "projeto": ["🚀", "🔥", "⚙️", "🏗️", "📦"],
    "reflexao": ["💭", "🌱", "🎯", "🧠", "💫"],
    "case": ["📊", "🏆", "🎖️", "💼", "📈"],
    "citacao": ["💬", "✨", "🌟", "📝", "🎭"],
    "carrossel": ["📸", "🎬", "🔄", "1️⃣", "2️⃣"]
}


def carregar_fonte(nome, tamanho):
    """Carrega fonte do diretório templates/ com fallback."""
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


def gerar_imagem_post(legenda, config):
    """Gera imagem para post com template visual profissional."""
    POSTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

    # Seleciona template (cíclico ou aleatório)
    templates_cfg = config.get("templates", NOMES_TEMPLATES)
    modo = config.get("post", {}).get("modo", "auto")

    if modo == "auto":
        # Pega template baseado no nome ou aleatório
        template_escolhido = random.choice(NOMES_TEMPLATES)
    else:
        template_escolhido = random.choice(NOMES_TEMPLATES)

    paleta = PALETAS.get(template_escolhido, PALETAS["dica"])
    emoji = random.choice(EMOJIS_TEMPLATE.get(template_escolhido, EMOJIS_TEMPLATE["dica"]))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = POSTS_DIR / f"post_{template_escolhido}_{timestamp}.jpg"

    return gerar_template(legenda, caminho, paleta, template_escolhido, emoji, config)


def hex_to_rgb(hex_color):
    """Converte #rrggbb para tupla (r,g,b)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def gerar_template(legenda, caminho, paleta, template_nome, emoji, config):
    """Cria imagem com layout profissional."""
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1080, 1080
    bg_top = hex_to_rgb(paleta["bg_top"])
    bg_bot = hex_to_rgb(paleta["bg_bot"])
    accent = hex_to_rgb(paleta["accent"])
    secundaria = hex_to_rgb(paleta["secundaria"])
    box_fill = hex_to_rgb(paleta["box_fill"])

    img = Image.new("RGB", (W, H), bg_top)
    draw = ImageDraw.Draw(img)

    # ---- GRADIENTE VERTICAL ----
    for y in range(H):
        ratio = y / H
        r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * ratio)
        g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * ratio)
        b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # ---- PADRÃO GEOMÉTRICO SUTIL (círculos) ----
    for _ in range(15):
        cx = random.randint(0, W)
        cy = random.randint(0, H)
        raio = random.randint(30, 120)
        alpha = 5
        cor = accent[:3] + (alpha,)
        draw.ellipse([cx-raio, cy-raio, cx+raio, cy+raio],
                      fill=None, outline=accent + (15,), width=1)

    # ---- BARRA DECORATIVA SUPERIOR ----
    barra_h = 6
    draw.rectangle([(60, 60), (W - 60, 60 + barra_h)], fill=accent)

    # ---- AVATAR/ÍCONE (círculo com emoji) ----
    avatar_centro_x, avatar_centro_y = 100, 160
    avatar_raio = 40
    draw.ellipse([avatar_centro_x - avatar_raio, avatar_centro_y - avatar_raio,
                  avatar_centro_x + avatar_raio, avatar_centro_y + avatar_raio],
                 fill=accent, outline=secundaria, width=3)
    # Emoji no centro do avatar
    font_emoji = ImageFont.load_default()
    draw.text((avatar_centro_x, avatar_centro_y), emoji,
              fill="white", anchor="mm", font=font_emoji)

    # ---- TAG DO TEMPLATE ----
    font_tag = carregar_fonte("Inter-Bold.ttf", 22)
    tag_text = template_nome.upper()
    draw.text((avatar_centro_x + avatar_raio + 20, avatar_centro_y - 12),
              tag_text, fill=accent, anchor="lm", font=font_tag)

    # ---- SUBTAG ----
    font_sub = carregar_fonte("Inter-Regular.ttf", 16)
    subtags = {
        "dica": "DICA RÁPIDA",
        "projeto": "PROJETO EM ANDAMENTO",
        "reflexao": "REFLEXÃO",
        "case": "CASE DE SUCESSO",
        "citacao": "CITAÇÃO",
        "carrossel": "CARROSSEL"
    }
    draw.text((avatar_centro_x + avatar_raio + 20, avatar_centro_y + 12),
              subtags.get(template_nome, "POST"), fill="#888888", anchor="lm", font=font_sub)

    # ---- BOX DE DESTAQUE (fundo semi-transparente para texto) ----
    margin_x = 80
    box_y1 = 260
    box_y2 = 780
    for y in range(box_y1, box_y2):
        alpha_box = max(0, 40 - int((y - box_y1) / (box_y2 - box_y1) * 20))
        draw.line([(margin_x, y), (W - margin_x, y)],
                  fill=box_fill[:3] + (alpha_box,))

    # ---- TEXTO PRINCIPAL (legenda) ----
    font_titulo = carregar_fonte("Inter-SemiBold.ttf", 22)
    font_texto = carregar_fonte("Inter-Regular.ttf", 40)

    # Limpar emojis da legenda (Pillow não renderiza bem)
    import re
    legenda_limpa = re.sub(r'[^\x00-\x7F]+', '', legenda).strip()

    # Primeira linha como título destacado
    linhas_legenda = textwrap.wrap(legenda_limpa, width=30)

    if linhas_legenda:
        # Título (primeira linha sem truncar)
        titulo = linhas_legenda[0]
        if len(titulo) > 35:
            # Pega só até o primeiro ponto ou exclamação
            import re
            m = re.match(r'^([^.!?]+[.!?])', titulo)
            if m:
                titulo = m.group(1)
            else:
                titulo = titulo[:35] + "…"
        draw.text((W // 2, 290), titulo, fill=accent,
                  anchor="mt", font=font_titulo)

        # Restante do texto (pula primeira linha que já virou título)
        y_texto = 350
        for linha in linhas_legenda[1:6]:
            draw.text((W // 2, y_texto), linha, fill=paleta["texto_cor"],
                      anchor="mt", font=font_texto)
            y_texto += 55

    # ---- LINHA DECORATIVA INFERIOR ----
    draw.rectangle([(W // 2 - 150, box_y2 + 10),
                    (W // 2 + 150, box_y2 + 14)], fill=accent)

    # ---- CRÉDITO / MARCA ----
    font_credito = carregar_fonte("Inter-Regular.ttf", 18)
    draw.text((W // 2, box_y2 + 50), f"@{config.get('instagram', {}).get('username', 'ig-auto-post')}",
              fill="#666666", anchor="mt", font=font_credito)

    # ---- HASHTAGS NO RODAPÉ ----
    font_hash = carregar_fonte("Inter-Regular.ttf", 28)
    hashtags = config.get("post", {}).get("hashtags_padrao", ["dev", "python"])
    hash_text = "  ".join(f"#{h}" for h in hashtags[:4])

    # Fundo escuro para hashtags
    draw.rectangle([(0, H - 100), (W, H)], fill=bg_bot[:3] + (180,))
    draw.text((W // 2, H - 60), hash_text, fill=paleta["hashtag_cor"],
              anchor="mt", font=font_hash)

    # ---- TIMESTAMP SUTIL ----
    font_data = carregar_fonte("Inter-Regular.ttf", 16)
    data_str = datetime.now().strftime("%d/%m/%Y • %H:%M")
    draw.text((W - 40, H - 30), data_str, fill="#444444",
              anchor="rb", font=font_data)

    # ---- NOME DO TEMPLATE NO CANTO SUPERIOR DIREITO (só debug) ----
    # Removido da imagem final - era resíduo de design

    img.save(caminho, "JPEG", quality=92)
    print(f"   ✅ Imagem gerada [{template_nome}]: {caminho.name}")
    return str(caminho)
