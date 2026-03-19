import logging

from .config import (
    APP_LOG_PATH,
    BATCH_SIZE,
    INPUT_FILE,
    INPUT_PATH,
    LOGS_DIR,
    ORIGINAL_DIR,
    OUTPUT_PATH,
    TRADUZIDO_DIR,
)
from .incremental_service import process_incremental
from .io_json import ensure_directories, load_json, save_json
from .translator_service import DialogueTranslator


def configure_logging() -> None:
    logging.basicConfig(
        filename=APP_LOG_PATH,
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        encoding="utf-8",
    )


def main() -> None:
    ensure_directories(ORIGINAL_DIR, TRADUZIDO_DIR, LOGS_DIR)
    configure_logging()

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Arquivo original não encontrado: {INPUT_PATH}")

    original_data = load_json(INPUT_PATH)

    if "dataList" not in original_data or not isinstance(original_data["dataList"], list):
        raise RuntimeError("O JSON original não possui 'dataList' no formato esperado.")

    existing_translated_data = None
    if OUTPUT_PATH.exists():
        existing_translated_data = load_json(OUTPUT_PATH)

    translator = DialogueTranslator()

    result = process_incremental(
        original_data=original_data,
        existing_translated_data=existing_translated_data,
        translator=translator,
        logs_dir=LOGS_DIR,
        input_file_name=INPUT_FILE,
        batch_size=BATCH_SIZE,
    )

    save_json(OUTPUT_PATH, result.data)

    print("Concluído.")
    print(f"Arquivo final: {OUTPUT_PATH.resolve()}")
    print(f"Novos ids traduzidos: {result.new_ids_count}")
    print(f"Ids reaproveitados: {result.reused_ids_count}")
    print(f"Itens sem id traduzidos diretamente: {result.translated_without_id_count}")
    print(f"Batch(s) executados: {result.batch_count}")
    print(f"Log principal: {APP_LOG_PATH.resolve()}")
    print(f"Log de novos ids: {result.new_ids_log_path.resolve()}")
    print(f"Log de itens sem id: {result.no_id_items_log_path.resolve()}")