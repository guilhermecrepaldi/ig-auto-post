"""
Geracao de imagem profissional para post do Instagram.
Suporta: posts simples + carrossel AI NEWS com categorias, datas e fundos contextuais.
"""
import os
import random
import re
import textwrap
import math
from pathlib import Path
from datetime import datetime

PASTA = Path(__file__).parent
TEMPLATES_DIR = PASTA / "templates"
POSTS_DIR = PASTA / "posts"

# ============================================================
# PALETAS POR CATEGORIA
# ============================================================
PALETAS_CATEGORIA = {
    "capa": {
        "bg_top": "#0f0f23", "bg_bot": "#1a1a3e",
        "accent": "#7c3aed", "secundaria": "#a855f7",
        "hashtag": "#c084fc",
    },
    "arquitetura": {
        "bg_top": "#0a1628", "bg_bot": "#0f2a4a",
        "accent": "#00d4ff", "secundaria": "#0088cc",
        "hashtag": "#66e0ff",
    },
    "hardware": {
        "bg_top": "#0a1a0a", "bg_bot": "#0f3a0f",
        "accent": "#22c55e", "secundaria": "#16a34a",
        "hashtag": "#86efac",
    },
    "tendencias": {
        "bg_top": "#1a1008", "bg_bot": "#3a2010",
        "accent": "#f59e0b", "secundaria": "#d97706",
        "hashtag": "#fcd34d",
    },
}

