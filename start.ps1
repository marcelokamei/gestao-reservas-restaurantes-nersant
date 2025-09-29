# Script PowerShell para iniciar a aplicação unificada de gestão de restaurantes no Windows

Write-Host "🍽️ Iniciando Sistema Unificado de Gestão de Restaurantes..." -ForegroundColor Cyan

# Ativar ambiente virtual
. .\.venv\Scripts\Activate.ps1

# Iniciar aplicação principal na porta 8080
streamlit run app.py --server.port 8080

Write-Host ""
Write-Host "Acesse: http://localhost:8080" -ForegroundColor Green
Write-Host "Admin: admin / admin123" -ForegroundColor Yellow
Write-Host "Cliente: Registre novo ou use existente" -ForegroundColor Yellow