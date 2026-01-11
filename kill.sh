#!/bin/bash

echo "Tüm sistem durduruluyor..."

# Hem worker hem master dosyalarını hedef al
pkill -15 -f "worker_main.py"
pkill -15 -f "master_asssemble.py"
pkill -15 -f "master_shred.py"

echo "Kapatma komutu gönderildi."