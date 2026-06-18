#!/bin/bash
# Script para cron job do Hermes
# Uso: cron.sh <categoria>
# Exemplo: cron.sh arquitetura
cd "$(dirname "$0")"
CATEGORIA="${1:-ainnews}"
python main.py "$CATEGORIA" 2>&1 >> "logs/cron_$(date +%Y%m%d_%H%M).log"
