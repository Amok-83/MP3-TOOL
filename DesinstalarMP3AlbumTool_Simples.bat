@echo off
REM MP3 Album Tool - Desinstalador Simples (Batch)
REM ==============================================
REM Este script remove o MP3 Album Tool usando apenas comandos batch

title MP3 Album Tool - Desinstalador Simples

echo.
echo =============================================
echo   MP3 Album Tool - Desinstalador Simples
echo =============================================
echo.

REM Verificar se está a correr como administrador
net session >nul 2>&1
if errorlevel 1 (
    echo ERRO: Este desinstalador precisa de ser executado como Administrador!
    echo.
    echo Para executar como administrador:
    echo 1. Clique com o botao direito neste ficheiro
    echo 2. Selecione "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo ATENCAO: Esta operacao ira remover o MP3 Album Tool do sistema!
echo.
echo Sera removido:
echo   - Pasta de instalacao: %ProgramFiles%\MP3AlbumTool
echo   - Atalho no Desktop
echo   - Entrada no Menu Iniciar
echo.
set /p confirm="Tem a certeza que deseja continuar? (S/N): "
if /i not "%confirm%"=="S" (
    echo Desinstalacao cancelada pelo utilizador.
    pause
    exit /b 0
)

echo.
echo Iniciando desinstalacao...
echo.

REM Terminar processos da aplicação
echo Terminando processos da aplicacao...
taskkill /f /im "MP3AlbumTool.exe" >nul 2>&1
if errorlevel 1 (
    echo   Nenhum processo em execucao
) else (
    echo   Processos terminados
)

REM Aguardar um pouco
timeout /t 2 /nobreak >nul

REM Remover atalho do Desktop
echo Removendo atalho do Desktop...
if exist "%USERPROFILE%\Desktop\MP3 Album Tool.lnk" (
    del /f /q "%USERPROFILE%\Desktop\MP3 Album Tool.lnk" >nul 2>&1
    echo   Atalho do Desktop removido
) else (
    echo   Atalho do Desktop nao encontrado
)

REM Remover atalho do Desktop público
if exist "%PUBLIC%\Desktop\MP3 Album Tool.lnk" (
    del /f /q "%PUBLIC%\Desktop\MP3 Album Tool.lnk" >nul 2>&1
    echo   Atalho publico do Desktop removido
)

REM Remover entrada do Menu Iniciar
echo Removendo entrada do Menu Iniciar...
if exist "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk" (
    del /f /q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk" >nul 2>&1
    echo   Entrada do Menu Iniciar removida
) else (
    echo   Entrada do Menu Iniciar nao encontrada
)

REM Remover pasta do Menu Iniciar se existir
if exist "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3AlbumTool" (
    rmdir /s /q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3AlbumTool" >nul 2>&1
    echo   Pasta do Menu Iniciar removida
)

REM Remover entrada do registo (básico)
echo Removendo entradas do registo...
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\MP3 Album Tool" /f >nul 2>&1
if errorlevel 1 (
    echo   Nenhuma entrada do registo encontrada
) else (
    echo   Entrada do registo removida
)

REM Remover pasta de instalação
echo Removendo pasta de instalacao...
if exist "%ProgramFiles%\MP3AlbumTool" (
    echo   Removendo: %ProgramFiles%\MP3AlbumTool
    
    REM Remover atributos de só leitura
    attrib -r "%ProgramFiles%\MP3AlbumTool\*.*" /s >nul 2>&1
    
    REM Remover pasta
    rmdir /s /q "%ProgramFiles%\MP3AlbumTool" >nul 2>&1
    if errorlevel 1 (
        echo   AVISO: Nao foi possivel remover completamente a pasta de instalacao
        echo   Pode ser necessario remover manualmente: %ProgramFiles%\MP3AlbumTool
    ) else (
        echo   Pasta de instalacao removida com sucesso
    )
) else (
    echo   Pasta de instalacao nao encontrada
)

REM Remover pasta de instalação alternativa (se existir)
if exist "%ProgramFiles(x86)%\MP3AlbumTool" (
    echo   Removendo pasta alternativa: %ProgramFiles(x86)%\MP3AlbumTool
    attrib -r "%ProgramFiles(x86)%\MP3AlbumTool\*.*" /s >nul 2>&1
    rmdir /s /q "%ProgramFiles(x86)%\MP3AlbumTool" >nul 2>&1
)

REM Limpar ficheiros temporários
echo Limpando ficheiros temporarios...
if exist "%TEMP%\MP3AlbumTool*" (
    del /f /q "%TEMP%\MP3AlbumTool*" >nul 2>&1
    echo   Ficheiros temporarios limpos
)

echo.
echo =============================================
echo   DESINSTALACAO CONCLUIDA
echo =============================================
echo.
echo O MP3 Album Tool foi removido do sistema.
echo.
echo NOTA: Se algum ficheiro nao foi removido, pode ser necessario
echo       reiniciar o computador e tentar novamente.
echo.
pause