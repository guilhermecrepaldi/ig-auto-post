"""
Postagem no Instagram usando instagrapi.
"""
import os
import json
from pathlib import Path

def postar_instagram(caminho_imagem, legenda, config):
    """Publica imagem no Instagram."""
    try:
        from instagrapi import Client
        from instagrapi.exceptions import LoginRequired, ClientError
        
        ig_config = config["instagram"]
        cl = Client()
        
        # Login com session reuse
        session_file = Path(__file__).parent / "session.json"
        if session_file.exists():
            with open(session_file) as f:
                session_data = json.load(f)
            cl.set_settings(session_data)
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                cl.login(ig_config["username"], ig_config["password"])
                with open(session_file, "w") as f:
                    json.dump(cl.get_settings(), f)
        else:
            cl.login(ig_config["username"], ig_config["password"])
            with open(session_file, "w") as f:
                json.dump(cl.get_settings(), f)
        
        # Upload da foto
        result = cl.photo_upload(str(caminho_imagem), legenda)
        print(f"   ✅ Post ID: {result.id}")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
