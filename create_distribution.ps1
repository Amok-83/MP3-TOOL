# MP3 Album Tool - Script de Distribuição
# ========================================
# Cria pacote final para distribuição

Write-Host "📦 MP3 Album Tool - Criando Distribuição" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Criar pasta de distribuição
$distFolder = "MP3AlbumTool_Distribution"
if (Test-Path $distFolder) { Remove-Item -Recurse -Force $distFolder }
New-Item -ItemType Directory -Path $distFolder | Out-Null

Write-Host "📁 Criando estrutura de distribuição..." -ForegroundColor Yellow

# Copiar executável
Copy-Item "dist\MP3AlbumTool.exe" "$distFolder\"
Write-Host "✅ Executável copiado" -ForegroundColor Green

# Copiar documentação
Copy-Item "README.md" "$distFolder\"
Copy-Item "LICENSE.txt" "$distFolder\"
Write-Host "✅ Documentação copiada" -ForegroundColor Green

# Criar pasta de código fonte
New-Item -ItemType Directory -Path "$distFolder\Source" | Out-Null
Copy-Item "final_optimized_mp3_tool.py" "$distFolder\Source\"
Copy-Item "requirements.txt" "$distFolder\Source\"
Copy-Item "build.ps1" "$distFolder\Source\"
Copy-Item "cleanup.ps1" "$distFolder\Source\"
Copy-Item "mp3_tool.spec" "$distFolder\Source\"
Copy-Item "version_info.txt" "$distFolder\Source\"
Write-Host "✅ Código fonte copiado" -ForegroundColor Green

# Criar ficheiro de instruções
$instructions = @"
# 🎵 MP3 Album Tool - Instruções de Instalação

## 📋 Opções de Instalação

### Opção 1: Executável Direto (Mais Simples)
1. Execute diretamente o ficheiro **MP3AlbumTool.exe**
2. A aplicação irá iniciar imediatamente
3. Não requer instalação adicional

### Opção 2: Instalação com NSIS (Recomendado)
1. Instale NSIS (Nullsoft Scriptable Install System)
2. Execute: makensis installer.nsi
3. Execute o MP3AlbumTool_Setup.exe gerado
4. Siga as instruções do instalador

### Opção 3: Código Fonte
1. Instale Python 3.8+
2. Navegue para a pasta Source
3. Execute: pip install -r requirements.txt
4. Execute: python final_optimized_mp3_tool.py

## 📁 Conteúdo do Pacote

- **MP3AlbumTool.exe**: Executável principal
- **README.md**: Documentação completa
- **LICENSE.txt**: Licença MIT
- **Source/**: Código fonte e scripts de build

## 🎯 Como Usar

1. Execute MP3AlbumTool.exe
2. Clique em "Carregar Ficheiros" para selecionar MP3s
3. Edite metadados clicando duas vezes nas linhas
4. Use "Buscar no Deezer" para informações automáticas
5. Clique em "Guardar Alterações" para aplicar

## 📞 Suporte

Para suporte técnico ou reportar problemas, consulte o README.md

---
**MP3 Album Tool v1.0 - Desenvolvido com ❤️ para amantes de música**
"@

$instructions | Out-File -FilePath "$distFolder\INSTRUÇÕES.txt" -Encoding UTF8
Write-Host "✅ Instruções criadas" -ForegroundColor Green

# Mostrar resumo
Write-Host "`n📊 Resumo da Distribuição:" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

$files = Get-ChildItem -Path $distFolder -Recurse -File
$totalSize = ($files | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "📁 Pasta: $distFolder" -ForegroundColor White
Write-Host "📄 Ficheiros: $($files.Count)" -ForegroundColor White
Write-Host "📊 Tamanho Total: $([math]::Round($totalSize, 2)) MB" -ForegroundColor White

Write-Host "`n🎉 Distribuição criada com sucesso!" -ForegroundColor Green
Write-Host "📦 Localização: $distFolder" -ForegroundColor Green
Write-Host "🚀 Pronto para distribuir!" -ForegroundColor Green