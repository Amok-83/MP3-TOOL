# MP3 Album Tool - Desinstalador
# ===============================
# Este script remove completamente o MP3 Album Tool do sistema

param(
    [string]$InstallPath = "$env:ProgramFiles\MP3AlbumTool",
    [switch]$Silent = $false
)

Write-Host "🗑️  MP3 Album Tool - Desinstalador" -ForegroundColor Red
Write-Host "===================================" -ForegroundColor Red
Write-Host ""

# Verificar se está a correr como administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Este desinstalador precisa de ser executado como Administrador!" -ForegroundColor Red
    Write-Host "   Clique com o botão direito no ficheiro e selecione 'Executar como administrador'" -ForegroundColor Yellow
    Write-Host ""
    if (-not $Silent) { Read-Host "Prima Enter para sair" }
    exit 1
}

# Confirmar desinstalação
if (-not $Silent) {
    Write-Host "⚠️  ATENÇÃO: Esta operação irá remover completamente o MP3 Album Tool do sistema!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Será removido:" -ForegroundColor Cyan
    Write-Host "  • Pasta de instalação: $InstallPath" -ForegroundColor White
    Write-Host "  • Atalho no Desktop" -ForegroundColor White
    Write-Host "  • Entrada no Menu Iniciar" -ForegroundColor White
    Write-Host "  • Entrada no PATH do sistema" -ForegroundColor White
    Write-Host "  • Entradas no registo do Windows" -ForegroundColor White
    Write-Host ""
    
    $confirmation = Read-Host "Tem a certeza que deseja continuar? (S/N)"
    if ($confirmation -notmatch '^[SsYy]') {
        Write-Host "❌ Desinstalação cancelada pelo utilizador" -ForegroundColor Yellow
        Read-Host "Prima Enter para sair"
        exit 0
    }
}

Write-Host "🔄 Iniciando desinstalação..." -ForegroundColor Yellow
Write-Host ""

$errors = @()
$warnings = @()

# Função para registar erros
function Add-Error($message) {
    $script:errors += $message
    Write-Host "❌ $message" -ForegroundColor Red
}

# Função para registar avisos
function Add-Warning($message) {
    $script:warnings += $message
    Write-Host "⚠️  $message" -ForegroundColor Yellow
}

# 1. Terminar processos da aplicação
Write-Host "🔄 Terminando processos da aplicação..." -ForegroundColor Yellow
try {
    $processes = Get-Process -Name "MP3AlbumTool" -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($process in $processes) {
            $process.Kill()
            Start-Sleep -Seconds 1
        }
        Write-Host "✅ Processos terminados" -ForegroundColor Green
    } else {
        Write-Host "✅ Nenhum processo em execução" -ForegroundColor Green
    }
} catch {
    Add-Warning "Não foi possível terminar todos os processos: $($_.Exception.Message)"
}

# 2. Remover atalho do Desktop
Write-Host "🔄 Removendo atalho do Desktop..." -ForegroundColor Yellow
try {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "MP3 Album Tool.lnk"
    
    if (Test-Path $shortcutPath) {
        Remove-Item $shortcutPath -Force
        Write-Host "✅ Atalho do Desktop removido" -ForegroundColor Green
    } else {
        Write-Host "✅ Atalho do Desktop não encontrado" -ForegroundColor Green
    }
} catch {
    Add-Error "Erro ao remover atalho do Desktop: $($_.Exception.Message)"
}

# 3. Remover entrada do Menu Iniciar
Write-Host "🔄 Removendo entrada do Menu Iniciar..." -ForegroundColor Yellow
try {
    $startMenuPaths = @(
        "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk",
        "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\MP3AlbumTool",
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk"
    )
    
    $removed = $false
    foreach ($path in $startMenuPaths) {
        if (Test-Path $path) {
            Remove-Item $path -Recurse -Force
            $removed = $true
        }
    }
    
    if ($removed) {
        Write-Host "✅ Entrada do Menu Iniciar removida" -ForegroundColor Green
    } else {
        Write-Host "✅ Entrada do Menu Iniciar não encontrada" -ForegroundColor Green
    }
} catch {
    Add-Error "Erro ao remover entrada do Menu Iniciar: $($_.Exception.Message)"
}

