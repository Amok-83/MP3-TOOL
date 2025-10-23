# MP3 Album Tool - Instalador PowerShell
# =====================================
# Instalador simples para MP3 Album Tool

param(
    [string]$InstallPath = "$env:ProgramFiles\MP3AlbumTool"
)

Write-Host "🎵 MP3 Album Tool - Instalador" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Verificar se está a executar como administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "⚠️  Este instalador requer privilégios de administrador." -ForegroundColor Yellow
    Write-Host "🔄 A reiniciar como administrador..." -ForegroundColor Yellow
    Start-Process PowerShell -Verb RunAs "-File `"$PSCommandPath`" -InstallPath `"$InstallPath`""
    exit
}

Write-Host "📁 Pasta de instalação: $InstallPath" -ForegroundColor White

# Criar pasta de instalação
if (!(Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Host "✅ Pasta de instalação criada" -ForegroundColor Green
}

# Copiar executável
$exePath = "dist\MP3AlbumTool.exe"
if (Test-Path $exePath) {
    Copy-Item $exePath "$InstallPath\MP3AlbumTool.exe" -Force
    Write-Host "✅ Executável instalado" -ForegroundColor Green
} else {
    Write-Host "❌ Executável não encontrado: $exePath" -ForegroundColor Red
    exit 1
}

# Copiar documentação
if (Test-Path "README.md") {
    Copy-Item "README.md" "$InstallPath\" -Force
}
if (Test-Path "LICENSE.txt") {
    Copy-Item "LICENSE.txt" "$InstallPath\" -Force
}
Write-Host "✅ Documentação instalada" -ForegroundColor Green

# Criar atalho no Desktop
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\MP3 Album Tool.lnk"

$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "$InstallPath\MP3AlbumTool.exe"
$Shortcut.WorkingDirectory = $InstallPath
$Shortcut.Description = "MP3 Album Tool - Editor de Metadados MP3"
$Shortcut.Save()
Write-Host "✅ Atalho criado no Desktop" -ForegroundColor Green

# Criar atalho no Menu Iniciar
$startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
$startMenuShortcut = "$startMenuPath\MP3 Album Tool.lnk"

$Shortcut2 = $WshShell.CreateShortcut($startMenuShortcut)
$Shortcut2.TargetPath = "$InstallPath\MP3AlbumTool.exe"
$Shortcut2.WorkingDirectory = $InstallPath
$Shortcut2.Description = "MP3 Album Tool - Editor de Metadados MP3"
$Shortcut2.Save()
Write-Host "✅ Atalho criado no Menu Iniciar" -ForegroundColor Green

# Adicionar ao PATH (opcional)
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
if ($currentPath -notlike "*$InstallPath*") {
    $newPath = "$currentPath;$InstallPath"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
    Write-Host "✅ Adicionado ao PATH do sistema" -ForegroundColor Green
}

# Criar desinstalador
$uninstaller = @"
# MP3 Album Tool - Desinstalador
Write-Host "🗑️  Desinstalando MP3 Album Tool..." -ForegroundColor Yellow

# Remover pasta de instalação
if (Test-Path "$InstallPath") {
    Remove-Item -Recurse -Force "$InstallPath"
    Write-Host "✅ Ficheiros removidos" -ForegroundColor Green
}

# Remover atalhos
if (Test-Path "$shortcutPath") {
    Remove-Item "$shortcutPath" -Force
    Write-Host "✅ Atalho do Desktop removido" -ForegroundColor Green
}

if (Test-Path "$startMenuShortcut") {
    Remove-Item "$startMenuShortcut" -Force
    Write-Host "✅ Atalho do Menu Iniciar removido" -ForegroundColor Green
}

# Remover do PATH
`$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
if (`$currentPath -like "*$InstallPath*") {
    `$newPath = `$currentPath -replace ";$InstallPath", ""
    [Environment]::SetEnvironmentVariable("PATH", `$newPath, "Machine")
    Write-Host "✅ Removido do PATH do sistema" -ForegroundColor Green
}

Write-Host "🎉 MP3 Album Tool desinstalado com sucesso!" -ForegroundColor Green
Read-Host "Pressione Enter para continuar"
"@

$uninstaller | Out-File -FilePath "$InstallPath\Uninstall.ps1" -Encoding UTF8
Write-Host "✅ Desinstalador criado" -ForegroundColor Green

# Registar no Windows (Adicionar/Remover Programas)
$regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MP3AlbumTool"
New-Item -Path $regPath -Force | Out-Null
Set-ItemProperty -Path $regPath -Name "DisplayName" -Value "MP3 Album Tool"
Set-ItemProperty -Path $regPath -Name "DisplayVersion" -Value "1.0.0"
Set-ItemProperty -Path $regPath -Name "Publisher" -Value "MP3 Album Tool"
Set-ItemProperty -Path $regPath -Name "InstallLocation" -Value $InstallPath
Set-ItemProperty -Path $regPath -Name "UninstallString" -Value "PowerShell.exe -ExecutionPolicy Bypass -File `"$InstallPath\Uninstall.ps1`""
Set-ItemProperty -Path $regPath -Name "DisplayIcon" -Value "$InstallPath\MP3AlbumTool.exe"
Write-Host "✅ Registado no Windows" -ForegroundColor Green

Write-Host "`n🎉 Instalação concluída com sucesso!" -ForegroundColor Green
Write-Host "📍 Localização: $InstallPath" -ForegroundColor White
Write-Host "🖥️  Atalho criado no Desktop" -ForegroundColor White
Write-Host "📋 Disponível no Menu Iniciar" -ForegroundColor White
Write-Host "🗑️  Para desinstalar: Execute Uninstall.ps1 na pasta de instalação" -ForegroundColor White

Write-Host "`n🚀 Pode agora executar MP3 Album Tool!" -ForegroundColor Cyan
Read-Host "Pressione Enter para continuar"