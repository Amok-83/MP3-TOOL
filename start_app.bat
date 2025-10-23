@echo off
title MP3 Album Tool
echo.
echo ================================================
echo           MP3 Album Tool - Windows
echo ================================================
echo.
echo Iniciando aplicacao...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.10+ de https://python.org
    echo.
    pause
    exit /b 1
)

REM Verificar se estamos no diretório correto
if not exist "web_app.py" (
    echo ERRO: web_app.py nao encontrado!
    echo Certifique-se de estar no diretorio correto.
    echo.
    pause
    exit /b 1
)

REM Verificar se o ambiente virtual existe
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
)

REM Ativar ambiente virtual e instalar dependências
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo           Aplicacao iniciada com sucesso!
echo ================================================
echo.
echo A aplicacao sera aberta no navegador automaticamente.
echo URL: http://localhost:5000
echo.
echo Para parar a aplicacao, pressione Ctrl+C
echo.

REM Iniciar aplicação
python start_app.py

echo.
echo Aplicacao encerrada.
pause
