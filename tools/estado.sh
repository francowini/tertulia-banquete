#!/bin/sh
curl -sf -H "X-Team-Code: $1" https://api.tertulia.ai/equipo | python3 -I "$(dirname "$0")/estado.py"
