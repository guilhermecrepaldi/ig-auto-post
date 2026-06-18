# IG Auto Post — Sistema Automatizado de Postagem no Instagram

Sistema completo para **criar e publicar posts no Instagram** usando IA local (Ollama) para gerar legendas e imagens.

## Stack

| Componente | Tecnologia | Custo |
|-----------|-----------|-------|
| **Postagem** | `instagrapi` (API privada Instagram) | ✅ Grátis |
| **Imagem** | Ollama + llava (local) | ✅ Grátis |
| **Legenda** | DeepSeek API | ~$0.0001/post |
| **Agendamento** | Hermes cron job | ✅ Grátis |
| **Template** | Pillow (Python) | ✅ Grátis |

## Estrutura

```
ig-auto-post/
├── main.py           # Orquestrador principal
├── postar.py         # Postagem no Instagram (instagrapi)
├── gerar_legenda.py  # Geração de legenda com IA
├── gerar_imagem.py   # Geração/edição de imagem
├── templates/        # Templates de imagem base
├── posts/            # Posts gerados (imagem + legenda)
├── config.json       # Config (credenciais, agendamento)
└── cron.sh           # Script para cron job
```

## Como Usar

```bash
# 1. Instalar dependências
pip install instagrapi Pillow requests

# 2. Configurar credenciais
cp config.example.json config.json
# Editar config.json com usuário/senha do Instagram

# 3. Postar manualmente
python main.py

# 4. Agendar (cron job)
# Adicionar no Hermes:
# hermes cron create "0 9 * * *" --script ig-auto-post/cron.sh
```

## Aviso Legal

Este sistema usa a API privada do Instagram. Use com responsabilidade:
- Respeite os limites de taxa do Instagram
- Não automatize interações (likes, comments, follows)
- Use apenas para postagem de conteúdo próprio