# Pattern SVG-like por categoria (desenhado com Pillow)
FUNDOS_PATTERN = {
    "capa": "circuitos",
    "arquitetura": "rede",
    "hardware": "grade",
    "tendencias": "ondas",
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


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# ====================================================================
# FUNDOS CONTEXTUAIS (patterns geométricos)
# ====================================================================

def desenhar_fundo_contextual(draw, W, H, paleta, padrao):
    """Desenha padrao geometrico de fundo baseado na categoria."""
    accent = hex_to_rgb(paleta["accent"])
    secundaria = hex_to_rgb(paleta["secundaria"])
    alpha = 12  # bem sutil

    if padrao == "circuitos":
        # Linhas retas horizontais/verticais
        for _ in range(20):
            x = random.randint(0, W)
            y = random.randint(0, H)
            if random.random() > 0.5:
                draw.line([(x, y), (x + random.randint(60, 200), y)],
                          fill=accent + (alpha,), width=1)
            else:
                draw.line([(x, y), (x, y + random.randint(60, 200))],
                          fill=accent + (alpha,), width=1)
            # Circulo nas juncoes
            draw.ellipse([x-4, y-4, x+4, y+4], fill=accent + (alpha + 5,))

    elif padrao == "rede":
        # Nos conectados
            nos = [(random.randint(50, W-50), random.randint(50, H-50)) for _ in range(12)]
            for (x1, y1) in nos:
                for (x2, y2) in nos:
                    if random.random() > 0.7:
                        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                        if dist < 300:
                            draw.line([(x1, y1), (x2, y2)],
                                      fill=secundaria + (alpha - 3,), width=1)
            for (x, y) in nos:
                draw.ellipse([x-6, y-6, x+6, y+6], fill=accent + (alpha + 5,))

    elif padrao == "grade":
        # Grid de pontos (chip)
        for x in range(0, W, 60):
            for y in range(0, H, 60):
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                draw.ellipse([x+offset_x-2, y+offset_y-2, x+offset_x+2, y+offset_y+2],
                             fill=accent + (alpha,))

    elif padrao == "ondas":
        # Ondas senoidais (grafico)
        for onda in range(3):
            y_base = H * (0.3 + onda * 0.2)
            pontos = []
            for x in range(0, W, 10):
                y = y_base + math.sin(x * 0.02 + onda * 2) * 40
                pontos.append((x, y))
            for i in range(len(pontos) - 1):
                draw.line([pontos[i], pontos[i+1]],
                          fill=accent + (alpha - 3,), width=1)

    elif padrao == "hexagono":
        # Hexagonos (blockchain)
        for _ in range(30):
            cx = random.randint(50, W-50)
            cy = random.randint(50, H-50)
            raio = random.randint(20, 50)
            pontos = []
            for ang in range(0, 360, 60):
                rad = math.radians(ang)
                px = cx + raio * math.cos(rad)
                py = cy + raio * math.sin(rad)
                pontos.append((px, py))
            for i in range(6):
                draw.line([pontos[i], pontos[(i+1) % 6]],
                          fill=accent + (alpha - 2,), width=1)

    else:  # estrelas / encerramento
        for _ in range(40):
            cx = random.randint(0, W)
            cy = random.randint(0, H)
            sz = random.randint(1, 3)
            draw.ellipse([cx-sz, cy-sz, cx+sz, cy+sz], fill=accent + (alpha + 5,))


# ====================================================================
# CARROSSEL AI NEWS (6+ slides)
# ====================================================================

def gerar_carrossel_noticias(noticias, config):
    """Gera carrossel com capa + noticias + encerramento."""
    POSTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminhos = []

    total_slides = len(noticias)

    for idx, slide_data in enumerate(noticias):
        tipo = slide_data.get("tipo", "noticia")
        # Categoria correta: se for capa/en不忍, usa direto; se for noticia, usa a categoria da noticia
        if tipo in ("capa", "encerramento"):
            categoria = tipo
        else:
            categoria = slide_data.get("categoria", "tendencias")
        paleta = PALETAS_CATEGORIA.get(categoria, PALETAS_CATEGORIA["tendencias"])
        padrao = FUNDOS_PATTERN.get(categoria, "rede")

        caminho = POSTS_DIR / f"ainews_{idx+1}_{timestamp}.jpg"

        from PIL import Image, ImageDraw, ImageFont

        W, H = 1080, 1080
        bg_top = hex_to_rgb(paleta["bg_top"])
        bg_bot = hex_to_rgb(paleta["bg_bot"])
        accent = hex_to_rgb(paleta["accent"])
        secundaria = hex_to_rgb(paleta["secundaria"])

        img = Image.new("RGB", (W, H), bg_top)
        draw = ImageDraw.Draw(img)

        # Fundo contextual: imagem real por categoria
        bg_image_path = PASTA / "assets" / f"{categoria}_bg.jpg"
        usa_imagem_fundo = False
        if bg_image_path.exists():
            try:
                bg_img = Image.open(str(bg_image_path)).convert("RGB").resize((W, H), Image.LANCZOS)
                # Misturar com gradiente escuro (30% imagem + 70% gradiente)
                grad = Image.new("RGB", (W, H), bg_top)
                for y in range(H):
                    ratio = y / H
                    r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * ratio)
                    g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * ratio)
                    b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * ratio)
                    grad.putpixel((0, y), (r, g, b))
                    for x in range(1, W):
                        grad.putpixel((x, y), (r, g, b))
                img = Image.blend(bg_img, grad, 0.5)
                draw = ImageDraw.Draw(img)
                usa_imagem_fundo = True
            except Exception as e:
                print(f"   Aviso: fundo {bg_image_path} falhou: {e}")

        if not usa_imagem_fundo:
            # Gradiente puro
            for y in range(H):
                ratio = y / H
                r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * ratio)
                g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * ratio)
                b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * ratio)
                draw.line([(0, y), (W, y)], fill=(r, g, b))

        # Fundo contextual geometrico (so se nao tiver imagem real)
        if not usa_imagem_fundo:
            desenhar_fundo_contextual(draw, W, H, paleta, padrao)

        # Bolinhas de progresso
        for j in range(total_slides):
            cx = W // 2 - (total_slides * 20) + j * 40
            cy = 40
            cor = accent if j == idx else (50, 50, 50)
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=cor)

        # Barra decorativa
        draw.rectangle([(60, 65), (W - 60, 70)], fill=accent)

        if tipo == "capa":
            _desenhar_capa(draw, W, H, slide_data, paleta)
        elif tipo == "devimpact":
            _desenhar_devimpact(draw, W, H, slide_data, paleta)
        elif tipo == "separador":
            _desenhar_separador(draw, W, H, slide_data, paleta)
        else:
            _desenhar_noticia(draw, W, H, slide_data, paleta)

        # Slide counter
        font_sl = carregar_fonte("Inter-Regular.ttf", 14)
        draw.text((W - 30, H - 25), f"{idx+1}/{total_slides}",
                  fill="#555555", anchor="rb", font=font_sl)

        img.save(caminho, "JPEG", quality=92)
        print(f"   Slide {idx+1}/{total_slides} [{categoria}]: {caminho.name}")
        caminhos.append(str(caminho))

    return caminhos


