#!/bin/bash

echo "🔧 Atualizando pacotes..."
apt update && apt upgrade -y

echo "🐳 Instalando Docker (se necessário)..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

echo "🔧 Instalando Docker Compose (se necessário)..."
if ! command -v docker-compose &> /dev/null; then
    apt install docker-compose -y
fi

echo "📁 Clonando o projeto do GitHub via HTTPS..."
cd /opt
git clone -b main https://github.com/euoguss/MaximosBot.git
cd MaximosBot

echo "🔐 Copie seu .env com:"
echo "   scp .env root@srv788024.hstgr.cloud:/opt/MaximosBot/.env"

echo "🚀 Subindo containers com Docker Compose..."
docker-compose up -d --build

echo "✅ Tudo pronto!"
echo "📦 Waha: http://srv788024.hstgr.cloud:3000"
echo "🧠 API:  http://srv788024.hstgr.cloud:5000"

