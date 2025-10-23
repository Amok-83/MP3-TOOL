@echo off
title Upload MP3 Album Tool para GitHub

echo.
echo ========================================
echo    UPLOAD PARA GITHUB
echo    MP3 Album Tool - Amok-83/MP3-TOOL
echo ========================================
echo.

echo Preparando upload para: https://github.com/Amok-83/MP3-TOOL.git
echo.

REM Verificar se Git esta instalado
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERRO: Git nao esta instalado!
    echo Instala o Git em: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git encontrado!
echo.

REM Inicializar repositorio Git se nao existir
if not exist ".git" (
    echo Inicializando repositorio Git...
    git init
    echo.
)

REM Configurar remote origin
echo Configurando repositorio remoto...
git remote remove origin 2>nul
git remote add origin https://github.com/Amok-83/MP3-TOOL.git
echo.

REM Criar .gitignore se nao existir
if not exist ".gitignore" (
    echo Criando .gitignore...
    echo __pycache__/ > .gitignore
    echo *.pyc >> .gitignore
    echo build/ >> .gitignore
    echo dist/ >> .gitignore
    echo .vscode/ >> .gitignore
    echo .idea/ >> .gitignore
    echo *.tmp >> .gitignore
    echo.
)

echo Adicionando ficheiros ao repositorio...
git add .
echo.

echo Fazendo commit inicial...
git commit -m "Initial commit: MP3 Album Tool with GitHub installers"
echo.

echo Enviando para GitHub...
echo NOTA: Pode ser necessario autenticar no GitHub
echo.
git branch -M main
git push -u origin main

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo        UPLOAD CONCLUIDO!
    echo ========================================
    echo.
    echo Projeto enviado com sucesso para GitHub!
    echo Repositorio: https://github.com/Amok-83/MP3-TOOL
    echo.
    echo PROXIMOS PASSOS:
    echo 1. Verifica o repositorio no GitHub
    echo 2. Testa os instaladores automaticos
    echo 3. Partilha os instaladores com os utilizadores
    echo.
    echo FICHEIROS PARA DISTRIBUICAO:
    echo - MP3AlbumTool_GitHub_Installer.ps1 (PowerShell)
    echo - InstalarMP3AlbumTool.bat (Batch)
    echo.
) else (
    echo.
    echo ERRO durante o upload!
    echo Verifica:
    echo - Conexao a internet
    echo - Autenticacao no GitHub
    echo - Permissoes do repositorio
    echo.
)

echo.
pause