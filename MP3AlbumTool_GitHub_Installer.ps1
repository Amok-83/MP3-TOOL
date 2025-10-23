# MP3 Album Tool - GitHub Installer
# Version: 1.0
# Description: Automatic installer that downloads and installs MP3 Album Tool from GitHub

param(
    [string]$InstallPath = "C:\Program Files\MP3AlbumTool",
    [string]$GitHubRepo = "Amok-83/MP3-TOOL",
    [switch]$AddToPath = $false
)

# Configuration
$AppName = "MP3 Album Tool"
$ExeName = "MP3AlbumTool.exe"
$TempDir = "$env:TEMP\MP3AlbumTool_Install"
$GitHubReleaseUrl = "https://api.github.com/repos/$GitHubRepo/releases/latest"
$GitHubDownloadUrl = "https://github.com/$GitHubRepo/archive/refs/heads/main.zip"

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
╔══════════════════════════════════════════════════════════════╗
║                    🎵 MP3 ALBUM TOOL                        ║
║                   Automatic Installer                       ║
╚══════════════════════════════════════════════════════════════╝
"@
    Write-Host ""
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Download-FromGitHub {
    param($Url, $OutputPath)
    
    try {
        Write-ColorOutput Yellow "📥 Downloading from: $Url"
        
        # Use Invoke-WebRequest with appropriate settings
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $Url -OutFile $OutputPath -UseBasicParsing
        
        Write-ColorOutput Green "✅ Download completed!"
        return $true
    }
    catch {
        Write-ColorOutput Red "❌ Download error: $($_.Exception.Message)"
        return $false
    }
}

function Extract-Archive {
    param($ArchivePath, $ExtractPath)
    
    try {
        Write-ColorOutput Yellow "📦 Extracting files..."
        
        # Create destination folder
        if (!(Test-Path $ExtractPath)) {
            New-Item -ItemType Directory -Path $ExtractPath -Force | Out-Null
        }
        
        # Extract using .NET
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($ArchivePath, $ExtractPath)
        
        Write-ColorOutput Green "✅ Extraction completed!"
        return $true
    }
    catch {
        Write-ColorOutput Red "❌ Extraction error: $($_.Exception.Message)"
        return $false
    }
}

function Install-Application {
    param($SourcePath, $DestinationPath)
    
    try {
        Write-ColorOutput Yellow "📁 Installing application..."
        
        # Create installation folder
        if (!(Test-Path $DestinationPath)) {
            New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
        }
        
        # Find extracted folder (usually has -main suffix)
        $ExtractedFolder = Get-ChildItem $SourcePath -Directory | Where-Object { $_.Name -like "*main*" -or $_.Name -like "*master*" } | Select-Object -First 1
        
        if ($ExtractedFolder) {
            $SourceFiles = "$($ExtractedFolder.FullName)\MP3AlbumTool_Distribuicao_Final\*"
        } else {
            $SourceFiles = "$SourcePath\*"
        }
        
        # Copy files
        Copy-Item -Path $SourceFiles -Destination $DestinationPath -Recurse -Force
        
        Write-ColorOutput Green "✅ Application installed at: $DestinationPath"
        return $true
    }
    catch {
        Write-ColorOutput Red "❌ Installation error: $($_.Exception.Message)"
        return $false
    }
}

function Create-Shortcuts {
    param($InstallPath, $ExeName)
    
    try {
        Write-ColorOutput Yellow "🔗 Creating shortcuts..."
        
        $WshShell = New-Object -comObject WScript.Shell
        $ExePath = Join-Path $InstallPath $ExeName
        
        # Desktop shortcut
        $DesktopPath = [Environment]::GetFolderPath("Desktop")
        $DesktopShortcut = $WshShell.CreateShortcut("$DesktopPath\$AppName.lnk")
        $DesktopShortcut.TargetPath = $ExePath
        $DesktopShortcut.WorkingDirectory = $InstallPath
        $DesktopShortcut.Description = $AppName
        $DesktopShortcut.Save()
        
        # Start Menu shortcut
        $StartMenuPath = [Environment]::GetFolderPath("StartMenu")
        $StartMenuShortcut = $WshShell.CreateShortcut("$StartMenuPath\Programs\$AppName.lnk")
        $StartMenuShortcut.TargetPath = $ExePath
        $StartMenuShortcut.WorkingDirectory = $InstallPath
        $StartMenuShortcut.Description = $AppName
        $StartMenuShortcut.Save()
        
        Write-ColorOutput Green "✅ Shortcuts created!"
        return $true
    }
    catch {
        Write-ColorOutput Red "❌ Error creating shortcuts: $($_.Exception.Message)"
        return $false
    }
}

