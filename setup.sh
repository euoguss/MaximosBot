#!/bin/bash

echo "🔧 Atualizando pacotes..."
apt update && apt upgrade -y

echo "🐳 Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "⚙️ Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

echo "🔧 Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "⚙️ Instalando Docker Compose..."
    apt install docker-compose -y
fi

echo "📁 Criando pasta do projeto..."
mkdir -p /opt/meu_bot && cd /opt/meu_bot

echo "📦 Copie seu projeto para /opt/meu_bot com SCP ou Git"
echo "➡️ Ex: scp -r ./meu_projeto root@srv788024.hstgr.cloud:/opt/meu_bot"

echo "✅ Depois execute: docker-compose up --build -d"
