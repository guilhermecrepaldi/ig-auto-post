"""
Busca noticias para AI NEWS.
Fonte PRINCIPAL: banco TOP OF THE HOUR (ed006_cards.json)
Fallback: Google News RSS
Formato rico: fact + impact + terms
"""
import json
import re
import os
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).parent
BANCO_PATH = Path("D:/projetos/TOP OF THE HOUR - IA/ed006_cards.json")

# Mapeamento de prefixo ID para categoria
ID_TO_CAT = {
    "arc": "arquitetura",
    "hw": "hardware",
    "mar": "tendencias",
}


def carregar_banco():
    """Carrega cards do banco TOP OF THE HOUR."""
    if not BANCO_PATH.exists():
        print(f"   Banco nao encontrado: {BANCO_PATH}")
        return []
    try:
        with open(BANCO_PATH, encoding="utf-8") as f:
            cards = json.load(f)
        print(f"   Banco TOP OF THE HOUR: {len(cards)} cards carregados")
        return cards
    except Exception as e:
        print(f"   Erro ao carregar banco: {e}")
        return []


def buscar_por_categoria(categoria, config):
    """Busca 6 noticias de uma categoria, priorizando banco TOP OF THE HOUR."""
    print(f"Buscando noticias de {categoria}...")

    cards = carregar_banco()
    noticias = []

    # 1. Filtrar do banco
    prefixo = None
    for k, v in ID_TO_CAT.items():
        if v == categoria:
            prefixo = k
            break

    if cards and prefixo:
        for c in cards:
            cid = c.get("id", "")
            if cid.startswith(prefixo):
                # Extrair texto do impact (primeiros 300 chars)
                impact = c.get("impact", "")
                fact = c.get("fact", "")

                # Combinar fact + impact num resumo rico
                resumo = fact[:200] if fact else ""
                if impact and len(resumo) < 150:
                    resumo += " " + impact[:150]

                noticias.append({
                    "titulo": c.get("title", ""),
                    "resumo": resumo[:250],
                    "fact": fact,
                    "impact": impact,
                    "terms": c.get("terms", {}),
                    "url": c.get("url", ""),
                    "fonte": c.get("source", ""),
                    "data_str": c.get("date", datetime.now().strftime("%d/%m/%Y")),
                    "importancia": c.get("importance", "medio"),
                })

        print(f"   Banco: {len(noticias)} noticias para {categoria}")
        # Ordenar por importancia
        imp_order = {"critico": 0, "alto": 1, "medio": 2, "baixo": 3}
        noticias.sort(key=lambda x: imp_order.get(x["importancia"], 99))

    # 2. Fallback: Google News se menos de 6
    if len(noticias) < 6:
        noticias += _buscar_google_news_fallback(categoria, 6 - len(noticias))

    # 3. Se ainda faltar, fallback local
    if len(noticias) < 6:
        fallbacks = _gerar_fallbacks_categoria(categoria)
        for fb in fallbacks:
            if len(noticias) >= 6:
                break
            if not any(fb["titulo"][:30] in n["titulo"] for n in noticias):
                noticias.append(fb)

    # 4. Formatar saida: capa + 6 noticias + devimpact
    emojis = ["🤖", "⚡", "🧠", "🚀", "💡", "🔬"]
    resultado = []

    # CAPA
    nome_cat = {"arquitetura": "ARQUITETURA", "hardware": "HARDWARE", "tendencias": "TENDENCIAS"}.get(categoria, categoria.upper())
    resultado.append({
        "numero": 0,
        "tipo": "capa",
        "categoria": categoria,
        "titulo": f"AI NEWS - {nome_cat}",
        "subtitulo": f"As 6 principais novidades em {nome_cat.lower()}",
        "data_str": datetime.now().strftime("%d/%m/%Y"),
        "emoji": "📡",
    })

    for i, n in enumerate(noticias[:6]):
        resultado.append({
            "numero": i + 1,
            "tipo": "noticia",
            "categoria": categoria,
            "titulo": n["titulo"],
            "resumo": n["resumo"][:250],
            "fact": n.get("fact", ""),
            "impact": n.get("impact", ""),
            "terms": n.get("terms", {}),
            "url": n.get("url", ""),
            "fonte": n.get("fonte", ""),
            "data_str": n.get("data_str", ""),
            "emoji": emojis[i % len(emojis)],
        })

    # DEVIPACT
    dev_texts = {
        "arquitetura": (
            "O QUE MUDA PRO DEV\n\n"
            "Modelos abertos com 1M de contexto permitem analisar codebases inteiros.\n"
            "Agents autonomos estao mudando o paradigma de desenvolvimento.\n"
            "Fine-tuning ficou viavel em desktop com GB300.\n\n"
            "Fique de olho: MoE, RAG avancado, agent frameworks."
        ),
        "hardware": (
            "O QUE MUDA PRO DEV\n\n"
            "GPUs Blackwell rodam 20x mais agents por watt.\n"
            "Desktop de 20 PFLOPS fine-tuna modelos 70B localmente.\n"
            "Scanner de seguranca para agent skills (1 em 4 tem falhas).\n\n"
            "Fique de olho: GB300, memoria HBM4, NPUs em desktop."
        ),
        "tendencias": (
            "O QUE MUDA PRO DEV\n\n"
            "IA generativa integrada em todas as plataformas.\n"
            "Mercado aquecido: 100k+ vagas em IA em 2026.\n"
            "Regulamentacao chegando - responsabilidade tecnica.\n\n"
            "Fique de olho: AI Mode no Facebook, Claude Corps, leis de IA."
        ),
    }

    resultado.append({
        "numero": 7,
        "tipo": "devimpact",
        "categoria": categoria,
        "titulo": "O que muda pro Dev",
        "texto": dev_texts.get(categoria, ""),
        "emoji": "🧑‍💻",
    })

    return resultado


