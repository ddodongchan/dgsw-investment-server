#!/bin/bash

SERVICE_DIR=$1
SERVICE_NAME=$2

if [ -z "$SERVICE_DIR" ] || [ -z "$SERVICE_NAME" ]; then
  echo "❗ 사용법: ./init-poetry.sh [디렉토리명] [서비스명]"
  exit 1
fi

cd "$SERVICE_DIR" || exit

echo "📦 $SERVICE_NAME 초기화 중..."

poetry init --name "$SERVICE_NAME" \
  --dependency fastapi \
  --dependency uvicorn \
  --dependency python-jose[cryptography] \
  --dependency pydantic \
  --no-interaction

poetry config virtualenvs.create false --local
poetry install

echo "✅ $SERVICE_NAME 초기화 완료!"
