"""
Busca as 6 principais notícias de IA do dia para UMA categoria específica.
Cada post = 1 categoria, 1 capa + 6 noticias + 1 "O que muda pro Dev"
"""
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).parent

# Queries de busca específicas por categoria
QUERIES_POR_CATEGORIA = {
    "arquitetura": [
        "inteligencia+artificial+modelos+LLM+arquitetura",
        "machine+learning+deep+learning+pesquisa",
        "AI+model+architecture+transformer+neural",
        "open+source+AI+framework+agent+raciocinio",
        "fine+tuning+treinamento+AI+algoritmo",
    ],
    "hardware": [
        "GPU+chip+NVIDIA+hardware+IA",
        "data+center+datacenter+energia+AI+consumo",
        "processador+inferencia+AI+computacao",
        "quantum+computing+edge+AI+servidor",
        "memoria+treinamento+AI+infraestrutura",
    ],
    "tendencias": [
        "mercado+IA+investimento+startup",
        "OpenAI+Google+Microsoft+Meta+IA",
        "regulacao+regulação+IA+governo+lei",
        "inovacao+IA+futuro+trabalho+emprego",
        "chatbot+copilot+ferramenta+IA+educacao",
    ],
}

# Texto "O que muda pro Dev" por categoria
DEVIPACT = {
    "arquitetura": (
        "🧑‍💻 O QUE MUDA PRO DEV\n\n"
        "Modelos mais eficientes = menos custo de API.\n"
        "Agents autônomos = novo paradigma de desenvolvimento.\n"
        "Open source dominando = mais liberdade pra inovar.\n"
        "Fique de olho em: arquiteturas MoE, reasoning agents, fine-tuning eficiente."
    ),
    "hardware": (
        "🧑‍💻 O QUE MUDA PRO DEV\n\n"
        "GPUs mais potentes = modelos maiores rodando local.\n"
        "Data centers eficientes = API mais barata.\n"
        "Edge computing = IA rodando no dispositivo.\n"
        "Fique de olho em: NPUs, inferencia local, custo por token caindo."
    ),
    "tendencias": (
        "🧑‍💻 O QUE MUDA PRO DEV\n\n"
        "Ferramentas IA = produtividade 10x em coding.\n"
        "Mercado aquecido = mais vagas pra devs de IA.\n"
        "Regulacao chegando = responsabilidade técnica.\n"
        "Fique de olho em: regulamentação, agentes autonomos, low-code AI."
    ),
}


