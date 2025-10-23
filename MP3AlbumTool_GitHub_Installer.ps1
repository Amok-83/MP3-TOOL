# MP3 Album Tool - GitHub Installer
# Version: 1.0
# Description: Automatic installer that downloads and installs MP3 Album Tool from GitHub

param(
    [string]$InstallPath = "$env:LOCALAPPDATA\MP3AlbumTool",
    [string]$GitHubRepo = "Amok-83/MP3-TOOL",
    [switch]$AddToPath = $false
)

# Configuration
$AppName = "MP3 Album Tool"
$ExeName = "MP3AlbumTool.exe"
$TempDir = "$env:TEMP\MP3AlbumTool_Install"
$GitHubReleaseUrl = "https://api.github.com/repos/$GitHubRepo/releases/latest"
$GitHubRawUrl = "https://raw.githubusercontent.com/$GitHubRepo/main"

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Header {
    Clear-Host
    Write-ColorOutput Green @"
===============================================================
                    MP3 ALBUM TOOL
                   Automatic Installer
===============================================================
"@
    Write-Host ""
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Download-FromGitHub {
    param($BaseUrl, $OutputPath)
    
    try {
        Write-ColorOutput Yellow "Downloading from GitHub..."
        
        # Set TLS version
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $ProgressPreference = 'SilentlyContinue'
        
        # List of files to download
        $FilesToDownload = @(
            "MP3AlbumTool_Distribuicao_Final/MP3AlbumTool.exe",
            "final_optimized_mp3_tool.py",
            "MP3AlbumTool_Distribuicao_Final/config.json",
            "MP3AlbumTool_Distribuicao_Final/README.md",
            "icon.ico"
        )
        
        $DownloadedFiles = @()
        
        foreach ($File in $FilesToDownload) {
            $FileUrl = "$BaseUrl/$File"
            $FileName = Split-Path $File -Leaf
            $LocalPath = Join-Path $OutputPath $FileName
            
            Write-Host "Downloading: $FileName"
            
            try {
                Invoke-WebRequest -Uri $FileUrl -OutFile $LocalPath -UseBasicParsing
                $DownloadedFiles += $LocalPath
                Write-ColorOutput Green "Downloaded: $FileName"
            }
            catch {
                Write-ColorOutput Yellow "Could not download: $FileName (may not exist)"
            }
        }
        
        if ($DownloadedFiles.Count -gt 0) {
            Write-ColorOutput Green "Download completed! Downloaded $($DownloadedFiles.Count) files."
            return $true
        } else {
            Write-ColorOutput Red "No files were downloaded successfully."
            return $false
        }
    }
    catch {
        Write-ColorOutput Red "ERROR: Download failed! Check internet connection and repository URL."
        Write-Host "Error details: $($_.Exception.Message)"
        return $false
    }
}



function Install-Application {
    param($SourcePath, $DestinationPath)
    
    try {
        Write-ColorOutput Yellow "Installing application..."
        
        # Create installation folder
        if (!(Test-Path $DestinationPath)) {
            New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
        }
        
        # Copy all downloaded files to destination
        $SourceFiles = Get-ChildItem $SourcePath -File
        $CopiedFiles = 0
        
        foreach ($File in $SourceFiles) {
            try {
                Copy-Item $File.FullName $DestinationPath -Force
                Write-ColorOutput Green "Copied: $($File.Name)"
                $CopiedFiles++
            }
            catch {
                Write-ColorOutput Yellow "Could not copy: $($File.Name)"
            }
        }
        
        if ($CopiedFiles -gt 0) {
            Write-ColorOutput Green "Installation completed! Copied $CopiedFiles files."
            return $true
        } else {
            Write-ColorOutput Red "No files were copied to installation directory."
            return $false
        }
    }
    catch {
        Write-ColorOutput Red "Installation error: $($_.Exception.Message)"
        return $false
    }
}

function Create-Shortcuts {
    param($InstallPath, $ExeName)
    
    try {
        $ExePath = Join-Path $InstallPath $ExeName
        $IconPath = Join-Path $InstallPath "icon.ico"
        
        # Create desktop shortcut
        $DesktopPath = [Environment]::GetFolderPath("Desktop")
        $ShortcutPath = Join-Path $DesktopPath "MP3 Album Tool.lnk"
        
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = $ExePath
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = "MP3 Album Tool"
        if (Test-Path $IconPath) {
            $Shortcut.IconLocation = $IconPath
        }
        $Shortcut.Save()
        
        Write-ColorOutput Green "Desktop shortcut created"
        
        # Create Start Menu shortcut
        $StartMenuPath = [Environment]::GetFolderPath("StartMenu")
        $StartMenuShortcut = Join-Path $StartMenuPath "Programs\MP3 Album Tool.lnk"
        
        $Shortcut2 = $WshShell.CreateShortcut($StartMenuShortcut)
        $Shortcut2.TargetPath = $ExePath
        $Shortcut2.WorkingDirectory = $InstallPath
        $Shortcut2.Description = "MP3 Album Tool"
        if (Test-Path $IconPath) {
            $Shortcut2.IconLocation = $IconPath
        }
        $Shortcut2.Save()
        
        Write-ColorOutput Green "Start Menu shortcut created"
        return $true
    }
    catch {
        Write-ColorOutput Yellow "Could not create shortcuts: $($_.Exception.Message)"
        return $false
    }
}

function Add-ToSystemPath {
    param($InstallPath)
    
    try {
        Write-ColorOutput Yellow "Adding to system PATH..."
        
        $CurrentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        if ($CurrentPath -notlike "*$InstallPath*") {
            $NewPath = "$CurrentPath;$InstallPath"
            [Environment]::SetEnvironmentVariable("Path", $NewPath, "Machine")
            Write-ColorOutput Green "Added to PATH!"
        } else {
            Write-ColorOutput Yellow "Already exists in PATH"
        }
        return $true
    }
    catch {
        Write-ColorOutput Red "Error adding to PATH: $($_.Exception.Message)"
        return $false
    }
}

function Create-Uninstaller {
    param($InstallPath)
    
    try {
        Write-ColorOutput Yellow "Creating uninstaller..."
        
        $UninstallerPath = Join-Path $InstallPath "Uninstall_MP3AlbumTool.bat"
        
        $UninstallerContent = @"
@echo off
title MP3 Album Tool - Uninstaller
echo.
echo ===============================================================
echo                    MP3 ALBUM TOOL
echo                      Uninstaller
echo ===============================================================
echo.

echo Removing shortcuts...
del "%USERPROFILE%\Desktop\MP3 Album Tool.lnk" 2>nul
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk" 2>nul

echo Removing application files...
cd /d "%TEMP%"

echo Removing installation directory and all files...
rmdir /s /q "$InstallPath" 2>nul

echo Verifying removal...
if exist "$InstallPath" (
    echo Warning: Some files may still exist. Trying alternative removal...
    timeout /t 2 /nobreak >nul
    rmdir /s /q "$InstallPath" 2>nul
)

echo.
echo ===============================================================
echo                 UNINSTALLATION COMPLETED!
echo ===============================================================
echo.
pause
"@
        
        $UninstallerContent | Out-File -FilePath $UninstallerPath -Encoding UTF8
        Write-ColorOutput Green "Uninstaller created successfully"
        return $true
    }
    catch {
        Write-ColorOutput Yellow "Could not create uninstaller: $($_.Exception.Message)"
        return $false
    }
}

function Cleanup-TempFiles {
    param($TempDir)
    
    try {
        if (Test-Path $TempDir) {
            Remove-Item $TempDir -Recurse -Force
            Write-ColorOutput Green "Temporary files removed"
        }
    }
    catch {
        Write-ColorOutput Yellow "Could not remove temporary files"
    }
}

# MAIN SCRIPT
Write-Header

Write-ColorOutput Cyan "Starting MP3 Album Tool installation..."
Write-ColorOutput White "Installation path: $InstallPath"
Write-ColorOutput White "GitHub repository: $GitHubRepo"
Write-Host ""

# Create temporary directory
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Download from GitHub
$DownloadPath = Join-Path $TempDir "downloads"
if (!(Test-Path $DownloadPath)) {
    New-Item -ItemType Directory -Path $DownloadPath -Force | Out-Null
}

if (-not (Download-FromGitHub -BaseUrl $GitHubRawUrl -OutputPath $DownloadPath)) {
    Write-ColorOutput Red "Failed to download from GitHub"
    Cleanup-TempFiles -TempDir $TempDir
    Read-Host "Press any key to continue"
    exit 1
}

# Install application
if (-not (Install-Application -SourcePath $DownloadPath -DestinationPath $InstallPath)) {
    Write-ColorOutput Red "Failed to install application"
    Cleanup-TempFiles -TempDir $TempDir
    Read-Host "Press any key to continue"
    exit 1
}

# Create shortcuts
Create-Shortcuts -InstallPath $InstallPath -ExeName $ExeName

# Create uninstaller
Create-Uninstaller -InstallPath $InstallPath

# Add to PATH if requested
if ($AddToPath) {
    Add-ToSystemPath -InstallPath $InstallPath
}

# Cleanup
Cleanup-TempFiles -TempDir $TempDir

# Success message
Write-Host ""
Write-ColorOutput Green "Installation completed successfully!"
Write-ColorOutput White "Application installed at: $InstallPath"
Write-ColorOutput White "Shortcuts created on Desktop and Start Menu"
Write-Host ""

# Ask to launch application
$Launch = Read-Host "Would you like to launch MP3 Album Tool now? (Y/N)"
if ($Launch -eq "Y" -or $Launch -eq "y") {
    $ExePath = Join-Path $InstallPath $ExeName
    if (Test-Path $ExePath) {
        Start-Process $ExePath
        Write-ColorOutput Green "MP3 Album Tool launched!"
    } else {
        Write-ColorOutput Red "Executable not found at: $ExePath"
    }
}

Write-Host ""
Write-ColorOutput Cyan "Thank you for using MP3 Album Tool!"
Read-Host "Press any key to continue"