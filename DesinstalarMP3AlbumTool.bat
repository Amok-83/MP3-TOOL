@echo off
REM MP3 Album Tool - Desinstalador Batch
REM ====================================
REM Este script executa o desinstalador PowerShell

title MP3 Album Tool - Desinstalador

echo.
echo ========================================
echo   MP3 Album Tool - Desinstalador
echo ========================================
echo.

REM Verificar se o script PowerShell existe
if not exist "%~dp0MP3AlbumTool_Uninstaller.ps1" (
    echo ERRO: Script de desinstalacao nao encontrado!
    echo Certifique-se de que o ficheiro MP3AlbumTool_Uninstaller.ps1 esta na mesma pasta.
    echo.
    pause
    exit /b 1
)

echo Preparando para executar o desinstalador...
echo.
echo ATENCAO: Este processo ira remover completamente o MP3 Album Tool do sistema!
echo.
pause

REM Tentar executar como administrador
echo Executando desinstalador...
echo.

REM Verificar se PowerShell está disponível
powershell -Command "Get-Host" >nul 2>&1
if errorlevel 1 (
    echo ERRO: PowerShell nao esta disponivel neste sistema!
    echo O desinstalador requer PowerShell para funcionar.
    echo.
    pause
    exit /b 1
)

REM Executar o script PowerShell como administrador
powershell -Command "Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0MP3AlbumTool_Uninstaller.ps1\"' -Verb RunAs"

if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel executar o desinstalador!
    echo Certifique-se de que tem privilegios de administrador.
    echo.
    echo Pode tentar executar manualmente:
    echo 1. Clique com o botao direito em MP3AlbumTool_Uninstaller.ps1
    echo 2. Selecione "Executar com PowerShell"
    echo 3. Aceite a execucao como administrador
    echo.
    pause
    exit /b 1
)

echo.
echo Desinstalador executado. Verifique a janela do PowerShell para o progresso.
echo.
pause