# Script PowerShell para iniciar a aplicação unificada de gestão de restaurantes no Windows

Write-Host "🍽️ Iniciando Sistema Unificado de Gestão de Restaurantes..." -ForegroundColor Cyan

# Verificar se o ambiente virtual existe
if (-not (Test-Path ".venv")) {
    Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, execute:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor White
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Parar aplicações anteriores do Streamlit
Write-Host "🛑 Parando aplicações anteriores..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Aguardar um pouco
Start-Sleep -Seconds 2

Write-Host "🚀 Iniciando aplicação na porta 8080..." -ForegroundColor Green

# Ativar ambiente virtual
try {
    . .\.venv\Scripts\Activate.ps1
    
    # Iniciar aplicação principal na porta 8080
    Start-Process -NoNewWindow streamlit -ArgumentList "run", "app.py", "--server.port", "8080"
    
    # Aguardar inicialização
    Start-Sleep -Seconds 3
    
    Write-Host ""
    Write-Host "✅ Aplicação iniciada com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Acesse: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "👤 Cliente - Registar novo cliente ou entrar com dados existentes" -ForegroundColor White
    Write-Host "👨‍💼 Admin - Utilizador: admin / Senha: admin123" -ForegroundColor White
    Write-Host ""
    Write-Host "Para parar a aplicação, feche esta janela ou pressione Ctrl+C" -ForegroundColor Yellow
    
    Read-Host "Pressione Enter para continuar"
}
catch {
    Write-Host "❌ Erro ao iniciar aplicação: $_" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}