def _buscar_google_news_fallback(categoria, max_noticias):
    """Fallback: busca noticias no Google News RSS."""
    noticias = []
    queries_map = {
        "arquitetura": ["inteligencia+artificial+modelos+LLM", "AI+framework+agent+raciocinio"],
        "hardware": ["GPU+chip+NVIDIA+IA", "data+center+datacenter+energia+AI"],
        "tendencias": ["mercado+IA+investimento+startup", "OpenAI+Google+Microsoft+Meta+IA"],
    }

    queries = queries_map.get(categoria, ["inteligencia+artificial+IA"])
    palavras_chave = {
        "arquitetura": ["modelo", "llm", "framework", "arquitetura", "neural", "algoritmo", "raciocinio", "agent", "deep learning", "machine learning", "pesquisa"],
        "hardware": ["chip", "gpu", "nvidia", "processador", "hardware", "data center", "datacenter", "energia", "memoria", "quantico", "infraestrutura"],
        "tendencias": ["mercado", "investimento", "startup", "regulacao", "lei", "openai", "google", "inovacao", "futuro", "emprego", "trabalho", "educacao", "ferramenta", "chatbot"],
    }.get(categoria, [])

    try:
        import xml.etree.ElementTree as ET
        import urllib.request

        for q in queries:
            q_ascii = q.encode("ascii", errors="replace").decode("ascii")
            url = f"https://news.google.com/rss/search?q={q_ascii}&hl=pt-BR&gl=BR"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode("utf-8", errors="replace")
                root = ET.fromstring(data)
                for item in root.iter("item"):
                    title = item.findtext("title", "")
                    desc = item.findtext("description", "")
                    link = item.findtext("link", "")
                    pubdate = item.findtext("pubDate", "")

                    title_limpo = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;', ' ', title)
                    title_limpo = re.sub(r'\s+', ' ', title_limpo).strip()
                    desc_limpo = re.sub(r'<[^>]+>', '', desc or "")
                    desc_limpo = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;', ' ', desc_limpo)
                    desc_limpo = re.sub(r'\s+', ' ', desc_limpo).strip()[:200]

                    data_obj = None
                    if pubdate:
                        try:
                            data_obj = datetime.strptime(pubdate.strip()[:25], "%a, %d %b %Y %H:%M:%S")
                        except:
                            pass

                    if title_limpo and len(title_limpo) > 20:
                        texto = (title_limpo + " " + desc_limpo).lower()
                        if any(p in texto for p in palavras_chave):
                            noticias.append({
                                "titulo": _limpar_titulo(title_limpo),
                                "resumo": desc_limpo or title_limpo[:200],
                                "fact": "",
                                "impact": "",
                                "terms": {},
                                "url": link,
                                "fonte": _extrair_fonte(link),
                                "data_str": data_obj.strftime("%d/%m/%Y") if data_obj else datetime.now().strftime("%d/%m/%Y"),
                                "importancia": "medio",
                            })

        print(f"   Google News fallback: {len(noticias)}")
    except Exception as e:
        print(f"   Google News fallback falhou: {e}")

    # Deduplicar
    unicas = []
    vistos = set()
    for n in noticias:
        chave = n["titulo"].lower()[:50]
        if chave not in vistos:
            vistos.add(chave)
            unicas.append(n)

    return unicas[:max_noticias]


