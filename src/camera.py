"""
Camera — Raspberry Pi Kamera Modülü 3
=======================================
Opsiyonel: CSI kamera ile MediaPipe yüz/el tanıma.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import cv2
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe kurulu değil. 'pip install mediapipe opencv-python'")

from config import GPIO_PINS


class CameraVision:
    """Kamera ile yüz/el tanıma"""

    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
        self.face_detection = None
        self.hands = None
        self._setup()

    def _setup(self):
        if not MEDIAPIPE_AVAILABLE:
            logger.info("MediaPipe yok, kamera devre dışı")
            return

        try:
            # Kamera başlat
            self.cap = cv2.VideoCapture(self.camera_id)
            # Pi Camera Module 3 için:
            # CSI kamerayı açmak için libcamera ile çalışır
            # Alternatif: picamera2 kütüphanesi
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            if not self.cap.isOpened():
                logger.warning("Kamera açılamadı")
                self.cap = None
                return

            # MediaPipe yüz detektörü
            self.face_detection = mp.solutions.face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5
            )

            # MediaPipe el detektörü
            self.hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
            )

            logger.info("✅ Kamera + MediaPipe hazır!")

        except Exception as e:
            logger.warning(f"Kamera başlatılamadı: {e}")
            self.cap = None

    def detect_face(self):
        """Yüz algıla, duygu durumu döndür
        
        Returns:
            str: "face_detected", "no_face", veya None
        """
        if not self.cap or not self.face_detection:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb)

        if results.detections:
            return "face_detected"
        return "no_face"

    def detect_gesture(self):
        """El hareketi algıla
        
        Returns:
            str: "wave", "thumbs_up", "point", veya None
        """
        if not self.cap or not self.hands:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None

        # İlk elin durumunu analiz et
        landmarks = results.multi_hand_landmarks[0]
        
        # Basit el hareketi tanıma
        # (Burada daha karmaşık bir model kullanılabilir)
        h, w, _ = frame.shape
        index_tip = landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

        thumb_up = thumb_tip.y < index_tip.y  # Başparmak yukarı
        if thumb_up:
            return "thumbs_up"

        return "wave"

    def handle_gesture(self, gesture):
        """Hareketi robot eylemine çevir"""
        if gesture == "face_detected":
            return "greeting"
        elif gesture == "thumbs_up":
            return "happy"
        elif gesture == "wave":
            return "surprised"
        return None

    def capture_photo(self, path="/tmp/robot_photo.jpg"):
        """Fotoğraf çek ve kaydet"""
        if not self.cap:
            return None

        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(path, frame)
            logger.info(f"📸 Fotoğraf çekildi: {path}")
            return path
        return None

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("📷 Kamera Testi")
    
    cam = CameraVision()
    if cam.cap:
        face = cam.detect_face()
        print(f"  Yüz: {face}")
        gesture = cam.detect_gesture()
        print(f"  Hareket: {gesture}")
        cam.cleanup()
    print("✅ Test tamamlandı")
