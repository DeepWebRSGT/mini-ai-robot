"""
Display — ILI9341 SPI TFT Ekran Kontrolü
==========================================
2.8" 240×320 TFT'de yüz ifadeleri, metin ve animasyon gösterir.
"""

import logging
import math
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import board
    import digitalio
    import adafruit_rgb_display.ili9341 as ili9341
    DISPLAY_AVAILABLE = True
except ImportError:
    DISPLAY_AVAILABLE = False
    logger.warning("Ekran kütüphanesi kurulu değil. 'pip install adafruit-circuitpython-rgb-display'")

from config import DISPLAY


class RobotFace:
    """Robot yüzü — gözler, ağız, ifadeler"""

    # Yüz ifadeleri (önceden tanımlı)
    EXPRESSIONS = {
        "neutral":   {"eyes": "normal",  "mouth": "line",   "color": 0xFFFFFF},
        "happy":     {"eyes": "closed",  "mouth": "smile",  "color": 0xFFFF00},
        "sad":       {"eyes": "droopy",  "mouth": "frown",  "color": 0x4488FF},
        "angry":     {"eyes": "narrow",  "mouth": "scowl",  "color": 0xFF4444},
        "surprised": {"eyes": "big",     "mouth": "circle", "color": 0xFF8800},
        "thinking":  {"eyes": "squint",  "mouth": "side",   "color": 0x00FF88},
        "sleep":     {"eyes": "closed",  "mouth": "line",   "color": 0x444444},
        "love":      {"eyes": "heart",   "mouth": "smile",  "color": 0xFF66AA},
    }

    def __init__(self):
        self.display = None
        self.width = DISPLAY["width"]
        self.height = DISPLAY["height"]
        self.expression = "neutral"
        self._setup()

    def _setup(self):
        """Ekran bağlantısını kur"""
        if not DISPLAY_AVAILABLE:
            logger.warning("Ekran kullanılamıyor (kütüphane yok)")
            return

        try:
            spi = board.SPI()
            cs = digitalio.DigitalInOut(board.CE0)
            dc = digitalio.DigitalInOut(board.D25)
            rst = digitalio.DigitalInOut(board.D24)

            self.display = ili9341.ILI9341(
                spi, cs=cs, dc=dc, rst=rst,
                baudrate=DISPLAY["spi_frequency"],
            )
            self.display.fill(0)
            logger.info("✅ TFT ekran hazır!")
        except Exception as e:
            logger.warning(f"Ekran başlatılamadı: {e}")
            self.display = None

    def show_face(self, expression="neutral", text=""):
        """Yüz ifadesi göster
        
        Args:
            expression: neutral, happy, sad, angry, surprised, thinking, sleep, love
            text: Alt kısımda gösterilecek yazı
        """
        if not self.display:
            return

        self.expression = expression
        expr = self.EXPRESSIONS.get(expression, self.EXPRESSIONS["neutral"])
        color = expr["color"]

        # Arkaplanı temizle
        self.display.fill(0)

        # Gözler
        if expr["eyes"] == "normal":
            self._draw_eye(70, 100, 15, color)   # Sol göz
            self._draw_eye(170, 100, 15, color)  # Sağ göz
        elif expr["eyes"] == "big":
            self._draw_eye(70, 100, 25, color)
            self._draw_eye(170, 100, 25, color)
        elif expr["eyes"] == "closed":
            self._draw_line(55, 100, 85, 100, color, 3)
            self._draw_line(155, 100, 185, 100, color, 3)
        elif expr["eyes"] == "droopy":
            self._draw_line(55, 115, 85, 100, color, 3)
            self._draw_line(155, 115, 185, 100, color, 3)
        elif expr["eyes"] == "narrow":
            self._draw_line(55, 105, 85, 95, color, 3)
            self._draw_line(155, 105, 185, 95, color, 3)
        elif expr["eyes"] == "heart":
            self._draw_heart(70, 105, 12, 0xFF0000)
            self._draw_heart(170, 105, 12, 0xFF0000)
        elif expr["eyes"] == "squint":
            self._draw_eye(70, 100, 8, color)
            self._draw_eye(170, 100, 8, color)

        # Ağız
        mouth_y = 180
        if expr["mouth"] == "smile":
            self._draw_arc(120, mouth_y, 40, 0, 180, color, 3)
        elif expr["mouth"] == "frown":
            self._draw_arc(120, mouth_y + 20, 40, 180, 360, color, 3)
        elif expr["mouth"] == "circle":
            self._draw_circle(120, mouth_y + 5, 15, color)
        elif expr["mouth"] == "line":
            self._draw_line(90, mouth_y + 5, 150, mouth_y + 5, color, 3)
        elif expr["mouth"] == "scowl":
            self._draw_line(90, mouth_y, 150, mouth_y + 10, color, 3)

        # Yanaklar (mutlu/şaşkın)
        if expression in ("happy", "surprised"):
            self._draw_circle(45, 145, 8, 0xFF8888)
            self._draw_circle(195, 145, 8, 0xFF8888)

        # Metin
        if text:
            self._show_text(text, 120, 250)

    def _draw_eye(self, cx, cy, r, color):
        """Göz çemberi çiz"""
        if not self.display:
            return
        self.display.fill_ellipse(cx, cy, r, r, 0xFFFFFF)
        self.display.fill_ellipse(cx, cy, r - 4, r - 4, color)
        self.display.fill_ellipse(cx, cy, 3, 3, 0x000000)  # Göz bebeği

    def _draw_circle(self, cx, cy, r, color):
        """İçi dolu çember"""
        if not self.display:
            return
        self.display.fill_ellipse(cx, cy, r, r, color)

    def _draw_line(self, x1, y1, x2, y2, color, width=2):
        """Çizgi çiz"""
        if not self.display:
            return
        self.display.line(x1, y1, x2, y2, color)

    def _draw_arc(self, cx, cy, r, start_angle, end_angle, color, width=2):
        """Yay çiz (gülümseme/kaş için)"""
        if not self.display:
            return
        for angle in range(start_angle, end_angle, 5):
            rad = math.radians(angle)
            x = int(cx + r * math.cos(rad))
            y = int(cy + r * math.sin(rad))
            self.display.pixel(x, y, color)

    def _draw_heart(self, cx, cy, size, color):
        """Küçük kalp çiz"""
        if not self.display:
            return
        # Basit kalp (pixel art)
        heart = [
            "..0110..",
            ".011110.",
            "01111110",
            "01111110",
            "01111110",
            ".011110.",
            "..0110..",
        ]
        for dy, row in enumerate(heart):
            for dx, ch in enumerate(row):
                if ch == "1":
                    x = cx - 4 + dx
                    y = cy - 4 + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.display.pixel(x, y, color)

    def _show_text(self, text, x, y):
        """Ekranın altında metin göster"""
        if not self.display:
            return
        # Satır satır göster (20 karakter/satır)
        lines = []
        words = text.split()
        current = ""
        for word in words:
            if len(current + " " + word) > 20:
                lines.append(current)
                current = word
            else:
                current = f"{current} {word}".strip()
        if current:
            lines.append(current)

        start_y = y - (len(lines) * 12) // 2
        for i, line in enumerate(lines[:3]):  # Maks 3 satır
            self.display.text(line, 10, start_y + i * 14, 0xFFFFFF)

    def show_splash(self):
        """Açılış ekranı"""
        if not self.display:
            return
        self.display.fill(0)
        self.display.text("Mini AI Robot", 40, 100, 0x00FF00)
        self.display.text("Laadprogramma...", 50, 140, 0x888888)
        import time
        time.sleep(2)

    def show_volume(self, level):
        """Ses seviyesi çubuğu göster"""
        if not self.display:
            return
        bar_width = int(200 * level)
        self.display.fill_rectangle(20, 300, 200, 10, 0x222222)
        self.display.fill_rectangle(20, 300, bar_width, 10, 0x00FF00)

    def clear(self):
        """Ekranı temizle"""
        if self.display:
            self.display.fill(0)

    def __del__(self):
        if self.display:
            self.display.fill(0)


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("🖥️  Ekran Testi")
    
    face = RobotFace()
    face.show_splash()
    
    import time
    for expr in ["neutral", "happy", "surprised", "thinking", "love", "sad", "angry", "sleep"]:
        print(f"  İfade: {expr}")
        face.show_face(expr, text=f"Dit is {expr}")
        time.sleep(1.5)
    
    print("✅ Test tamamlandı")
