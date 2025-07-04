#!/usr/bin/env bash

MODEL="phi3:mini-q4_K_M"

if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama is not installed. Please install it from https://ollama.com first." >&2
  exit 1
fi

if ! ollama list | grep -q "$MODEL"; then
  echo "Downloading $MODEL..."
  ollama pull "$MODEL"
fi

echo "Starting Ollama server on http://localhost:11434/v1 ..."
exec ollama serve

