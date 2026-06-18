"""
IG Auto Post — Orquestrador Principal
Modos:
  - auto: post simples (legenda + imagem)
  - ainnews: carrossel com capa + 4-5 noticias + encerramento
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


def modo_ainnews(config):
    """Carrossel AI NEWS: capa + noticias + encerramento."""
    from buscar_noticias import buscar_noticias
    from gerar_imagem import gerar_carrossel_noticias
    from postar import postar_carrossel

    print("[MODO AI NEWS] Carrossel do dia")

    print("Buscando noticias de IA por categoria...")
    noticias = buscar_noticias(config)
    total_noticias = len([n for n in noticias if n.get("tipo") == "noticia"])
    print(f"   {total_noticias} noticias em {len(noticias)} slides (capa + noticias + encerramento)")

    if total_noticias == 0:
        print("Nenhuma noticia encontrada.")
        return

    print("Gerando carrossel...")
    caminhos = gerar_carrossel_noticias(noticias, config)

    if len(caminhos) < 3:
        print(f"So {len(caminhos)} slides gerados.")
        return

    # Montar legenda principal
    legenda = f"📡 AI NEWS - {noticias[0].get('data_str', '')}\n\n"
    for n in noticias:
        if n.get("tipo") == "noticia":
            cat = n.get("categoria", "").upper()
            legenda += f"{n['emoji']} [{cat}] {n['titulo'][:80]}\n"
    legenda += "\n\n#IA #AI #Noticias #Tecnologia #MachineLearning #DeepLearning"

    print("Publicando carrossel no Instagram...")
    resultado = postar_carrossel(caminhos, legenda, config)
    if resultado:
        print("Carrossel AI NEWS publicado com sucesso!")
    else:
        print("Falha ao publicar carrossel.")


def modo_auto(config):
    """Post simples: gerar legenda + imagem + publicar."""
    from gerar_legenda import gerar_legenda
    from gerar_imagem import gerar_imagem_post
    from postar import postar_instagram

    print("[MODO AUTO] Post simples")

    print("Gerando legenda com IA...")
    legenda = gerar_legenda(config)
    print(f"   Legenda: {legenda[:60]}...")

    print("Gerando imagem...")
    caminho_imagem = gerar_imagem_post(legenda, config)
    print(f"   Imagem: {caminho_imagem}")

    print("Publicando no Instagram...")
    resultado = postar_instagram(caminho_imagem, legenda, config)
    if resultado:
        print("Post publicado com sucesso!")
    else:
        print("Falha ao publicar. Verifique as credenciais.")


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
