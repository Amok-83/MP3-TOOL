# MP3 Album Tool - Script de Build
# =================================
# Este script automatiza a criação do executável

Write-Host "🎵 MP3 Album Tool - Build Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Verificar se Python está instalado
Write-Host "📋 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado! Instale Python primeiro." -ForegroundColor Red
    exit 1
}

# Instalar dependências
Write-Host "📦 Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Limpar builds anteriores
Write-Host "🧹 Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }

# Criar executável com PyInstaller
Write-Host "🔨 Criando executável..." -ForegroundColor Yellow
pyinstaller --onefile --windowed --name "MP3AlbumTool" --icon=icon.ico final_optimized_mp3_tool.py

# Verificar se foi criado com sucesso
if (Test-Path "dist\MP3AlbumTool.exe") {
    Write-Host "✅ Executável criado com sucesso!" -ForegroundColor Green
    Write-Host "📁 Localização: dist\MP3AlbumTool.exe" -ForegroundColor Green
    
    # Mostrar tamanho do ficheiro
    $fileSize = (Get-Item "dist\MP3AlbumTool.exe").Length / 1MB
    Write-Host "📊 Tamanho: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao criar executável!" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 Build concluído!" -ForegroundColor Green