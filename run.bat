@echo off
cd /d "D:\projetos\ig-auto-post"
echo ========================================
echo    IG AUTO POST - Automacao Instagram
echo ========================================
echo.
echo 1 - Postar agora (python main.py)
echo 2 - Gerar imagem de teste (sem postar)
echo 3 - Ver ultimas imagens
echo 4 - Abrir pasta posts
echo 5 - Abrir terminal Git Bash
echo 0 - Sair
echo.
set /p opcao="Escolha: "

if "%opcao%"=="1" (
    python main.py
    pause
)
if "%opcao%"=="2" (
    python -c "from gerar_legenda import *; from gerar_imagem import *; import json; c=json.load(open('config.json')); i=gerar_imagem_post(gerar_legenda(c), c); print('Imagem:', i)"
    pause
)
if "%opcao%"=="3" (
    dir /o-d posts\*.jpg
    pause
)
if "%opcao%"=="4" (
    start posts
)
if "%opcao%"=="5" (
    start "" "C:\Program Files\Git\git-bash.exe" --cd="D:\projetos\ig-auto-post"
)
