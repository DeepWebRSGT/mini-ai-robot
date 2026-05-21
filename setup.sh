#!/bin/bash
# ==========================================
# Mini AI Robot — Kurulum Scripti
# Raspberry Pi OS Bookworm 64-bit için
# ==========================================
set -e

echo "========================================"
echo "🤖 Mini AI Robot Kurulum Başlıyor"
echo "========================================"

# 1. Sistem paketleri
echo ""
echo "[1/6] Sistem paketleri güncelleniyor..."
sudo apt update && sudo apt upgrade -y

echo "[2/6] Gerekli paketler kuruluyor..."
sudo apt install -y \
    python3-pip python3-venv python3-full \
    portaudio19-dev libatlas-base-dev \
    espeak-ng \
    git curl wget unzip \
    i2c-tools

# 2. Python sanal ortamı
echo ""
echo "[3/6] Python sanal ortamı oluşturuluyor..."
cd "$(dirname "$0")"
python3 -m venv robot-env
source robot-env/bin/activate

# 3. Python paketleri
echo ""
echo "[4/6] Python bağımlılıkları kuruluyor..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Ollama (isteğe bağlı, 4GB Pi için)
echo ""
echo "[5/6] Ollama kuruluyor..."
if command -v ollama &> /dev/null; then
    echo "  Ollama zaten kurulu."
else
    curl -fsSL https://ollama.com/install.sh | sh
    sudo systemctl enable ollama
    sudo systemctl start ollama
    echo "  Ollama kuruldu!"
    echo "  Model çekiliyor (qwen2.5:0.5b)..."
    ollama pull qwen2.5:0.5b &
    echo "  Model arka planda indiriliyor (tamamlanması birkaç dakika sürebilir)"
fi

# 5. Modeller
echo ""
echo "[6/6] Ses modelleri indiriliyor..."
bash models/download_models.sh

echo ""
echo "========================================"
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Çalıştırmak için:"
echo "  source robot-env/bin/activate"
echo "  cd src && python main.py"
echo "========================================"