def _desenhar_capa(draw, W, H, slide, paleta):
    """Slide de capa do carrossel."""
    accent = hex_to_rgb(paleta["accent"])
    secundaria = hex_to_rgb(paleta["secundaria"])

    font_tit = carregar_fonte("Inter-Bold.ttf", 72)
    font_sub = carregar_fonte("Inter-Regular.ttf", 28)
    font_data = carregar_fonte("Inter-Regular.ttf", 20)

    # Logo grande
    draw.text((W // 2, H // 2 - 100), "AI NEWS",
              fill="white", anchor="mm", font=font_tit)

    # Linha decorativa
    draw.rectangle([(W//2 - 120, H//2 - 25), (W//2 + 120, H//2 - 20)], fill=accent)

    # Subtitulo
    draw.text((W // 2, H // 2 + 40), slide.get("subtitulo", "As principais noticias de IA"),
              fill="#aaaaaa", anchor="mm", font=font_sub)

    # Data
    data = slide.get("data_str", datetime.now().strftime("%d/%m/%Y"))
    draw.text((W // 2, H // 2 + 100), data,
              fill="#666666", anchor="mm", font=font_data)

    # Hashtags no rodape
    font_hash = carregar_fonte("Inter-Regular.ttf", 22)
    draw.rectangle([(0, H - 90), (W, H)], fill=(10, 10, 20, 180))
    draw.text((W // 2, H - 55), "#IA #AI #Noticias #Tecnologia",
              fill=paleta["hashtag"], anchor="mt", font=font_hash)


def _desenhar_noticia(draw, W, H, slide, paleta):
    """Slide de noticia com info completa: titulo + bullet-fact + impacto."""
    accent = hex_to_rgb(paleta["accent"])
    secundaria = hex_to_rgb(paleta["secundaria"])

    # Badge + data na mesma linha (economiza espaco)
    font_badge = carregar_fonte("Inter-Bold.ttf", 14)
    cat_info = slide.get("categoria", "tendencias").upper()
    draw.rectangle([(W//2 - 100, 90), (W//2 + 100, 118)], fill=secundaria + (60,))
    draw.text((W // 2, 104), f"  {cat_info}  ", fill=accent, anchor="mt", font=font_badge)

    data = slide.get("data_str", "")
    font_data = carregar_fonte("Inter-Regular.ttf", 15)
    draw.text((W // 2, 140), f"📅 {data}", fill="#777777", anchor="mt", font=font_data)

    # TITULO - maior possivel
    font_tit = carregar_fonte("Inter-SemiBold.ttf", 28)
    tit_linhas = textwrap.wrap(slide["titulo"], width=30)
    yt = 185
    for linha in tit_linhas[:3]:
        draw.text((W // 2, yt), linha, fill="white", anchor="mt", font=font_tit)
        yt += 36

    # FACT como bullets curtos
    fact = slide.get("fact", "") or slide.get("resumo", "")
    bullets = slide.get("bullets", [])

    if bullets:
        font_fact = carregar_fonte("Inter-Regular.ttf", 18)
        yf = yt + 12
        for bullet in bullets[:3]:
            btext = f"▸ {bullet}"
            lines = textwrap.wrap(btext, width=50)
            for line in lines[:2]:
                if yf > 720:
                    break
                draw.text((W // 2, yf), line, fill="#bbbbbb", anchor="mt", font=font_fact)
                yf += 24
        yt = yf
    elif fact:
        frases = [f.strip() for f in fact.replace(". ", ".@@").replace("! ", "!@@").replace("? ", "?@@").split("@@") if f.strip()]
        font_fact = carregar_fonte("Inter-Regular.ttf", 18)
        yf = yt + 12
        for frase in frases[:3]:
            if len(frase) > 100:
                frase = frase[:97] + "..."
            bullet = f"▸ {frase}"
            lines = textwrap.wrap(bullet, width=50)
            for line in lines[:2]:
                if yf > 720:
                    break
                draw.text((W // 2, yf), line, fill="#bbbbbb", anchor="mt", font=font_fact)
                yf += 24
        yt = yf

    # IMPACTO - bullets curtos
    imp_bullets = slide.get("imp_bullets", [])
    impact = slide.get("impact", "")

    if imp_bullets:
        font_imp_label = carregar_fonte("Inter-Bold.ttf", 13)
        font_imp = carregar_fonte("Inter-Regular.ttf", 17)
        yi = yt + 15
        if yi < 720:
            draw.text((W // 2, yi), "IMPACTO", fill=accent, anchor="mt", font=font_imp_label)
            yi += 20
            for ib in imp_bullets[:2]:
                ibtext = f"▸ {ib}"
                ib_lines = textwrap.wrap(ibtext, width=48)
                for line in ib_lines[:2]:
                    if yi > 760:
                        break
                    draw.text((W // 2, yi), line, fill="#cccccc", anchor="mt", font=font_imp)
                    yi += 22
    elif impact:
        imp_short = impact[:250]
        font_imp_label = carregar_fonte("Inter-Bold.ttf", 13)
        font_imp = carregar_fonte("Inter-Regular.ttf", 17)
        yi = yt + 15
        if yi < 720:
            draw.text((W // 2, yi), "IMPACTO", fill=accent, anchor="mt", font=font_imp_label)
            yi += 20
            imp_lines = textwrap.wrap(imp_short, width=48)
            for line in imp_lines[:2]:
                if yi > 760:
                    break
                draw.text((W // 2, yi), line, fill="#cccccc", anchor="mt", font=font_imp)
                yi += 22

    # Fonte
    fonte = slide.get("fonte", "")
    if fonte:
        font_fonte = carregar_fonte("Inter-Regular.ttf", 14)
        draw.text((W // 2, H - 140), f"Fonte: {fonte}",
                  fill="#555555", anchor="mt", font=font_fonte)

    # Linha decorativa
    draw.rectangle([(W//2 - 100, H - 115), (W//2 + 100, H - 111)], fill=accent)

    # Hashtags
    font_hash = carregar_fonte("Inter-Regular.ttf", 20)
    draw.rectangle([(0, H - 90), (W, H)], fill=(0, 0, 0, 40))
    draw.text((W // 2, H - 55), "#IA #AI #Noticias #Tecnologia",
              fill=paleta["hashtag"], anchor="mt", font=font_hash)


def _desenhar_encerramento(draw, W, H, slide, paleta):
    pass


def _desenhar_devimpact(draw, W, H, slide, paleta):
    """Slide 'O que muda pro Dev'."""
    accent = hex_to_rgb(paleta["accent"])
    font_tit = carregar_fonte("Inter-Bold.ttf", 36)
    font_texto = carregar_fonte("Inter-Regular.ttf", 26)
    draw.text((W // 2, 140), "🧑‍💻", fill="white", anchor="mt",
              font=carregar_fonte("Inter-Regular.ttf", 60))
    draw.text((W // 2, 230), slide.get("titulo", "O que muda pro Dev"),
              fill="white", anchor="mt", font=font_tit)
    draw.rectangle([(W//2 - 100, 270), (W//2 + 100, 274)], fill=accent)
    texto = slide.get("texto", "")
    if texto:
        yt = 320
        for linha in texto.split("\n"):
            if linha.strip():
                draw.text((W // 2, yt), linha.strip(), fill="#cccccc",
                          anchor="mt", font=font_texto)
                yt += 40
    font_hash = carregar_fonte("Inter-Regular.ttf", 22)
    draw.rectangle([(0, H - 90), (W, H)], fill=(0, 0, 0, 40))
    draw.text((W // 2, H - 55), "#Dev #Programacao #Carreira #Tecnologia",
              fill=paleta["hashtag"], anchor="mt", font=font_hash)


def _desenhar_separador(draw, W, H, slide, paleta):
    """Slide separador de categoria."""
    accent = hex_to_rgb(paleta["accent"])
    font_emoji = carregar_fonte("Inter-Regular.ttf", 72)
    font_tit = carregar_fonte("Inter-Bold.ttf", 48)
    font_sub = carregar_fonte("Inter-Regular.ttf", 24)
    draw.text((W // 2, H // 2 - 80), slide.get("emoji", "🏗️"),
              fill="white", anchor="mm", font=font_emoji)
    draw.text((W // 2, H // 2), slide.get("titulo", ""),
              fill="white", anchor="mm", font=font_tit)
    draw.rectangle([(W//2 - 100, H//2 + 40), (W//2 + 100, H//2 + 44)], fill=accent)
    draw.text((W // 2, H // 2 + 80), slide.get("subtitulo", ""),
              fill="#888888", anchor="mm", font=font_sub)
    font_hash = carregar_fonte("Inter-Regular.ttf", 22)
    draw.rectangle([(0, H - 90), (W, H)], fill=(0, 0, 0, 40))
    draw.text((W // 2, H - 55), "#IA #AI #Noticias #Tecnologia",
              fill=paleta["hashtag"], anchor="mt", font=font_hash)


# ====================================================================
# POST SIMPLES (legacy)
# ====================================================================

def gerar_imagem_post(legenda, config):
    """Post unico com template aleatorio."""
    POSTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

    paleta = list(PALETAS_CATEGORIA.values())[random.randint(0, 3)]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = POSTS_DIR / f"post_{timestamp}.jpg"

    from PIL import Image, ImageDraw, ImageFont

    W, H = 1080, 1080
    bg_top = hex_to_rgb(paleta["bg_top"])
    bg_bot = hex_to_rgb(paleta["bg_bot"])
    accent = hex_to_rgb(paleta["accent"])
    secundaria = hex_to_rgb(paleta["secundaria"])

    img = Image.new("RGB", (W, H), bg_top)
    draw = ImageDraw.Draw(img)

    for y in range(H):
        ratio = y / H
        r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * ratio)
        g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * ratio)
        b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    font_tit = carregar_fonte("Inter-SemiBold.ttf", 22)
    font_texto = carregar_fonte("Inter-Regular.ttf", 36)
    legenda_limpa = re.sub(r'[^\x00-\x7F]+', '', legenda).strip()
    linhas = textwrap.wrap(legenda_limpa, width=30)

    if linhas:
        titulo = linhas[0]
        if len(titulo) > 35:
            m = re.match(r'^([^.!?]+[.!?])', titulo)
            titulo = m.group(1) if m else titulo[:35] + "\u2026"
        draw.text((W//2, 200), titulo, fill=accent, anchor="mt", font=font_tit)
        yt = 260
        for linha in linhas[1:6]:
            draw.text((W//2, yt), linha, fill="white", anchor="mt", font=font_texto)
            yt += 50

    draw.text((W//2, H-80), f"@{config.get('instagram',{}).get('username','ig-auto-post')}",
              fill="#666666", anchor="mt",
              font=carregar_fonte("Inter-Regular.ttf", 18))

    img.save(caminho, "JPEG", quality=92)
    print(f"   Post gerado: {caminho.name}")
    return str(caminho)
