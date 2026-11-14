#!/bin/sh
# Uso: tools/enviar.sh TRT-XXXX NIVEL -> igual que "Enviar a Aristóteles" (evalúa último commit de main)
curl -s -X POST -H "X-Team-Code: $1" -H "Content-Type: application/json" \
  -d "{\"repo\":\"https://github.com/francowini/tertulia-banquete\",\"nivel\":$2}" https://api.tertulia.ai/entregas; echo
