#!/bin/sh
set -eu

OLLAMA_HOST="${OLLAMA_HOST:-http://ollama:11434}"
OLLAMA_CHAT_MODEL="${OLLAMA_CHAT_MODEL:-qwen3.5:9b-q4_K_M}"
OLLAMA_EMBED_MODEL="${OLLAMA_EMBED_MODEL:-bge-m3}"

echo "Waiting for Ollama at ${OLLAMA_HOST}..."
until ollama list >/dev/null 2>&1; do
  sleep 3
done

echo "Pulling chat model: ${OLLAMA_CHAT_MODEL}"
ollama pull "${OLLAMA_CHAT_MODEL}"

echo "Pulling embedding model: ${OLLAMA_EMBED_MODEL}"
ollama pull "${OLLAMA_EMBED_MODEL}"

echo "Ollama model initialization complete."
