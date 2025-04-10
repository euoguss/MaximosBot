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
mkdir -p /opt/maximos_bot && cd /opt/maximos_bot
git clone -b main https://github.com/euoguss/MaximosBot.git .

echo "🔐 Certifique-se de que o arquivo .env foi criado com as variáveis necessárias."
echo "   Use: scp .env root@srv788024.hstgr.cloud:/opt/maximos_bot/.env"

echo "🚀 Subindo containers com Docker Compose..."
docker-compose up -d --build

echo "✅ Tudo pronto! Acesse:"
echo "📦 Waha: http://srv788024.hstgr.cloud:3000"
echo "🧠 API:  http://srv788024.hstgr.cloud:5000"

