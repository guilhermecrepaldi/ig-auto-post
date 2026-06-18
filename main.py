"""
IG Auto Post — Orquestrador Principal
1 post diario com 20 slides: capa + 18 noticias + devimpact
"""
import json
import sys
from pathlib import Path

PASTA = Path(__file__).parent


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
    print("IG AUTO POST — AI NEWS DIARIO (20 SLIDES)")
    print("=" * 50)

    from buscar_noticias import buscar_todas_categorias
    from gerar_imagem import gerar_carrossel_noticias
    from postar import postar_carrossel

    print("\nBuscando noticias das 3 categorias...")
    noticias = buscar_todas_categorias(config)

    if len(noticias) < 3:
        print("Poucos slides, abortando.")
        return

    print(f"\nGerando {len(noticias)} slides...")
    caminhos = gerar_carrossel_noticias(noticias, config)

    if len(caminhos) < 3:
        print("Falha ao gerar imagens.")
        return

    # Legenda
    legenda = "📡 AI NEWS - Resumo do Dia\n"
    legenda += f"📅 {noticias[0].get('data_str', '')}\n\n"
    legenda += "🏗️ Arquitetura | ⚙️ Hardware | 📈 Tendencias\n"
    legenda += "\nAs 18 principais noticias de IA em 1 post!\n"
    legenda += "\n\n#IA #AI #Noticias #Tecnologia #MachineLearning #DeepLearning"

    print("Publicando carrossel de 20 slides...")
    resultado = postar_carrossel(caminhos, legenda, config)
    if resultado:
        print("AI NEWS DIARIO publicado com sucesso! (20 slides)")
    else:
        print("Falha ao publicar.")


if __name__ == "__main__":
    main()
