#!/bin/bash

# --- 1. Master Süreçlerini Başlat ---
echo "Master süreçleri başlatılıyor..."

# Master dosyaları src/master altındaysa:
python src/master/master_asssemble.py > master_assemble.log 2>&1 &
python src/master/master_shred.py > master_shred.log 2>&1 &

sleep 1 # Master'ların ayağa kalkması için kısa bir bekleme

# --- 2. Worker Süreçlerini Başlat ---
TARGET_DIR="src/worker"
cd "$TARGET_DIR" || { echo "Hata: $TARGET_DIR dizini bulunamadı!"; exit 1; }

# SET A (Port 7000-7004)
for i in {0..4}
do
    PORT=$((7000 + i))
    ENV_FILE=".worker_env$((i + 1))_a"
    echo "Başlatılıyor (Set A): Port $PORT, Env: $ENV_FILE"
    python ./worker_main.py --port $PORT --env "$ENV_FILE" > "worker_$PORT.log" 2>&1 &
done

# SET S (Port 8000-8004)
for i in {0..4}
do
    PORT=$((8000 + i))
    ENV_FILE=".worker_env$((i + 1))_s"
    echo "Başlatılıyor (Set S): Port $PORT, Env: $ENV_FILE"
    python ./worker_main.py --port $PORT --env "$ENV_FILE" > "worker_$PORT.log" 2>&1 &
done

echo "Tüm sistem (2 Master + 10 Worker) başlatıldı."