import time
import webbrowser
import numpy as np
import pyaudio
from datetime import datetime
import logging
import sys
import threading
from collections import deque

# ======== SETTINGS ========
GAME_ID             = 570     # Steam game ID (e.g. Dota 2 = 570, WPE = 431960)
SAMPLING_RATE       = 22050   # Microphone sampling rate in Hz
FRAME_DURATION      = 0.05    # Duration of one audio frame in seconds
FRAME_SIZE          = int(SAMPLING_RATE * FRAME_DURATION)  # Number of samples per frame
AMPLITUDE_THRESHOLD = 0.1     # Amplitude threshold to detect a clap
MIN_PEAK_INTERVAL   = 0.2     # Minimum interval between detected peaks in seconds
CLAP_WINDOW         = 1.5     # Time window after first clap to detect second clap in seconds
PRE_SILENCE         = 2.0     # Required silence before the first clap in seconds
RESET_PAUSE         = 0.1     # Pause after trigger or reset in seconds

TEST_MODE           = 0       # 1 = test mode (does not actually launch the game)
LOGGING_ENABLED     = 0       # 1 = enable console logging, 0 = disable logging

# ======== LOGGING SETUP ========
if LOGGING_ENABLED:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
else:
    logging.basicConfig(level=logging.CRITICAL + 1)
logger = logging.getLogger(__name__)

class ExactTwoClapDetector:
    def __init__(self):
        # EMA coefficient for quick volume filtering
        self.ema_alpha = 0.2
        self.ema_prev = 0.0

        # State machine variables
        self.state = 'IDLE'
        self.t1 = None
        self.last_any = time.time()
        self.last_peak = 0.0

        # Queue to store detected clap timestamps
        self.clap_times = deque()
        self.lock = threading.Lock()

        # Initialize PyAudio in callback mode
        pa = pyaudio.PyAudio()
        try:
            self.stream = pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLING_RATE,
                input=True,
                frames_per_buffer=FRAME_SIZE,
                stream_callback=self._callback
            )
        except Exception as e:
            logger.error(f"Failed to open audio stream: {e}")
            sys.exit(1)

    def _callback(self, in_data, frame_count, time_info, status):
        # Simple volume filtering using exponential moving average
        audio = np.frombuffer(in_data, np.int16).astype(np.float32) / 32768.0
        mag = np.mean(np.abs(audio))
        self.ema_prev = self.ema_alpha * mag + (1 - self.ema_alpha) * self.ema_prev

        # Skip processing if the volume is very low
        if self.ema_prev < AMPLITUDE_THRESHOLD * 0.5:
            return (None, pyaudio.paContinue)

        # Detect a peak in the current frame
        peak = np.max(np.abs(audio))
        now = time.time()
        if peak >= AMPLITUDE_THRESHOLD and now - self.last_peak >= MIN_PEAK_INTERVAL:
            self.last_peak = now
            # Record the clap event
            with self.lock:
                self.clap_times.append(now)

        return (None, pyaudio.paContinue)

    def _process_clap(self, now):
        """Process a single clap event through the state machine."""
        if self.state == 'IDLE':
            # First clap after required silence
            if now - self.last_any >= PRE_SILENCE:
                self.t1 = now
                self.state = 'FIRST'
                logger.info(f"First clap detected — starting {CLAP_WINDOW}s window")
            self.last_any = now

        elif self.state == 'FIRST':
            # Second clap within the time window
            if now - self.t1 <= CLAP_WINDOW:
                self.state = 'VERIFY'
                logger.info("Second clap detected — verifying no extra claps")
            else:
                # If window expired, treat this clap as the new first clap
                logger.info("Window expired — treating as first clap")
                self.t1 = now
                self.state = 'FIRST'
                logger.info(f"First clap detected — starting {CLAP_WINDOW}s window")
            self.last_any = now

        elif self.state == 'VERIFY':
            # Any extra clap before window ends triggers a reset
            if now - self.t1 < CLAP_WINDOW:
                logger.info("Extra clap detected — resetting")
                time.sleep(RESET_PAUSE)
                self._reset(now)

    def _reset(self, now):
        self.state = 'IDLE'
        self.last_any = now

    def run(self):
        logger.info("Waiting for exactly two claps after silence…")
        self.stream.start_stream()

        try:
            while self.stream.is_active():
                time.sleep(FRAME_DURATION / 2)
                now = time.time()

                # 1) Handle all queued clap events
                with self.lock:
                    while self.clap_times:
                        clap_t = self.clap_times.popleft()
                        self._process_clap(clap_t)

                # 2) Handle timeouts
                if self.state == 'FIRST' and now - self.t1 > CLAP_WINDOW:
                    logger.info("Second clap not detected in time — resetting")
                    time.sleep(RESET_PAUSE)
                    self._reset(now)

                elif self.state == 'VERIFY' and now - self.t1 >= CLAP_WINDOW:
                    logger.info("Success! Exactly two claps detected — launching game")
                    if not TEST_MODE:
                        webbrowser.open(f"steam://rungameid/{GAME_ID}")
                    time.sleep(RESET_PAUSE)
                    self._reset(now)

        except KeyboardInterrupt:
            logger.info("Interrupted by user (Ctrl+C) — exiting.")
        finally:
            self.stream.stop_stream()
            self.stream.close()

if __name__ == '__main__':
    ExactTwoClapDetector().run()
