# 📸 IG Auto Post

**Instagram auto-posting with local AI — Ollama generates captions, DeepSeek creates images, and publishes automatically on schedule.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Ollama](https://img.shields.io/badge/AI-Ollama%20%7C%20DeepSeek-green)
![Instagram](https://img.shields.io/badge/Instagrapi-API%20Privada-E4405F)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Cron](https://img.shields.io/badge/Cron-ready-brightgreen)

> **Custo por post: ~$0.0001** (apenas API DeepSeek para legenda — imagem e template são 100% locais).

---

## 🎯 Como Funciona

```
┌─────────────┐    ┌────────────┐    ┌────────────┐    ┌──────────────┐
│  DeepSeek   │ →  │   Ollama   │ →  │   Pillow   │ →  │  Instagrapi  │
│  Gera       │    │  Gera      │    │  Monta     │    │  Publica no  │
│  Legenda    │    │  Descrição │    │  Template  │    │  Instagram   │
└─────────────┘    └────────────┘    └────────────┘    └──────────────┘
      ↓                  ↓                  ↓                  ↓
   $0.0001            Grátis             Grátis             Grátis
```

---

## ✨ Features

- ✅ **Geração automática de legendas** com IA (DeepSeek)
- ✅ **Geração de imagens** com Ollama (llava) ou **templates prontos** (Pillow)
- ✅ **Publicação automática** via instagrapi (API privada do Instagram)
- ✅ **Agendamento cron** — posta no horário que você definir
- ✅ **Custo quase zero** — ~$0.0001/post
- ✅ **Modo manual** e **modo automático**

---

## 🔧 Stack

| Componente | Tecnologia | Custo |
|-----------|-----------|-------|
| Postagem | `instagrapi` | ✅ Grátis |
| Imagem | Ollama + llava (local) | ✅ Grátis |
| Legenda | DeepSeek API | ~$0.0001/post |
| Template | Pillow (Python) | ✅ Grátis |
| Agendamento | Hermes cron job | ✅ Grátis |

---

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install instagrapi Pillow requests

# 2. Configurar credenciais
cp config.example.json config.json
# Editar config.json com usuário/senha do Instagram

# 3. Postar manualmente
python main.py

# 4. Agendar (cron)
# Adicionar no Hermes:
# hermes cron create "0 9 * * *" --script ig-auto-post/cron.sh
```

---

## 📁 Estrutura

```
ig-auto-post/
├── main.py             # Orquestrador principal
├── postar.py           # Postagem no Instagram (instagrapi)
├── gerar_legenda.py    # Geração de legenda com IA
├── gerar_imagem.py     # Geração/edição de imagem
├── templates/          # Templates de imagem base
├── posts/              # Posts gerados (imagem + legenda)
├── config.json         # Config (credenciais, agendamento)
└── cron.sh             # Script para cron job
```

---

## ⚙️ Configuração

```json
{
  "instagram_user": "seu_usuario",
  "instagram_pass": "sua_senha",
  "post_interval_hours": 24,
  "use_ollama": true,
  "language": "pt-BR",
  "topics": ["tecnologia", "programação", "IA", "automação"]
}
```

---

## 📊 Exemplo de Post Gerado

```
🧠 Automação com IA: do zero ao post em 3 segundos
  
Hoje o DeepSeek gerou esta legenda, o Ollama pensou no conteúdo
e o Pillow montou o template. Tudo local, tudo automático.
  
O futuro do conteúdo é: configure uma vez, publique para sempre.
  
#automacao #ia #python #instagram #dev
```

---

## ⚠️ Aviso Legal

Este sistema usa a API privada do Instagram. Use com responsabilidade:
- ✅ Postagem de conteúdo próprio apenas
- ❌ Não automatize interações (likes, comments, follows)
- ✅ Respeite os limites de taxa do Instagram
- ✅ Use conta pessoal ou de negócios com autorização

---

## 🤝 Contribuindo

Issues e PRs são bem-vindos!

---

## 📫 Contato

**Guilherme Crepaldi** — [silvagui8@gmail.com](mailto:silvagui8@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/guilherme-crepaldi-778b3b237) · [Portfolio](https://crepaldi.online)

---

> *Automation that creates. AI that delivers. Zero bullshit.*
