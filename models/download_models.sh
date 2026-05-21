#!/bin/bash
# ==========================================
# AI Modellerini İndir
# ==========================================
set -e

MODELS_DIR="$(dirname "$0")"
cd "$MODELS_DIR"

echo "========================================"
echo "📥 AI Modelleri İndiriliyor"
echo "========================================"

# 1. Vosk STT Modeli (Hollandaca)
echo ""
echo "[1/3] Vosk STT modeli (Hollandaca)..."
if [ -d "vosk-model-small-nl-0.22" ]; then
    echo "  ✓ Zaten mevcut"
else
    wget -O vosk-model-small-nl-0.22.zip \
        https://alphacephei.com/vosk/models/vosk-model-small-nl-0.22.zip
    unzip vosk-model-small-nl-0.22.zip
    rm vosk-model-small-nl-0.22.zip
    echo "  ✓ İndirildi (~42 MB)"
fi

# 2. Piper TTS Modeli (Hollandaca kadın ses)
echo ""
echo "[2/3] Piper TTS modeli (Hollandaca)..."
if [ -f "nl_NL-glow-tts-medium.onnx" ]; then
    echo "  ✓ Zaten mevcut"
else
    wget -O nl_NL-glow-tts-medium.onnx \
        https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/glow-tts/medium/nl_NL-glow-tts-medium.onnx
    wget -O nl_NL-glow-tts-medium.onnx.json \
        https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/glow-tts/medium/nl_NL-glow-tts-medium.onnx.json
    echo "  ✓ İndirildi (~63 MB)"
fi

# 3. Ollama LLM Modeli (isteğe bağlı)
echo ""
echo "[3/3] Ollama LLM modeli (opsiyonel)..."
if command -v ollama &> /dev/null; then
    if ollama list | grep -q "qwen2.5:0.5b"; then
        echo "  ✓ Zaten mevcut"
    else
        echo "  İndiriliyor (arka planda)..."
        ollama pull qwen2.5:0.5b &
        echo "  PID: $!"
    fi
else
    echo "  ⚠️  Ollama kurulu değil. LLM kullanmak için: curl -fsSL https://ollama.com/install.sh | sh"
fi

echo ""
echo "========================================"
echo "✅ Tüm modeller indirildi!"
echo ""
echo "Toplam boyut: ~105 MB (Vosk + Piper)"
echo "             + ~400 MB (Ollama Qwen 2.5 0.5B)"
echo "========================================"
