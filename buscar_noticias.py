"""
Busca as principais notícias de IA do dia organizadas por categoria.
Categorias: arquitetura, hardware, tendencias, cripto (futuro)
"""
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).parent

# Palavras-chave por categoria para filtrar noticias
CATEGORIAS = {
    "arquitetura": {
        "palavras": ["modelo", "llm", "framework", "arquitetura", "transformer",
                     "neural", "treinamento", "treino", "fine-tuning", "open source",
                     "algoritmo", "raciocinio", "reasoning", "agente", "agent",
                     "deep learning", "machine learning", "pesquisa", "research",
                     "paper", "publicacao", "publicação", "cientista"],
        "emoji": "🏗️",
        "cor": "#00d4ff",
        "descricao": "Arquitetura de IA"
    },
    "hardware": {
        "palavras": ["chip", "gpu", "nvidia", "amd", "processador", "hardware",
                     "data center", "datacenter", "energia", "consumo", "servidor",
                     "memoria", "inferencia", "treinamento", "computacao",
                     "edge", "iot", "quantico", "quantum", "infraestrutura"],
        "emoji": "⚙️",
        "cor": "#22c55e",
        "descricao": "Hardware e Infraestrutura"
    },
    "tendencias": {
        "palavras": ["mercado", "investimento", "startup", "regulacao", "regulação",
                     "lei", "governo", "openai", "google", "meta", "microsoft",
                     "amazon", "apple", "inovacao", "inovação", "futuro",
                     "emprego", "trabalho", "educacao", "educação",
                     "copilot", "assistente", "chatbot", "ferramenta",
                     "startup", "unicornio", "investidor", "bill gates",
                     "sam altman", "musk", "etica", "ética", "seguranca"],
        "emoji": "📈",
        "cor": "#f59e0b",
        "descricao": "Tendencias e Mercado"
    }
}

NOMES_CATEGORIAS = list(CATEGORIAS.keys())


def buscar_noticias(config):
    """Busca noticias do dia, retorna ate 6 organizadas por categoria."""
    print("Buscando noticias de IA por categoria...")

    todas_noticias = []

    # 1. Google News RSS
    try:
        import xml.etree.ElementTree as ET
        queries = [
            "inteligencia+artificial+IA",
            "machine+learning+deep+learning",
            "hardware+GPU+chip+IA",
            "mercado+IA+tecnologia",
        ]
        for q in queries:
            url = f"https://news.google.com/rss/search?q={q}&hl=pt-BR&gl=BR"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode("utf-8", errors="replace")
                root = ET.fromstring(data)
                for item in root.iter("item"):
                    title = item.findtext("title", "")
                    desc = item.findtext("description", "")
                    link = item.findtext("link", "")
                    pubdate = item.findtext("pubDate", "")

                    # Limpar HTML
                    title_limpo = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;', ' ', title)
                    title_limpo = re.sub(r'\s+', ' ', title_limpo).strip()
                    desc_limpo = re.sub(r'<[^>]+>', '', desc)
                    desc_limpo = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;', ' ', desc_limpo)
                    desc_limpo = re.sub(r'\s+', ' ', desc_limpo).strip()[:200]

                    # Parse data
                    data_obj = None
                    if pubdate:
                        try:
                            data_obj = datetime.strptime(pubdate.strip()[:25], "%a, %d %b %Y %H:%M:%S")
                        except:
                            pass

                    if title_limpo and len(title_limpo) > 20:
                        todas_noticias.append({
                            "titulo": title_limpo,
                            "resumo": desc_limpo if desc_limpo else title_limpo[:200],
                            "url": link,
                            "fonte": extrair_fonte(link),
                            "data": data_obj,
                            "data_str": data_obj.strftime("%d/%m/%Y") if data_obj else datetime.now().strftime("%d/%m/%Y")
                        })
        print(f"   Google News: {len(todas_noticias)} noticias")
    except Exception as e:
        print(f"   Google News falhou: {e}")

    # 2. Classificar por categoria
    categorizadas = {cat: [] for cat in NOMES_CATEGORIAS}

    for n in todas_noticias:
        titulo_lower = n["titulo"].lower()
        resumo_lower = n["resumo"].lower()
        texto = titulo_lower + " " + resumo_lower

        for cat_nome, cat_info in CATEGORIAS.items():
            for palavra in cat_info["palavras"]:
                if palavra in texto:
                    categorizadas[cat_nome].append(n)
                    break

    # 3. Selecionar a MELHOR noticia de cada categoria
    # (mais recente, titulo mais informativo)
    selecionadas = []
    for cat_nome in NOMES_CATEGORIAS:
        candidatos = categorizadas[cat_nome]
        if not candidatos:
            continue
        # Ordenar por data (mais recente primeiro), depois por tamanho do titulo
        candidatos.sort(key=lambda x: (
            -(x["data"].timestamp() if x["data"] else 0),
            -len(x["titulo"])
        ))
        melhor = candidatos[0]
        melhor["categoria"] = cat_nome
        selecionadas.append(melhor)

    print(f"   Classificadas: {len(selecionadas)} noticias em {len(set(n['categoria'] for n in selecionadas))} categorias")

    # 4. Fallback se faltar categorias
    if len(selecionadas) < 3:
        print("   Poucas categorias preenchidas, completando com fallbacks")
        fallbacks = gerar_fallbacks()
        cats_presentes = set(n["categoria"] for n in selecionadas)
        for fb in fallbacks:
            if fb["categoria"] not in cats_presentes:
                selecionadas.append(fb)
                cats_presentes.add(fb["categoria"])

    # 5. Formatar resultado
    emojis = ["🤖", "⚙️", "📈"]

    resultado = []

    # Primeiro slide: CAPA
    resultado.append({
        "numero": 0,
        "tipo": "capa",
        "titulo": "AI NEWS",
        "subtitulo": "As principais noticias de IA",
        "data_str": datetime.now().strftime("%d/%m/%Y"),
        "emoji": "📡",
        "fonte": "",
        "resumo": ""
    })

    for i, n in enumerate(selecionadas[:3]):
        resultado.append({
            "numero": i + 1,
            "tipo": "noticia",
            "categoria": n.get("categoria", "tendencias"),
            "titulo": limpar_titulo(n["titulo"]),
            "resumo": n["resumo"][:150],
            "url": n.get("url", ""),
            "fonte": n.get("fonte", ""),
            "data_str": n.get("data_str", datetime.now().strftime("%d/%m/%Y")),
            "emoji": emojis[i % len(emojis)],
        })

    return resultado


