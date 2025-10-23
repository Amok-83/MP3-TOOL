@echo off
title MP3 Album Tool - Uninstaller
color 0B

echo.
echo ========================================
echo    MP3 Album Tool - Uninstaller
echo ========================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
) else (
    echo [ERROR] This uninstaller must be run as Administrator!
    echo Right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo Removing MP3 Album Tool...
echo.

:: Remove from Program Files (GitHub installer location)
if exist "%LOCALAPPDATA%\MP3AlbumTool" (
    echo [INFO] Removing from %LOCALAPPDATA%\MP3AlbumTool
    rmdir /s /q "%LOCALAPPDATA%\MP3AlbumTool"
    if %errorLevel% == 0 (
        echo [OK] Local installation removed
    ) else (
        echo [WARNING] Could not remove local installation
    )
)

:: Remove from Program Files (if installed there)
if exist "%ProgramFiles%\MP3AlbumTool" (
    echo [INFO] Removing from %ProgramFiles%\MP3AlbumTool
    rmdir /s /q "%ProgramFiles%\MP3AlbumTool"
    if %errorLevel% == 0 (
        echo [OK] Program Files installation removed
    ) else (
        echo [WARNING] Could not remove Program Files installation
    )
)

:: Remove Desktop shortcut
if exist "%USERPROFILE%\Desktop\MP3 Album Tool.lnk" (
    echo [INFO] Removing Desktop shortcut
    del "%USERPROFILE%\Desktop\MP3 Album Tool.lnk"
    if %errorLevel% == 0 (
        echo [OK] Desktop shortcut removed
    )
)

:: Remove Start Menu shortcut
if exist "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk" (
    echo [INFO] Removing Start Menu shortcut
    del "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk"
    if %errorLevel% == 0 (
        echo [OK] Start Menu shortcut removed
    )
)

:: Remove from PATH (if added)
echo [INFO] Checking PATH environment variable...
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "currentPath=%%b"
if defined currentPath (
    echo %currentPath% | findstr /i "MP3AlbumTool" >nul
    if %errorLevel% == 0 (
        echo [INFO] Removing from system PATH...
        setx PATH "%currentPath:;%LOCALAPPDATA%\MP3AlbumTool=%" /M >nul 2>&1
        setx PATH "%currentPath:;%ProgramFiles%\MP3AlbumTool=%" /M >nul 2>&1
        echo [OK] Removed from system PATH
    )
)

echo.
echo ========================================
echo    Uninstallation completed!
echo ========================================
echo.
echo MP3 Album Tool has been removed from your system.
echo You may need to restart your computer for PATH changes to take effect.
echo.
pause