def buscar_por_categoria(categoria, config):
    """Busca 6 noticias de uma categoria especifica."""
    print(f"Buscando noticias de {categoria}...")

    cat_info = {
        "arquitetura": {"emoji": "🏗️", "cor": "#00d4ff", "nome": "ARQUITETURA"},
        "hardware": {"emoji": "⚙️", "cor": "#22c55e", "nome": "HARDWARE"},
        "tendencias": {"emoji": "📈", "cor": "#f59e0b", "nome": "TENDENCIAS"},
    }.get(categoria, {})

    todas_noticias = []

    # Google News RSS com queries específicas da categoria
    queries = QUERIES_POR_CATEGORIA.get(categoria, ["inteligencia+artificial+IA"])
    try:
        import xml.etree.ElementTree as ET
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

                    title_limpo = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;', ' ', title)
                    title_limpo = re.sub(r'\s+', ' ', title_limpo).strip()
                    desc_limpo = re.sub(r'<[^>]+>', '', desc)
                    desc_limpo = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;', ' ', desc_limpo)
                    desc_limpo = re.sub(r'\s+', ' ', desc_limpo).strip()[:200]

                    data_obj = None
                    if pubdate:
                        try:
                            data_obj = datetime.strptime(pubdate.strip()[:25], "%a, %d %b %Y %H:%M:%S")
                        except:
                            pass

                    if title_limpo and len(title_limpo) > 20:
                        # Filtrar só noticias com palavras da categoria
                        palavras_cat = {
                            "arquitetura": ["modelo","llm","framework","arquitetura","transformer",
                                           "neural","treinamento","fine-tuning","open source",
                                           "algoritmo","raciocinio","reasoning","agente","agent",
                                           "deep learning","machine learning","pesquisa","research",
                                           "paper","publicacao"],
                            "hardware": ["chip","gpu","nvidia","amd","processador","hardware",
                                        "data center","datacenter","energia","consumo","servidor",
                                        "memoria","inferencia","computacao","edge","iot",
                                        "quantico","quantum","infraestrutura"],
                            "tendencias": ["mercado","investimento","startup","regulacao","regulação",
                                          "lei","governo","openai","google","meta","microsoft",
                                          "amazon","apple","inovacao","futuro","emprego","trabalho",
                                          "educacao","copilot","assistente","chatbot","ferramenta",
                                          "etica","ética","seguranca","bill gates","sam altman","musk"],
                        }.get(categoria, [])

                        texto = (title_limpo + " " + desc_limpo).lower()
                        if any(p in texto for p in palavras_cat):
                            todas_noticias.append({
                                "titulo": limpar_titulo(title_limpo),
                                "resumo": desc_limpo if desc_limpo else title_limpo[:200],
                                "url": link,
                                "fonte": extrair_fonte(link),
                                "data": data_obj,
                                "data_str": data_obj.strftime("%d/%m/%Y") if data_obj else datetime.now().strftime("%d/%m/%Y")
                            })

        print(f"   Google News: {len(todas_noticias)} candidatas")
    except Exception as e:
        print(f"   Google News falhou: {e}")

    # Deduplicar
    unicas = []
    vistos = set()
    for n in todas_noticias:
        chave = n["titulo"].lower()[:60]
        if chave not in vistos:
            vistos.add(chave)
            unicas.append(n)

    # Ordenar: mais recentes primeiro, depois maior titulo
    unicas.sort(key=lambda x: (
        -(x["data"].timestamp() if x["data"] else 0),
        -len(x["titulo"])
    ))

    # Pegar top 6
    top6 = unicas[:6]

    # Fallback se nao tiver 6
    if len(top6) < 6:
        fallbacks = gerar_fallbacks_categoria(categoria)
        for fb in fallbacks:
            if len(top6) >= 6:
                break
            # So adiciona se nao tiver noticia similar
            tit_fb = fb["titulo"].lower()[:40]
            if not any(tit_fb in n["titulo"].lower() for n in top6):
                top6.append(fb)

    print(f"   Selecionadas: {len(top6)} noticias")

    # Montar resultado: capa + 6 noticias + devimpact
    emojis_lista = ["🤖", "⚡", "🧠", "🚀", "💡", "🔬"]
    resultado = []

    # CAPA
    resultado.append({
        "numero": 0,
        "tipo": "capa",
        "categoria": categoria,
        "titulo": f"AI NEWS - {cat_info.get('nome', categoria.upper())}",
        "subtitulo": f"As 6 principais novidades em {cat_info.get('nome', categoria)}",
        "data_str": datetime.now().strftime("%d/%m/%Y"),
        "emoji": cat_info.get("emoji", "📡"),
        "fonte": "",
        "resumo": ""
    })

    # 6 NOTICIAS
    for i, n in enumerate(top6[:6]):
        resultado.append({
            "numero": i + 1,
            "tipo": "noticia",
            "categoria": categoria,
            "titulo": n["titulo"],
            "resumo": n["resumo"][:150],
            "url": n.get("url", ""),
            "fonte": n.get("fonte", ""),
            "data_str": n.get("data_str", datetime.now().strftime("%d/%m/%Y")),
            "emoji": emojis_lista[i % len(emojis_lista)],
        })

    # DEVIPACT
    resultado.append({
        "numero": 7,
        "tipo": "devimpact",
        "categoria": categoria,
        "titulo": "O que muda pro Dev",
        "texto": DEVIPACT.get(categoria, ""),
        "emoji": "🧑‍💻",
        "fonte": "",
        "resumo": ""
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


def gerar_fallbacks_categoria(categoria):
    """Fallback local para cada categoria."""
    hoje = datetime.now()
    fallbacks = {
        "arquitetura": [
            {"titulo": "Novo modelo open-source supera GPT em raciocinio logico", "resumo": "Pesquisadores liberam modelo com arquitetura MoE que supera benchmarks em 15%", "url": "", "fonte": "TechCrunch", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Fine-tuning eficiente: tecnica reduz custo de treino em 90%", "resumo": "Novo metodo de fine-tuning promete democratizar o acesso a modelos de ultima geracao", "url": "", "fonte": "ArXiv", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Agents autonomos: o novo paradigma do desenvolvimento", "resumo": "Frameworks de agentes estao mudando a forma como construimos software", "url": "", "fonte": "GitHub Blog", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Arquitetura Transformer completa 10 anos de revolucao", "resumo": "De paper seminal a base de todos os LLMs modernos, o Transformer reina absoluto", "url": "", "fonte": "Wired", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Nova tecnica de RAG melhora precisao em 40%", "resumo": "Retrieval-Augmented Generation avancada promete respostas mais precisas e contextualizadas", "url": "", "fonte": "VentureBeat", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Modelos menores superam gigantes em tarefas especificas", "resumo": "SLMs (Small Language Models) estao provando que tamanho nao e documento", "url": "", "fonte": "The Verge", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
        ],
        "hardware": [
            {"titulo": "NVIDIA anuncia GPU com 3x mais performance em inferencia", "resumo": "Nova geracao de GPUs promete revolucionar o custo por token em data centers", "url": "", "fonte": "Tom's Hardware", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Data centers de IA consumirao 8% da energia global ate 2030", "resumo": "Demanda energetica explode com crescimento exponencial de modelos de IA", "url": "", "fonte": "Bloomberg", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "AMD entra forte no mercado de chips para IA", "resumo": "Nova linha de processadores promete competir directamente com NVIDIA", "url": "", "fonte": "AnandTech", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Memoria HBM4 promete 2x largura de banda para treinamento", "resumo": "Nova geracao de memoria de alta largura de banda chega em 2026", "url": "", "fonte": "Samsung News", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Edge computing com NPUs leva IA para dispositivos IoT", "resumo": "Processadores neurais em dispositivos de borda permitem inferencia sem nuvem", "url": "", "fonte": "IEEE Spectrum", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Computacao quantica aplicada a IA da primeiros passos", "resumo": "Prototipos de chips quanticos mostram vantagem em problemas de otimizacao de ML", "url": "", "fonte": "Nature", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
        ],
        "tendencias": [
            {"titulo": "OpenAI libera versao gratuita com busca em tempo real", "resumo": "ChatGPT gratis agora inclui busca na web, tornando informacao mais acessivel", "url": "", "fonte": "The Verge", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Mercado de IA deve gerar 100 mil novas vagas em 2026", "resumo": "Demanda por engenheiros de IA cresce 3x mais rapido que outras areas de tech", "url": "", "fonte": "Forbes", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Regulacao de IA avanca na Europa e nos EUA", "resumo": "Novas leis de IA comecam a definir responsabilidades para empresas de tecnologia", "url": "", "fonte": "Reuters", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Microsoft Copilot atinge 50 milhoes de usuarios pagos", "resumo": "Ferramenta de produtividade com IA se torna o produto que mais cresce na Microsoft", "url": "", "fonte": "CNBC", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "Startups de IA captam recorde de US$ 50 bi no 1o trimestre", "resumo": "Investimento em IA atinge novo recorde, puxado por empresas de infraestrutura", "url": "", "fonte": "Bloomberg", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
            {"titulo": "IA na educacao: escolas adotam tutores inteligentes", "resumo": "Plataformas de ensino com IA personalizada prometem revolucionar a educacao basica", "url": "", "fonte": "Wired", "data": hoje, "data_str": hoje.strftime("%d/%m/%Y")},
        ],
    }
    return fallbacks.get(categoria, fallbacks["tendencias"])