# 4. Remover do PATH do sistema
Write-Host "🔄 Removendo do PATH do sistema..." -ForegroundColor Yellow
try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    if ($currentPath -like "*$InstallPath*") {
        $newPath = $currentPath -replace [regex]::Escape(";$InstallPath"), ""
        $newPath = $newPath -replace [regex]::Escape("$InstallPath;"), ""
        $newPath = $newPath -replace [regex]::Escape("$InstallPath"), ""
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
        Write-Host "✅ Removido do PATH do sistema" -ForegroundColor Green
    } else {
        Write-Host "✅ Não estava no PATH do sistema" -ForegroundColor Green
    }
} catch {
    Add-Warning "Não foi possível remover do PATH: $($_.Exception.Message)"
}

# 5. Remover entradas do registo
Write-Host "🔄 Removendo entradas do registo..." -ForegroundColor Yellow
try {
    $registryPaths = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\MP3 Album Tool",
        "HKLM:\Software\MP3AlbumTool",
        "HKCU:\Software\MP3AlbumTool"
    )
    
    $removed = $false
    foreach ($regPath in $registryPaths) {
        if (Test-Path $regPath) {
            Remove-Item $regPath -Recurse -Force
            $removed = $true
        }
    }
    
    if ($removed) {
        Write-Host "✅ Entradas do registo removidas" -ForegroundColor Green
    } else {
        Write-Host "✅ Nenhuma entrada do registo encontrada" -ForegroundColor Green
    }
} catch {
    Add-Warning "Não foi possível remover todas as entradas do registo: $($_.Exception.Message)"
}

# 6. Remover pasta de instalação
Write-Host "🔄 Removendo pasta de instalação..." -ForegroundColor Yellow
try {
    if (Test-Path $InstallPath) {
        # Tentar remover atributos de só leitura
        Get-ChildItem $InstallPath -Recurse -Force | ForEach-Object {
            $_.Attributes = $_.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
        }
        
        Remove-Item $InstallPath -Recurse -Force
        Write-Host "✅ Pasta de instalação removida: $InstallPath" -ForegroundColor Green
    } else {
        Write-Host "✅ Pasta de instalação não encontrada" -ForegroundColor Green
    }
} catch {
    Add-Error "Erro ao remover pasta de instalação: $($_.Exception.Message)"
}

# 7. Limpar cache e ficheiros temporários
Write-Host "🔄 Limpando ficheiros temporários..." -ForegroundColor Yellow
try {
    $tempPaths = @(
        "$env:TEMP\MP3AlbumTool*",
        "$env:LOCALAPPDATA\MP3AlbumTool",
        "$env:APPDATA\MP3AlbumTool"
    )
    
    $cleaned = $false
    foreach ($tempPath in $tempPaths) {
        if (Test-Path $tempPath) {
            Remove-Item $tempPath -Recurse -Force -ErrorAction SilentlyContinue
            $cleaned = $true
        }
    }
    
    if ($cleaned) {
        Write-Host "✅ Ficheiros temporários limpos" -ForegroundColor Green
    } else {
        Write-Host "✅ Nenhum ficheiro temporário encontrado" -ForegroundColor Green
    }
} catch {
    Add-Warning "Não foi possível limpar todos os ficheiros temporários: $($_.Exception.Message)"
}

# Mostrar resumo
Write-Host ""
Write-Host "📊 RESUMO DA DESINSTALAÇÃO" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "🎉 Desinstalação concluída com sucesso!" -ForegroundColor Green
    Write-Host "   O MP3 Album Tool foi completamente removido do sistema." -ForegroundColor Green
} else {
    if ($errors.Count -gt 0) {
        Write-Host "❌ Desinstalação concluída com erros:" -ForegroundColor Red
        foreach ($error in $errors) {
            Write-Host "   • $error" -ForegroundColor Red
        }
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host "⚠️  Avisos durante a desinstalação:" -ForegroundColor Yellow
        foreach ($warning in $warnings) {
            Write-Host "   • $warning" -ForegroundColor Yellow
        }
    }
    
    if ($errors.Count -eq 0) {
        Write-Host "✅ Desinstalação concluída com avisos menores" -ForegroundColor Green
    }
}

Write-Host ""
if (-not $Silent) {
    Read-Host "Press Enter to exit"
}