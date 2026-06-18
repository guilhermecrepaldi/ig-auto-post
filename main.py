"""
IG Auto Post — Orquestrador Principal
Modos:
  - auto: post simples
  - ainnews: posta UMA categoria (arquitetura, hardware, tendencias)
  Recebe CATEGORIA via argumento ou config
"""
import json
import sys
from pathlib import Path

PASTA = Path(__file__).parent
CATEGORIAS = ["arquitetura", "hardware", "tendencias"]


def carregar_config():
    cfg_path = PASTA / "config.json"
    if not cfg_path.exists():
        print("config.json nao encontrado.")
        sys.exit(1)
    with open(cfg_path) as f:
        return json.load(f)


def postar_categoria(categoria, config):
    """Gera e publica carrossel de 8 slides para UMA categoria."""
    from buscar_noticias import buscar_por_categoria
    from gerar_imagem import gerar_carrossel_noticias
    from postar import postar_carrossel

    print(f"[AI NEWS] Postando categoria: {categoria.upper()}")

    noticias = buscar_por_categoria(categoria, config)
    total_slides = len(noticias)
    print(f"   {total_slides} slides gerados")

    if total_slides < 3:
        print("Poucos slides, abortando.")
        return False

    print("Gerando imagens do carrossel...")
    caminhos = gerar_carrossel_noticias(noticias, config)

    if len(caminhos) < 3:
        print("Falha ao gerar imagens.")
        return False

    # Montar legenda
    nome_cat = {"arquitetura": "Arquitetura", "hardware": "Hardware", "tendencias": "Tendencias"}.get(categoria, categoria)
    legenda = f"🏗️ AI NEWS - {nome_cat}\n"
    legenda += f"📅 {noticias[0].get('data_str', '')}\n\n"
    for n in noticias:
        if n.get("tipo") == "noticia":
            legenda += f"{n['emoji']} {n['titulo'][:80]}\n"
    legenda += "\n\n#IA #AI #Noticias #Tecnologia #MachineLearning #DeepLearning"

    print("Publicando no Instagram...")
    resultado = postar_carrossel(caminhos, legenda, config)
    if resultado:
        print(f"AI NEWS [{categoria}] publicado com sucesso!")
    else:
        print(f"Falha ao publicar [{categoria}].")

    return resultado


def main():
    config = carregar_config()
    modo = config.get("post", {}).get("modo", "auto")

    # Verificar se veio categoria como argumento
    if len(sys.argv) > 1:
        categoria = sys.argv[1].lower()
        if categoria in CATEGORIAS:
            print(f"IG Auto Post — Modo: ainnews [{categoria}]")
            return postar_categoria(categoria, config)
        else:
            print(f"Categoria invalida: {categoria}. Opcoes: {', '.join(CATEGORIAS)}")
            sys.exit(1)

    # Modo padrao
    if modo == "ainnews":
        # Posta todas as 3 categorias em sequencia
        print("IG Auto Post — Modo: ainnews (3 posts)")
        for cat in CATEGORIAS:
            postar_categoria(cat, config)
            import time
            time.sleep(30)  # espera entre posts
    else:
        # Modo auto: post simples
        from gerar_legenda import gerar_legenda
        from gerar_imagem import gerar_imagem_post
        from postar import postar_instagram

        print("[MODO AUTO] Post simples")
        legenda = gerar_legenda(config)
        caminho_imagem = gerar_imagem_post(legenda, config)
        resultado = postar_instagram(caminho_imagem, legenda, config)
        if resultado:
            print("Post publicado com sucesso!")
        else:
            print("Falha ao publicar.")


if __name__ == "__main__":
    main()
