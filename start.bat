@echo off
REM Script para iniciar a aplicação unificada de gestão de restaurantes no Windows

echo 🍽️ Iniciando Sistema Unificado de Gestão de Restaurantes...

REM Verificar se o ambiente virtual existe
if not exist ".venv\" (
    echo ❌ Ambiente virtual não encontrado!
    echo Por favor, execute: python -m venv .venv
    echo Depois: .venv\Scripts\activate
    echo E então: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Parar aplicações anteriores do Streamlit
echo 🛑 Parando aplicações anteriores...
taskkill /f /im python.exe 2>nul

REM Aguardar um pouco
timeout /t 2 /nobreak >nul

echo 🚀 Iniciando aplicação na porta 8080...

REM Ativar ambiente virtual e iniciar aplicação
call .venv\Scripts\activate
start /b streamlit run app.py --server.port 8080

REM Aguardar inicialização
timeout /t 3 /nobreak >nul

echo.
echo ✅ Aplicação iniciada com sucesso!
echo.
echo 🌐 Acesse: http://localhost:8080
echo 👤 Cliente - Registar novo cliente ou entrar com dados existentes
echo 👨‍💼 Admin - Utilizador: admin / Senha: admin123
echo.
echo Para parar a aplicação, feche esta janela ou pressione Ctrl+C
pause