function Add-ToSystemPath {
    param($InstallPath)
    
    try {
        Write-ColorOutput Yellow "🛤️ Adding to system PATH..."
        
        $CurrentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        if ($CurrentPath -notlike "*$InstallPath*") {
            $NewPath = "$CurrentPath;$InstallPath"
            [Environment]::SetEnvironmentVariable("Path", $NewPath, "Machine")
            Write-ColorOutput Green "✅ Added to PATH!"
        } else {
            Write-ColorOutput Yellow "ℹ️ Already exists in PATH"
        }
        return $true
    }
    catch {
        Write-ColorOutput Red "❌ Error adding to PATH: $($_.Exception.Message)"
        return $false
    }
}

function Cleanup-TempFiles {
    param($TempDir)
    
    try {
        if (Test-Path $TempDir) {
            Remove-Item $TempDir -Recurse -Force
            Write-ColorOutput Green "🧹 Temporary files removed"
        }
    }
    catch {
        Write-ColorOutput Yellow "⚠️ Could not remove temporary files"
    }
}

# MAIN SCRIPT
Write-Header

# Check administrator privileges
if (-not (Test-Administrator)) {
    Write-ColorOutput Red "❌ This script must be run as Administrator!"
    Write-ColorOutput Yellow "💡 Right-click and select 'Run as administrator'"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-ColorOutput Cyan "🚀 Starting MP3 Album Tool installation..."
Write-ColorOutput White "📍 Installation path: $InstallPath"
Write-ColorOutput White "📦 GitHub repository: $GitHubRepo"
Write-Host ""

# Create temporary directory
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Download from GitHub
$ZipFile = Join-Path $TempDir "mp3albumtool.zip"
if (-not (Download-FromGitHub -Url $GitHubDownloadUrl -OutputPath $ZipFile)) {
    Write-ColorOutput Red "❌ Failed to download from GitHub"
    Cleanup-TempFiles -TempDir $TempDir
    Read-Host "Press Enter to exit"
    exit 1
}

# Extract files
$ExtractPath = Join-Path $TempDir "extracted"
if (-not (Extract-Archive -ArchivePath $ZipFile -ExtractPath $ExtractPath)) {
    Write-ColorOutput Red "❌ Failed to extract files"
    Cleanup-TempFiles -TempDir $TempDir
    Read-Host "Press Enter to exit"
    exit 1
}

# Install application
if (-not (Install-Application -SourcePath $ExtractPath -DestinationPath $InstallPath)) {
    Write-ColorOutput Red "❌ Failed to install application"
    Cleanup-TempFiles -TempDir $TempDir
    Read-Host "Press Enter to exit"
    exit 1
}

# Create shortcuts
Create-Shortcuts -InstallPath $InstallPath -ExeName $ExeName

# Add to PATH if requested
if ($AddToPath) {
    Add-ToSystemPath -InstallPath $InstallPath
}

# Cleanup
Cleanup-TempFiles -TempDir $TempDir

# Success message
Write-Host ""
Write-ColorOutput Green "🎉 Installation completed successfully!"
Write-ColorOutput White "📍 Application installed at: $InstallPath"
Write-ColorOutput White "🔗 Shortcuts created on Desktop and Start Menu"
Write-Host ""

# Ask to launch application
$Launch = Read-Host "Would you like to launch MP3 Album Tool now? (Y/N)"
if ($Launch -eq "Y" -or $Launch -eq "y") {
    $ExePath = Join-Path $InstallPath $ExeName
    if (Test-Path $ExePath) {
        Start-Process $ExePath
        Write-ColorOutput Green "🚀 MP3 Album Tool launched!"
    } else {
        Write-ColorOutput Red "❌ Executable not found at: $ExePath"
    }
}

Write-Host ""
Write-ColorOutput Cyan "Thank you for using MP3 Album Tool!"
Read-Host "Press Enter to exit"