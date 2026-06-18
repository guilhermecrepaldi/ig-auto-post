"""
IG Auto Post — Orquestrador Principal
Modos:
  - auto: post simples (legenda + imagem)
  - ainnews: carrossel de 4 noticias
"""
import json
import sys
from pathlib import Path

PASTA = Path(__file__).parent


def carregar_config():
    cfg_path = PASTA / "config.json"
    if not cfg_path.exists():
        print("config.json nao encontrado. Copie config.example.json e edite.")
        sys.exit(1)
    with open(cfg_path) as f:
        return json.load(f)


def modo_auto(config):
    """Post simples: gerar legenda + imagem + publicar."""
    from gerar_legenda import gerar_legenda
    from gerar_imagem import gerar_imagem_post
    from postar import postar_instagram

    print("[MODO AUTO] Post simples")

    print("Gerando legenda com IA...")
    legenda = gerar_legenda(config)
    print(f"   Legenda: {legenda[:60]}...")

    print("Gerando imagem do post...")
    caminho_imagem = gerar_imagem_post(legenda, config)
    print(f"   Imagem: {caminho_imagem}")

    print("Publicando no Instagram...")
    resultado = postar_instagram(caminho_imagem, legenda, config)
    if resultado:
        print("Post publicado com sucesso!")
    else:
        print("Falha ao publicar. Verifique as credenciais.")


def modo_ainnews(config):
    """Carrossel AI NEWS: buscar noticias + gerar 4 slides + publicar."""
    from buscar_noticias import buscar_noticias
    from gerar_imagem import gerar_carrossel_noticias
    from postar import postar_carrossel

    print("[MODO AI NEWS] Carrossel de noticias do dia")

    print("Buscando noticias de IA...")
    noticias = buscar_noticias(config)
    print(f"   {len(noticias)} noticias selecionadas")

    if not noticias:
        print("Nenhuma noticia encontrada. Usando modo auto como fallback.")
        return modo_auto(config)

    print("Gerando carrossel de 4 slides...")
    caminhos = gerar_carrossel_noticias(noticias, config)

    if len(caminhos) < 4:
        print(f"So {len(caminhos)} imagens geradas, necessario 4.")
        return

    print("Publicando carrossel no Instagram...")
    legenda_principal = f"{noticias[0]['emoji']} AI NEWS - As 4 principais noticias de IA do dia!\n\n"
    for n in noticias:
        legenda_principal += f"{n['numero']}. {n['titulo'][:80]}\n"
    legenda_principal += "\n\n#IA #AI #Noticias #Tecnologia #MachineLearning #DeepLearning #Inovacao"

    resultado = postar_carrossel(caminhos, legenda_principal, config)
    if resultado:
        print("Carrossel publicado com sucesso!")
    else:
        print("Falha ao publicar carrossel.")


def main():
    config = carregar_config()
    modo = config.get("post", {}).get("modo", "auto")

    print("IG Auto Post — Iniciando...")
    print(f"Modo: {modo}")

    if modo == "ainnews":
        modo_ainnews(config)
    else:
        modo_auto(config)


if __name__ == "__main__":
    main()
