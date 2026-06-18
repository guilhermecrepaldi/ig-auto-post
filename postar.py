"""
Postagem no Instagram usando instagrapi.
Suporta foto única e carrossel (album).
"""
import json
from pathlib import Path


def _login_instagram(config):
    """Faz login no Instagram com sessão persistente."""
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired

    ig_config = config["instagram"]
    cl = Client()

    session_file = Path(__file__).parent / "session.json"
    if session_file.exists():
        with open(session_file) as f:
            session_data = json.load(f)
        cl.set_settings(session_data)
        try:
            cl.get_timeline_feed()
            print("   Sessao carregada do cache")
            return cl
        except LoginRequired:
            print("   Sessao expirada, refazendo login...")

    cl.login(ig_config["username"], ig_config["password"])
    with open(session_file, "w") as f:
        json.dump(cl.get_settings(), f)
    print("   Login realizado, sessao salva")
    return cl


def postar_instagram(caminho_imagem, legenda, config):
    """Publica imagem unica no Instagram."""
    try:
        cl = _login_instagram(config)
        result = cl.photo_upload(str(caminho_imagem), legenda)
        print(f"   Post ID: {result.id}")
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        return False


def postar_carrossel(caminhos_imagens, legenda, config):
    """Publica carrossel (album) de ate 20 imagens no Instagram."""
    try:
        cl = _login_instagram(config)
        from pathlib import Path
        medias = [Path(str(p)) for p in caminhos_imagens]
        result = cl.album_upload(medias, caption=legenda)
        print(f"   Carrossel Post ID: {result.id}")
        return True
    except Exception as e:
        print(f"   Erro carrossel: {e}")
        return False
