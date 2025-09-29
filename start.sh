#!/bin/bash

# Script para iniciar a aplicação unificada de gestão de restaurantes

echo "🍽️ Iniciando Sistema Unificado de Gestão de Restaurantes..."

# Parar aplicações anteriores
echo "🛑 Parando aplicações anteriores..."
pkill -f "streamlit" 2>/dev/null

# Aguardar um pouco
sleep 2

# Navegar para o diretório
cd /home/mkamei/developer/nersant/python/avaliacao-gestao-restaurantes

# Verificar se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Por favor, execute: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Iniciar aplicação principal
echo "🚀 Iniciando aplicação na porta 8080..."
.venv/bin/python -m streamlit run app.py --server.port 8080 &

# Aguardar inicialização
sleep 3

echo ""
echo "✅ Aplicação iniciada com sucesso!"
echo ""
echo "🌐 Acesse: http://localhost:8080"
echo "👤 Cliente - Registar novo cliente ou entrar com dados existentes"
echo "👨‍💼 Admin - Utilizador: admin | Senha: admin123"
echo ""
echo "Para parar a aplicação, execute: pkill -f streamlit"
echo ""