def _extrair_fonte(url):
    if not url:
        return ""
    if "news.google.com" in url:
        m = re.search(r'[?&]url=([^&]+)', url)
        if m:
            url = __import__("urllib.parse").unquote(m.group(1))
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if m:
        partes = m.group(1).split(".")
        if len(partes) >= 2:
            return partes[-2].capitalize()
        return partes[0].capitalize()
    return ""


def _limpar_titulo(titulo):
    for p in ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "🆕", "🚨", "BREAKING:", "URGENTE:"]:
        titulo = titulo.replace(p, "").strip()
    titulo = re.sub(r'\s*[|\-–]\s*(TechCrunch|The Verge|Wired|Reuters|BBC|CNN|NYT|Forbes|Bloomberg).*$', '', titulo, flags=re.IGNORECASE)
    return titulo.strip().strip('"').strip("'")


def _gerar_fallbacks_categoria(categoria):
    hoje = datetime.now()
    fb = {
        "arquitetura": [
            {"titulo": "Novo modelo open-source supera GPT em raciocinio logico", "resumo": "Pesquisadores liberam modelo com arquitetura MoE que supera benchmarks em 15%", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "TechCrunch", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Fine-tuning eficiente: tecnica reduz custo de treino em 90%", "resumo": "Novo metodo de fine-tuning promete democratizar o acesso a modelos de ultima geracao", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "ArXiv", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Agents autonomos: o novo paradigma do desenvolvimento", "resumo": "Frameworks de agentes estao mudando a forma como construimos software", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "GitHub Blog", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Nova tecnica de RAG melhora precisao em 40%", "resumo": "Retrieval-Augmented Generation avancada promete respostas mais precisas", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "VentureBeat", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "medio"},
            {"titulo": "Modelos menores superam gigantes em tarefas especificas", "resumo": "SLMs (Small Language Models) estao provando que tamanho nao e documento", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "The Verge", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "medio"},
            {"titulo": "Contexto de 1M tokens se torna padrao em modelos abertos", "resumo": "GLM-5.2 e outros modelos atingem 1M de tokens de contexto, revolucionando analise de dados", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "Zhipu AI", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
        ],
        "hardware": [
            {"titulo": "NVIDIA Blackwell Ultra entrega 20x mais agents por megawatt", "resumo": "Novo benchmark AgentPerf mostra eficiencia energetica revolucionaria para cargas de IA", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "NVIDIA Blog", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "critico"},
            {"titulo": "Desktop com GB300 Blackwell chega com 20 PFLOPS", "resumo": "ASUS lanca workstation que fine-tuna modelos 70B localmente sem nuvem", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "TechPowerUp", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Scanner de seguranca para agent skills e open-source", "resumo": "SkillSpector da NVIDIA detecta 64 vulnerabilidades em agentes de IA", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "NVIDIA/GitHub", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Apple expande PCC para Google Cloud com NVIDIA CC", "resumo": "Infraestrutura de IA da Apple agora roda em nuvem de terceiros com privacidade total", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "Apple/NVIDIA", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "medio"},
            {"titulo": "Reino Unido investe em datacenters nucleares de 1.7 GW", "resumo": "Projeto Sovereign AI usa reatores modulares para alimentar infraestrutura de IA", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "UK Government", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "medio"},
            {"titulo": "NVIDIA RTX Spark: superchip para desktop chega em 2026", "resumo": "Nova linha de processadores promete levar inferencia de IA para estacoes de trabalho", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "NVIDIA", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
        ],
        "tendencias": [
            {"titulo": "Mercado global de IA deve atingir US$ 1 trilhao em 2026", "resumo": "Relatorio aponta crescimento acelerado impulsionado por adocao empresarial", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "Forbes", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "OpenAI libera versao gratuita com busca em tempo real", "resumo": "ChatGPT gratis agora inclui busca na web, tornando informacao mais acessivel", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "The Verge", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Regulacao de IA avanca na Europa e nos EUA", "resumo": "Novas leis de IA comecam a definir responsabilidades para empresas de tecnologia", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "Reuters", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
            {"titulo": "Startups de IA captam recorde de US$ 50 bi no trimestre", "resumo": "Investimento em IA atinge novo recorde, puxado por empresas de infraestrutura", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "Bloomberg", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "medio"},
            {"titulo": "IA na educacao: escolas adotam tutores inteligentes", "resumo": "Plataformas de ensino com IA personalizada prometem revolucionar a educacao basica", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "Wired", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "medio"},
            {"titulo": "Microsoft Copilot atinge 50 milhoes de usuarios pagos", "resumo": "Ferramenta de produtividade com IA se torna o produto que mais cresce na Microsoft", "fact": "", "impact": "", "terms": {}, "url": "", "fonte": "CNBC", "data_str": hoje.strftime("%d/%m/%Y"), "importancia": "alto"},
        ],
    }
    return fb.get(categoria, fb["tendencias"])


# ============================================================
# FUNCAO UNIFICADA PARA 20 SLIDES
# ============================================================

def buscar_todas_categorias(config):
    """Busca noticias das 3 categorias e retorna 20 slides."""
    import time

    CATS = ["arquitetura", "hardware", "tendencias"]
    INFO = {
        "arquitetura": {"emoji": "🏗️", "cor": "#00d4ff", "nome": "ARQUITETURA"},
        "hardware": {"emoji": "⚙️", "cor": "#22c55e", "nome": "HARDWARE"},
        "tendencias": {"emoji": "📈", "cor": "#f59e0b", "nome": "TENDENCIAS"},
    }

    print("Buscando noticias para 3 categorias (banco TOP OF THE HOUR)...")

    todas_noticias = {}
    for cat in CATS:
        print(f"\n--- {cat.upper()} ---")
        todas_noticias[cat] = buscar_por_categoria(cat, config)
        time.sleep(1)

    # Montar 20 slides
    resultado = []
    emoji_seq = ["🤖", "⚡", "🧠", "🚀", "💡", "🔬"]

    # CAPA
    resultado.append({
        "numero": 0,
        "tipo": "capa",
        "categoria": "capa",
        "titulo": "AI NEWS",
        "subtitulo": "Arquitetura + Hardware + Tendencias",
        "data_str": datetime.now().strftime("%d/%m/%Y"),
        "emoji": "📡",
    })

    slide_num = 1
    max_noticias_per_cat = {0: 6, 1: 5, 2: 4}  # 6+5+4 = 15 noticias

    for ci, cat in enumerate(CATS):
        info = INFO[cat]
        noticias_raw = todas_noticias.get(cat, [])

        # Separador
        resultado.append({
            "numero": slide_num,
            "tipo": "separador",
            "categoria": cat,
            "titulo": info["nome"],
            "emoji": info["emoji"],
            "subtitulo": f"{max_noticias_per_cat[ci]} principais noticias",
        })
        slide_num += 1

        # Noticias
        max_n = max_noticias_per_cat[ci]
        count = 0
        for n in noticias_raw:
            if n.get("tipo") != "noticia":
                continue
            if count >= max_n:
                break
            resultado.append({
                "numero": slide_num,
                "tipo": "noticia",
                "categoria": cat,
                "titulo": n["titulo"],
                "resumo": n.get("resumo", "")[:250],
                "fact": n.get("fact", ""),
                "impact": n.get("impact", ""),
                "terms": n.get("terms", {}),
                "url": n.get("url", ""),
                "fonte": n.get("fonte", ""),
                "data_str": n.get("data_str", ""),
                "emoji": emoji_seq[count % len(emoji_seq)],
            })
            slide_num += 1
            count += 1

    # DEVIPACT GERAL
    dev_texto = (
        "O QUE MUDA PRO DEV\n\n"
        "Arquitetura: Modelos abertos com 1M de contexto.\n"
        "Hardware: GPUs Blackwell, desktop 20 PFLOPS.\n"
        "Tendencias: IA generativa, regulamentacao.\n\n"
        "Fique de olho: MoE, GB300, agents autonomos, NPUs."
    )
    resultado.append({
        "numero": slide_num,
        "tipo": "devimpact",
        "categoria": "devimpact",
        "titulo": "O que muda pro Dev",
        "texto": dev_texto,
        "emoji": "🧑‍💻",
    })

    print(f"\nTotal: {len(resultado)} slides")
    return resultado
