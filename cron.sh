#!/bin/bash
# Script para cron job do Hermes
# Posta automaticamente no Instagram
cd "$(dirname "$0")"
python main.py 2>&1 >> "logs/cron_$(date +%Y%m%d).log"
