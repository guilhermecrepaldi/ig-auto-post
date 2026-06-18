"""
IG Auto Post — Orquestrador Principal
Fluxo unico: busca noticias 1x → gera 3 carrosseis → publica tudo
"""
import json
import sys
import time
from pathlib import Path

PASTA = Path(__file__).parent
CATEGORIAS = ["arquitetura", "hardware", "tendencias"]

INFO_CAT = {
    "arquitetura": {"nome": "Arquitetura", "emoji": "🏗️", "cor": "#00d4ff"},
    "hardware": {"nome": "Hardware", "emoji": "⚙️", "cor": "#22c55e"},
    "tendencias": {"nome": "Tendencias", "emoji": "📈", "cor": "#f59e0b"},
}


def carregar_config():
    cfg_path = PASTA / "config.json"
    if not cfg_path.exists():
        print("config.json nao encontrado.")
        sys.exit(1)
    with open(cfg_path) as f:
        return json.load(f)


def main():
    config = carregar_config()
    print("=" * 50)
    print("IG AUTO POST — AI NEWS DIARIO")
    print("=" * 50)

    from buscar_noticias import buscar_por_categoria
    from gerar_imagem import gerar_carrossel_noticias
    from postar import postar_carrossel

    # Cache das noticias (busca 1x)
    cache_noticias = {}

    print(f"\nBuscando noticias para {len(CATEGORIAS)} categorias...")
    for cat in CATEGORIAS:
        print(f"\n--- {cat.upper()} ---")
        cache_noticias[cat] = buscar_por_categoria(cat, config)
        time.sleep(2)  # pausa entre buscas pra nao sobrecarregar

    print("\n" + "=" * 50)
    print("GERANDO E PUBLICANDO 3 CARROSSEIS")
    print("=" * 50)

    for cat in CATEGORIAS:
        noticias = cache_noticias[cat]
        info = INFO_CAT[cat]

        print(f"\n>>> {info['emoji']} {info['nome']}")

        if len(noticias) < 3:
            print(f"   Poucos slides ({len(noticias)}), pulando.")
            continue

        print(f"   Gerando {len(noticias)} slides...")
        caminhos = gerar_carrossel_noticias(noticias, config)

        if len(caminhos) < 3:
            print("   Falha ao gerar imagens.")
            continue

        # Montar legenda
        legenda = f"{info['emoji']} AI NEWS - {info['nome']}\n"
        legenda += f"📅 {noticias[0].get('data_str', '')}\n\n"
        for n in noticias:
            if n.get("tipo") == "noticia":
                legenda += f"{n['emoji']} {n['titulo'][:80]}\n"
        legenda += "\n\n#IA #AI #Noticias #Tecnologia #MachineLearning #DeepLearning"

        print(f"   Publicando...")
        resultado = postar_carrossel(caminhos, legenda, config)
        if resultado:
            print(f"   ✅ {info['nome']} publicado!")
        else:
            print(f"   ❌ Falha ao publicar {info['nome']}.")

        # Espera entre posts (evita rate limit)
        if cat != CATEGORIAS[-1]:
            print("   Aguardando 30s...")
            time.sleep(30)

    print("\n" + "=" * 50)
    print("✅ RODADA DO DIA CONCLUIDA")
    print("=" * 50)


if __name__ == "__main__":
    main()