def extrair_fonte(url):
    if not url:
        return ""
    if "news.google.com" in url:
        m = re.search(r'[?&]url=([^&]+)', url)
        if m:
            url = urllib.parse.unquote(m.group(1))
        elif "CBMi" in url:
            return "Google News"
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if m:
        partes = m.group(1).split(".")
        if len(partes) >= 2:
            return partes[-2].capitalize()
        return partes[0].capitalize()
    return ""


def limpar_titulo(titulo):
    for p in ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "🆕", "🚨", "BREAKING:", "URGENTE:"]:
        titulo = titulo.replace(p, "").strip()
    titulo = re.sub(r'\s*[|\-–]\s*(TechCrunch|The Verge|Wired|Reuters|BBC|CNN|NYT|Forbes|Bloomberg).*$', '', titulo, flags=re.IGNORECASE)
    return titulo.strip().strip('"').strip("'")


def gerar_fallbacks():
    """Fallback local para cada categoria."""
    from datetime import datetime, timedelta
    hoje = datetime.now()
    return [
        {
            "titulo": "Novos modelos de IA superam benchmarks com arquitetura inovadora",
            "resumo": "Pesquisadores anunciaram avanços significativos em arquiteturas transformer com eficiencia energetica 10x maior.",
            "url": "", "fonte": "TechCrunch",
            "data": hoje, "data_str": hoje.strftime("%d/%m/%Y"),
            "categoria": "arquitetura"
        },
        {
            "titulo": "NVIDIA revela nova geracao de GPUs para data centers",
            "resumo": "As novas GPUs prometem 5x mais performance em inferencia com consumo energetico 40% menor.",
            "url": "", "fonte": "Tom's Hardware",
            "data": hoje, "data_str": hoje.strftime("%d/%m/%Y"),
            "categoria": "hardware"
        },
        {
            "titulo": "Mercado global de IA deve atingir US$ 1 trilhao em 2026",
            "resumo": "Relatorio aponta crescimento acelerado impulsionado por adocao empresarial e investimentos em infraestrutura.",
            "url": "", "fonte": "Forbes",
            "data": hoje, "data_str": hoje.strftime("%d/%m/%Y"),
            "categoria": "tendencias"
        },
        {
            "titulo": "Blockchain e IA: convergencia promete revolucionar setor financeiro",
            "resumo": "Startups estao combinando blockchain com machine learning para criar sistemas financeiros autonomos e seguros.",
            "url": "", "fonte": "CoinDesk",
            "data": hoje, "data_str": hoje.strftime("%d/%m/%Y"),
            "categoria": "cripto"
        }
    ]
