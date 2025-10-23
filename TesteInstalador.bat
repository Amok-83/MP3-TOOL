@echo off
title Teste dos Instaladores MP3 Album Tool
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🧪 TESTE DOS INSTALADORES                ║
echo ║                      MP3 Album Tool                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando ficheiros criados...
echo.

REM Verificar se os instaladores foram criados
if exist "MP3AlbumTool_GitHub_Installer.ps1" (
    echo ✅ MP3AlbumTool_GitHub_Installer.ps1 - CRIADO
) else (
    echo ❌ MP3AlbumTool_GitHub_Installer.ps1 - NÃO ENCONTRADO
)

if exist "InstalarMP3AlbumTool.bat" (
    echo ✅ InstalarMP3AlbumTool.bat - CRIADO
) else (
    echo ❌ InstalarMP3AlbumTool.bat - NÃO ENCONTRADO
)

if exist "INSTRUCOES_GITHUB.md" (
    echo ✅ INSTRUCOES_GITHUB.md - CRIADO
) else (
    echo ❌ INSTRUCOES_GITHUB.md - NÃO ENCONTRADO
)

if exist "MP3AlbumTool_Distribuicao_Final" (
    echo ✅ MP3AlbumTool_Distribuicao_Final - PASTA CRIADA
    
    echo.
    echo 📁 Conteúdo da pasta de distribuição:
    dir "MP3AlbumTool_Distribuicao_Final" /B
) else (
    echo ❌ MP3AlbumTool_Distribuicao_Final - PASTA NÃO ENCONTRADA
)

echo.
echo 🔧 Verificando sintaxe dos instaladores...
echo.

REM Verificar sintaxe do PowerShell (sem executar)
powershell -Command "& {try { $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content 'MP3AlbumTool_GitHub_Installer.ps1' -Raw), [ref]$null); Write-Host '✅ PowerShell Installer - SINTAXE OK' -ForegroundColor Green } catch { Write-Host '❌ PowerShell Installer - ERRO DE SINTAXE' -ForegroundColor Red; Write-Host $_.Exception.Message -ForegroundColor Yellow }}"

echo.
echo 📋 Resumo dos ficheiros para distribuição:
echo.
echo 📦 PARA GITHUB:
echo    └── MP3AlbumTool_Distribuicao_Final\ (pasta completa)
echo.
echo 🚀 PARA DISTRIBUIR AOS UTILIZADORES:
echo    ├── MP3AlbumTool_GitHub_Installer.ps1 (recomendado)
echo    ├── InstalarMP3AlbumTool.bat (alternativa simples)
echo    └── INSTRUCOES_GITHUB.md (instruções)
echo.

echo 💡 PRÓXIMOS PASSOS:
echo    1. Criar repositório no GitHub
echo    2. Fazer upload da pasta MP3AlbumTool_Distribuicao_Final
echo    3. Editar URLs nos instaladores (substituir SEU_USUARIO)
echo    4. Testar instaladores com repositório real
echo    5. Distribuir apenas o ficheiro instalador
echo.

echo ✨ VANTAGENS:
echo    • Só distribui 1 ficheiro pequeno (instalador)
echo    • Descarrega sempre a versão mais recente
echo    • Instalação profissional automática
echo    • Fácil manutenção (só atualizar no GitHub)
echo.

pause