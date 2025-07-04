#!/usr/bin/env bash

MODEL="phi3:mini-q4_K_M"
LOG_FILE="logs/ollama.log"

if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama is not installed. Please install it from https://ollama.com first." >&2
  exit 1
fi

mkdir -p "$(dirname "$LOG_FILE")"

if ! ollama list | grep -q "$MODEL"; then
  echo "Downloading $MODEL..." | tee -a "$LOG_FILE"
  if ! ollama pull "$MODEL" >>"$LOG_FILE" 2>&1; then
    echo "Failed to download $MODEL. Check $LOG_FILE for details." >&2
    exit 1
  fi
fi

echo "Starting Ollama server on http://localhost:11434/v1 ..." | tee -a "$LOG_FILE"
ollama serve >>"$LOG_FILE" 2>&1 &
PID=$!

# wait up to 10 seconds for the server to respond
for i in {1..10}; do
  if curl -sf http://localhost:11434/v1/models >/dev/null 2>&1; then
    echo "Ollama server started (pid $PID)" | tee -a "$LOG_FILE"
    wait $PID
    exit 0
  fi
  sleep 1
done

echo "Failed to start Ollama server. Check $LOG_FILE for details." >&2
tail -n 20 "$LOG_FILE" >&2
kill $PID 2>/dev/null
exit 1

