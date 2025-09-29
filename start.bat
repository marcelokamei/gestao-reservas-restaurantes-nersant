@echo off
REM Script para iniciar a aplicação unificada de gestão de restaurantes no Windows

echo 🍽️ Iniciando Sistema Unificado de Gestão de Restaurantes...

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Iniciar aplicação principal na porta 8080
streamlit run app.py --server.port 8080

REM Instruções de acesso
echo.
echo Acesse: http://localhost:8080
echo Admin: admin / admin123
echo Cliente: Registre novo ou use existente
pause