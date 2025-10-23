@echo off
title MP3 Album Tool - Instalador
echo.
echo 🎵 MP3 Album Tool - Instalador
echo =================================
echo.
echo Este instalador irá instalar o MP3 Album Tool no seu sistema.
echo.
echo IMPORTANTE: Este ficheiro deve ser executado como Administrador!
echo.
pause
echo.
echo Iniciando instalação...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0MP3AlbumTool_Installer_Final.ps1"

echo.
echo Instalação concluída!
echo.
pause
