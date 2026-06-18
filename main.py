"""
IG Auto Post — Orquestrador Principal
Gera legenda, imagem e publica no Instagram automaticamente.
"""
import json
import os
from pathlib import Path

PASTA = Path(__file__).parent

def carregar_config():
    cfg_path = PASTA / "config.json"
    if not cfg_path.exists():
        print("❌ config.json não encontrado. Copie config.example.json e edite.")
        exit(1)
    with open(cfg_path) as f:
        return json.load(f)

def main():
    config = carregar_config()
    print("🚀 IG Auto Post — Iniciando...")
    
    from gerar_legenda import gerar_legenda
    from gerar_imagem import gerar_imagem_post
    from postar import postar_instagram
    
    # 1. Gerar legenda
    print("📝 Gerando legenda com IA...")
    legenda = gerar_legenda(config)
    print(f"   ✅ Legenda: {legenda[:60]}...")
    
    # 2. Gerar imagem
    print("🎨 Gerando imagem do post...")
    caminho_imagem = gerar_imagem_post(legenda, config)
    print(f"   ✅ Imagem: {caminho_imagem}")
    
    # 3. Postar no Instagram
    print("📤 Publicando no Instagram...")
    resultado = postar_instagram(caminho_imagem, legenda, config)
    
    if resultado:
        print("✅ Post publicado com sucesso!")
    else:
        print("❌ Falha ao publicar. Verifique as credenciais.")

if __name__ == "__main__":
    main()
