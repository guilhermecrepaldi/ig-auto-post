# 🚀 MISSÃO: IG Auto Post — Automação de Posts no Instagram

## Contexto
Na sessão anterior (18/06/2026), construímos o sistema base em `D:\projetos\ig-auto-post`. 
Está funcional: gera legenda, cria imagem 1080x1080, publica via instagrapi.
Agora precisamos **evoluir** com o Neo Hermes: mais qualidade visual, autonomia, agendamento.

---

## 📦 O QUE JÁ EXISTE

### Repositório
```
https://github.com/guilhermecrepaldi/ig-auto-post
D:\projetos\ig-auto-post\
```

### Estrutura Atual
```
ig-auto-post/
├── main.py              # Orquestrador
├── gerar_legenda.py     # Legenda via DeepSeek API (fallback frases prontas)
├── gerar_imagem.py      # Imagem com Pillow (template gradiente azul escuro)
├── postar.py            # Postagem via instagrapi
├── config.example.json  # Template de configuração
├── cron.sh              # Script para agendamento
├── posts/               # Imagens geradas
├── logs/                # Logs do cron
└── README.md
```

### Dependências Instaladas
- ✅ Python 3.11+
- ✅ `instagrapi==2.16.5` (API privada Instagram)
- ✅ `Pillow==12.2.0` (geração de imagens)
- ✅ `requests==2.34.2` (API DeepSeek)
- ✅ Ollama rodando com `qwen3-vl:4b` (modelo vision disponível)
- ✅ DeepSeek V4 Flash configurado

### Testado e Funcionando
- ✅ Geração de legenda com IA
- ✅ Criação de imagem 1080x1080 com template profissional
- ✅ Fallback sem Internet (frases prontas)
- ✅ Imagem aprovada visualmente (gradiente, texto, hashtags, data)

---

## 🎯 O QUE EVOLUIR NESTA SESSÃO

### Prioridade Alta

#### 1. Postagem Real no Instagram
`postar.py` precisa de:
- [ ] `config.json` com usuário/senha reais do Instagram
- [ ] Login + sessão persistente (`session.json`)
- [ ] Testar `photo_upload()` em conta real
- [ ] Tratamento de desafio/2FA do Instagram

