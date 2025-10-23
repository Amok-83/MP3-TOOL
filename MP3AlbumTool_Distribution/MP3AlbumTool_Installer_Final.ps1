# MP3 Album Tool - Instalador Final
# Este script instala o MP3 Album Tool no sistema

param(
    [string]$InstallPath = "$env:ProgramFiles\MP3AlbumTool"
)

Write-Host "🎵 MP3 Album Tool - Instalador" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está a correr como administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Este instalador precisa de ser executado como Administrador!" -ForegroundColor Red
    Write-Host "   Clique com o botão direito no ficheiro e selecione 'Executar como administrador'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Prima Enter para sair"
    exit 1
}

Write-Host "📁 Pasta de instalação: $InstallPath" -ForegroundColor Green
Write-Host ""

# Criar pasta de instalação
try {
    if (!(Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        Write-Host "✅ Pasta de instalação criada" -ForegroundColor Green
    } else {
        Write-Host "✅ Pasta de instalação já existe" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Erro ao criar pasta de instalação: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Prima Enter para sair"
    exit 1
}

# Copiar executável
try {
    $sourceExe = Join-Path $PSScriptRoot "dist\MP3AlbumTool.exe"
    $destExe = Join-Path $InstallPath "MP3AlbumTool.exe"
    
    if (Test-Path $sourceExe) {
        Copy-Item $sourceExe $destExe -Force
        Write-Host "✅ Executável copiado" -ForegroundColor Green
    } else {
        Write-Host "❌ Executável não encontrado: $sourceExe" -ForegroundColor Red
        Read-Host "Prima Enter para sair"
        exit 1
    }
} catch {
    Write-Host "❌ Erro ao copiar executável: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Prima Enter para sair"
    exit 1
}

# Copiar ficheiros de configuração
try {
    $configFiles = @("config.json", "LICENSE.txt", "README.md")
    foreach ($file in $configFiles) {
        $sourcePath = Join-Path $PSScriptRoot $file
        if (Test-Path $sourcePath) {
            $destPath = Join-Path $InstallPath $file
            Copy-Item $sourcePath $destPath -Force
            Write-Host "✅ $file copiado" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "⚠️  Aviso: Alguns ficheiros de configuração podem não ter sido copiados" -ForegroundColor Yellow
}

# Criar atalho no Desktop
try {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "MP3 Album Tool.lnk"
    
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = Join-Path $InstallPath "MP3AlbumTool.exe"
    $Shortcut.WorkingDirectory = $InstallPath
    $Shortcut.Description = "MP3 Album Tool - Ferramenta profissional para organizar álbuns MP3"
    $Shortcut.Save()
    
    Write-Host "✅ Atalho criado no Desktop" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Aviso: Não foi possível criar atalho no Desktop" -ForegroundColor Yellow
}

# Criar entrada no Menu Iniciar
try {
    $startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
    $startMenuShortcut = Join-Path $startMenuPath "MP3 Album Tool.lnk"
    
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($startMenuShortcut)
    $Shortcut.TargetPath = Join-Path $InstallPath "MP3AlbumTool.exe"
    $Shortcut.WorkingDirectory = $InstallPath
    $Shortcut.Description = "MP3 Album Tool - Ferramenta profissional para organizar álbuns MP3"
    $Shortcut.Save()
    
    Write-Host "✅ Entrada criada no Menu Iniciar" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Aviso: Não foi possível criar entrada no Menu Iniciar" -ForegroundColor Yellow
}

# Adicionar ao PATH (opcional)
try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    if ($currentPath -notlike "*$InstallPath*") {
        $newPath = $currentPath + ";" + $InstallPath
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
        Write-Host "✅ Adicionado ao PATH do sistema" -ForegroundColor Green
    } else {
        Write-Host "✅ Já está no PATH do sistema" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Aviso: Não foi possível adicionar ao PATH" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Instalação concluída com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Localização: $InstallPath" -ForegroundColor Cyan
Write-Host "🖥️  Atalho no Desktop: MP3 Album Tool" -ForegroundColor Cyan
Write-Host "📋 Menu Iniciar: MP3 Album Tool" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para desinstalar, execute: Remove-Item '$InstallPath' -Recurse -Force" -ForegroundColor Yellow
Write-Host ""
Read-Host "Prima Enter para sair"