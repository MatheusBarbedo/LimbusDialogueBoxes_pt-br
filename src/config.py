from pathlib import Path

INPUT_FILE = "BattleSpeechBubbleDlg.json"
BATCH_SIZE = 200

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGINAL_DIR = BASE_DIR / "original"
TRADUZIDO_DIR = BASE_DIR / "traduzido"
LOGS_DIR = BASE_DIR / "logs"

INPUT_PATH = ORIGINAL_DIR / INPUT_FILE
OUTPUT_PATH = TRADUZIDO_DIR / INPUT_FILE

APP_LOG_PATH = LOGS_DIR / "tradutor.log"