#### 2. Templates Visuais Profissionais
`gerar_imagem.py` atualmente faz:
- Gradiente simples (#0a0a1a → #1a1a3a)
- Texto centralizado branco
- Hashtags no rodapé

**Evoluir para**:
- [ ] Múltiplos templates (dica, projeto, reflexão, citação)
- [ ] Background com gradiente + padrão geométrico
- [ ] Avatar/ícone no canto superior
- [ ] Box de destaque para o texto principal
- [ ] Barra de progresso decorativa
- [ ] Fontes Google (Inter, Poppins) em vez de Arial
- [ ] Paletas de cores por template (dark/cyan, purple/neon, green/tech)

#### 3. Ollama para Geração de Imagem (FULL LOCAL)
O Ollama tem `qwen3-vl:4b` (vision) mas **não gera imagens** — só descreve.
Para gerar imagem local: precisamos de **ComfyUI + Stable Diffusion** ou **FLUX**.

**Checklist:**
- [ ] Verificar se ComfyUI está instalado
- [ ] Se não: instalar ComfyUI + SDXL ou FLUX
- [ ] Workflow: gerar background profissional baseado no tema do post
- [ ] Sobrepor texto (Pillow) na imagem gerada

#### 4. Variedade de Conteúdo
- [ ] Múltiplos modos: dica técnica, projeto, reflexão, case
- [ ] Rodízio automático entre modos
- [ ] Template visual diferente para cada modo

### Prioridade Média

#### 5. Agendamento com Hermes Cron
```bash
hermes cron create "0 9 * * *" \
  --name "ig-auto-post-diario" \
  --script "cron.sh" \
  --workdir "D:\\projetos\\ig-auto-post"
```
E também:
- [ ] `hermes cron create "0 12 * * *"` (post almoço)
- [ ] `hermes cron create "0 18 * * *"` (post noite)
- [ ] Verificar: `hermes cron list`

#### 6. Analytics e Histórico
- [ ] Log de posts publicados (data, legenda, template)
- [ ] Métricas: likes, comentários (via instagrapi)
- [ ] Dashboard simples

### Prioridade Baixa

#### 7. Modo Headless / Sem Postar
Para testar sem publicar:
```bash
python main.py --dry-run
```
Já é possível rodando `gerar_legenda.py` + `gerar_imagem.py` isoladamente.

#### 8. Múltiplas Contas
- [ ] Suporte a troca de conta Instagram
- [ ] Perfil por conta (config separado)

---

## 🔧 CONFIGURAÇÃO NECESSÁRIA

### config.json (copiar de config.example.json)
```json
{
  "instagram": {
    "username": "SEU_USUARIO",
    "password": "SUA_SENHA"
  },
  "deepseek": {
    "api_key": "SUA_KEY_OPENROUTER",
    "model": "deepseek/deepseek-v4-flash"
  },
  "post": {
    "intervalo_horas": 24,
    "modo": "auto",
    "hashtags_padrao": ["dev", "python", "automation", "ai", "coding"]
  },
  "templates": [
    {"nome": "dica", "descricao": "Dica rápida de programação"},
    {"nome": "projeto", "descricao": "Mostrar projeto em andamento"},
    {"nome": "reflexao", "descricao": "Reflexão sobre tecnologia"}
  ],
  "pasta_saida": "posts"
}
```

---

## 📋 COMANDOS ÚTEIS

```bash
# Navegar até o projeto
cd /d/projetos/ig-auto-post

# Verificar dependências
pip list | grep -E "instagrapi|Pillow|requests"

# Testar geração sem postar
python -c "from gerar_legenda import *; from gerar_imagem import *; import json; c=json.load(open('config.json')); i=gerar_imagem_post(gerar_legenda(c), c); print('IMAGEM:', i)"

# Ver última imagem gerada
ls -lt posts/ | head -3

# Ver imagem
start posts/$(ls -t posts/ | head -1)

# Verificar Ollama
curl http://localhost:11434/api/tags

# Ver cron jobs do Hermes
hermes cron list

# Adicionar cron job
hermes cron create "0 9 * * *" --name ig-diario --script cron.sh --workdir "D:\\projetos\\ig-auto-post"
```

---

## 📂 CAMINHOS IMPORTANTES

| Item | Caminho |
|------|---------|
| Projeto | `D:\projetos\ig-auto-post\` |
| GitHub | `https://github.com/guilhermecrepaldi/ig-auto-post` |
| Imagens geradas | `D:\projetos\ig-auto-post\posts\` |
| Logs | `D:\projetos\ig-auto-post\logs\` |
| Config | `D:\projetos\ig-auto-post\config.json` |
| Sessão Instagram | `D:\projetos\ig-auto-post\session.json` |
| Templates | `D:\projetos\ig-auto-post\templates\` |
| Ollama | `http://localhost:11434` |
| Modelo vision | `qwen3-vl:4b` (já baixado) |

---

## ⚡ FLUXO DE TRABALHO SUGERIDO

```
1. Carregar skills:
   skill_view(name='auto-executor')     # Loop Plan→Execute→Verify
   skill_view(name='auto-healing')      # Fallbacks automáticos
   skill_view(name='output-coeso')      # Template de resposta
   skill_view(name='roteador-economico') # DeepSeek sempre

2. Configurar Instagram:
   - Editar config.json com dados reais
   - Rodar: python main.py (testa login + post)

3. Evoluir templates visuais:
   - Editar gerar_imagem.py
   - Testar: python -c "...gerar_imagem_post..."

4. Instalar ComfyUI (se for gerar imagem local):
   - Verificar se já existe
   - Instalar workflow SDXL/FLUX

5. Agendar:
   - hermes cron create ...
   - Verificar: hermes cron list
```

---

> **Neo Hermes**: esta sessão focou em construir a base funcional. 
> A PRÓXIMA sessão pode focar em: templates visuais profissionais, 
> postagem real, ComfyUI, e agendamento diário.
