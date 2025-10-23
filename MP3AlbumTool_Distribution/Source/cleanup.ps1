# MP3 Album Tool - Script de Limpeza
# ===================================
# Remove ficheiros temporários e desnecessários

Write-Host "🧹 MP3 Album Tool - Limpeza" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Ficheiros e pastas a remover
$itemsToRemove = @(
    "__pycache__",
    "*.pyc",
    "*.pyo", 
    "*.pyd",
    ".pytest_cache",
    "build",
    "*.egg-info",
    ".coverage",
    "htmlcov",
    "*.log",
    "*.tmp",
    "*.temp",
    "Thumbs.db",
    ".DS_Store"
)

Write-Host "🔍 Procurando ficheiros desnecessários..." -ForegroundColor Yellow

$removedCount = 0
foreach ($item in $itemsToRemove) {
    $found = Get-ChildItem -Path . -Name $item -Recurse -Force -ErrorAction SilentlyContinue
    foreach ($file in $found) {
        try {
            Remove-Item -Path $file -Recurse -Force
            Write-Host "🗑️  Removido: $file" -ForegroundColor Gray
            $removedCount++
        } catch {
            Write-Host "⚠️  Não foi possível remover: $file" -ForegroundColor Yellow
        }
    }
}

# Remover ficheiros de backup antigos
$backupFiles = Get-ChildItem -Path . -Name "*.bak" -Recurse -ErrorAction SilentlyContinue
foreach ($backup in $backupFiles) {
    try {
        Remove-Item -Path $backup -Force
        Write-Host "🗑️  Backup removido: $backup" -ForegroundColor Gray
        $removedCount++
    } catch {
        Write-Host "⚠️  Não foi possível remover backup: $backup" -ForegroundColor Yellow
    }
}

if ($removedCount -eq 0) {
    Write-Host "✅ Nenhum ficheiro desnecessário encontrado!" -ForegroundColor Green
} else {
    Write-Host "✅ Limpeza concluída! $removedCount itens removidos." -ForegroundColor Green
}

Write-Host "🎉 Projeto limpo e organizado!" -ForegroundColor Green