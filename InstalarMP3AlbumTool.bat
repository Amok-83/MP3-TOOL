@echo off
chcp 65001 >nul
title MP3 Album Tool - GitHub Installer

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎵 MP3 ALBUM TOOL                        ║
echo ║                   Automatic Installer                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ This script must be run as Administrator!
    echo 💡 Right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Configuration
set "INSTALL_PATH=C:\Program Files\MP3AlbumTool"
set "GITHUB_REPO=Amok-83/MP3-TOOL"
set "DOWNLOAD_URL=https://github.com/%GITHUB_REPO%/archive/refs/heads/main.zip"
set "TEMP_DIR=%TEMP%\MP3AlbumTool_Install"
set "ZIP_FILE=%TEMP_DIR%\mp3albumtool.zip"
set "EXTRACT_DIR=%TEMP_DIR%\extracted"

echo 🚀 Starting MP3 Album Tool installation...
echo 📍 Installation path: %INSTALL_PATH%
echo 📦 GitHub repository: %GITHUB_REPO%
echo.

REM Create temporary directory
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM Download from GitHub
echo 📥 Downloading from GitHub...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%ZIP_FILE%' -UseBasicParsing}"

if not exist "%ZIP_FILE%" (
    echo ❌ Download failed! Check internet connection and repository URL.
    echo.
    pause
    exit /b 1
)

echo ✅ Download completed!

REM Extract files
echo 📦 Extracting files...
powershell -Command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%ZIP_FILE%', '%EXTRACT_DIR%')}"

if not exist "%EXTRACT_DIR%" (
    echo ❌ Extraction failed!
    echo.
    pause
    exit /b 1
)

echo ✅ Extraction completed!

REM Install application
echo 📁 Installing application...

REM Create installation directory
if not exist "%INSTALL_PATH%" mkdir "%INSTALL_PATH%"

REM Find extracted folder (usually has -main suffix)
for /d %%i in ("%EXTRACT_DIR%\*") do (
    if exist "%%i\MP3AlbumTool_Distribuicao_Final" (
        xcopy "%%i\MP3AlbumTool_Distribuicao_Final\*" "%INSTALL_PATH%\" /E /Y /Q
        goto :install_done
    )
)

REM If distribution folder not found, copy everything
xcopy "%EXTRACT_DIR%\*" "%INSTALL_PATH%\" /E /Y /Q

:install_done
echo ✅ Application installed!

REM Create desktop shortcut
echo 🔗 Creating shortcuts...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\MP3 Album Tool.lnk'); $Shortcut.TargetPath = '%INSTALL_PATH%\MP3AlbumTool.exe'; $Shortcut.WorkingDirectory = '%INSTALL_PATH%'; $Shortcut.Description = 'MP3 Album Tool'; $Shortcut.Save()}"

REM Create Start Menu shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('StartMenu') + '\Programs\MP3 Album Tool.lnk'); $Shortcut.TargetPath = '%INSTALL_PATH%\MP3AlbumTool.exe'; $Shortcut.WorkingDirectory = '%INSTALL_PATH%'; $Shortcut.Description = 'MP3 Album Tool'; $Shortcut.Save()}"

echo ✅ Shortcuts created!

REM Cleanup temporary files
echo 🧹 Cleaning up temporary files...
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

REM Success message
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                ✅ INSTALLATION COMPLETED!                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📍 Application installed at: %INSTALL_PATH%
echo 🔗 Shortcuts created on Desktop and Start Menu
echo.

REM Ask to launch application
set /p launch="Would you like to launch MP3 Album Tool now? (Y/N): "
if /i "%launch%"=="Y" (
    if exist "%INSTALL_PATH%\MP3AlbumTool.exe" (
        start "" "%INSTALL_PATH%\MP3AlbumTool.exe"
        echo 🚀 MP3 Album Tool launched!
    ) else (
        echo ❌ Executable not found at: %INSTALL_PATH%\MP3AlbumTool.exe
    )
)

echo.
echo 🎶 Thank you for using MP3 Album Tool!
pause