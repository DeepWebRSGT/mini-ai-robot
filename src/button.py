"""
Button — GPIO Buton Kontrolü
=============================
6×6mm momenter buton ile bas-konuş modu ve uyandırma.
"""

import logging
import time

logger = logging.getLogger(__name__)

from config import GPIO_PINS


class ButtonController:
    """GPIO buton yönetimi"""

    def __init__(self, pin=None, callback=None):
        self.pin = pin or GPIO_PINS["button"]
        self.callback = callback
        self.last_press = 0
        self.debounce_ms = 200
        self._setup()

    def _setup(self):
        """GPIO pinini yapılandır"""
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Düşen kenarda kesme (butona basınca)
            GPIO.add_event_detect(
                self.pin,
                GPIO.FALLING,
                callback=self._handle_press,
                bouncetime=self.debounce_ms
            )
            logger.info(f"✅ Buton hazır (GPIO{self.pin})")
        except ImportError:
            logger.warning("RPi.GPIO yok, buton simüle ediliyor")
        except RuntimeError as e:
            logger.warning(f"GPIO ayarlanamadı: {e}")

    def _handle_press(self, channel):
        """Butona basılınca çağrılır"""
        now = time.time() * 1000
        if now - self.last_press < self.debounce_ms:
            return
        self.last_press = now

        logger.info("🔘 Butona basıldı!")
        if self.callback:
            self.callback()

    def wait_for_press(self, timeout=None):
        """Butona basılmasını bekle (bloklamalı)"""
        try:
            import RPi.GPIO as GPIO
            if timeout:
                GPIO.wait_for_edge(self.pin, GPIO.FALLING, timeout=timeout)
            else:
                GPIO.wait_for_edge(self.pin, GPIO.FALLING)
            return True
        except (ImportError, RuntimeError):
            # Simülasyon: enter tuşu bekle
            logger.info("Simülasyon: Enter'a bas...")
            try:
                input()
                return True
            except KeyboardInterrupt:
                return False

    def is_pressed(self):
        """Anlık buton durumu"""
        try:
            import RPi.GPIO as GPIO
            return GPIO.input(self.pin) == GPIO.LOW
        except (ImportError, RuntimeError):
            return False

    def cleanup(self):
        """GPIO kaynaklarını temizle"""
        try:
            import RPi.GPIO as GPIO
            GPIO.remove_event_detect(self.pin)
            GPIO.cleanup()
        except (ImportError, RuntimeError):
            pass


class LEDController:
    """Durum LED'i kontrolü"""

    def __init__(self, pin=None):
        self.pin = pin or GPIO_PINS["led_status"]
        self._setup()

    def _setup(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
        except (ImportError, RuntimeError):
            pass

    def on(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.pin, GPIO.HIGH)
        except (ImportError, RuntimeError):
            print("💡 LED ON")

    def off(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.pin, GPIO.LOW)
        except (ImportError, RuntimeError):
            print("💡 LED OFF")

    def blink(self, count=3, interval=0.3):
        """LED yanıp sönsün"""
        import time
        for _ in range(count):
            self.on()
            time.sleep(interval)
            self.off()
            time.sleep(interval)

    def cleanup(self):
        try:
            import RPi.GPIO as GPIO
            self.off()
        except (ImportError, RuntimeError):
            pass


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("🔘 Buton Testi — Bas ve gör...")
    
    led = LEDController()
    led.blink(count=2)
    
    button = ButtonController(callback=lambda: led.blink(count=1))
    print("  Butona bas (Ctrl+C çıkış)")
    
    try:
        button.wait_for_press()
    except KeyboardInterrupt:
        button.cleanup()
        led.cleanup()
    print("✅ Test tamamlandı")
