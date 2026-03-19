import math
from dataclasses import dataclass
from pathlib import Path

from .io_json import append_json_line, append_text_line, reset_file
from .translator_service import DialogueTranslator


@dataclass
class PendingTranslationItem:
    index: int
    item_path: str
    item_id: str | None
    desc: str | None
    original_dlg: str


@dataclass
class IncrementalProcessResult:
    data: dict
    new_ids_count: int
    reused_ids_count: int
    translated_without_id_count: int
    new_ids_log_path: Path
    no_id_items_log_path: Path
    pending_translation_count: int
    batch_count: int


def build_map_by_id(items: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}

    for item in items:
        item_id = item.get("id")

        if isinstance(item_id, str) and item_id.strip():
            result[item_id] = item

    return result


def process_incremental(
    original_data: dict,
    existing_translated_data: dict | None,
    translator: DialogueTranslator,
    logs_dir: Path,
    input_file_name: str,
    batch_size: int,
) -> IncrementalProcessResult:
    file_stem = Path(input_file_name).stem
    new_ids_log_path = logs_dir / f"{file_stem}_novos_ids_traduzidos.txt"
    no_id_items_log_path = logs_dir / f"{file_stem}_itens_sem_id_traduzidos.jsonl"

    reset_file(new_ids_log_path)
    reset_file(no_id_items_log_path)

    original_list = original_data.get("dataList", [])
    existing_list = existing_translated_data.get("dataList", []) if existing_translated_data else []
    existing_map = build_map_by_id(existing_list)

    result_items: list[dict] = []
    pending_items: list[PendingTranslationItem] = []

    new_ids_count = 0
    reused_ids_count = 0
    translated_without_id_count = 0

    for index, original_item in enumerate(original_list):
        item_path = f"root.dataList[{index}]"
        final_item = dict(original_item)
        result_items.append(final_item)

        item_id = original_item.get("id")
        has_valid_id = isinstance(item_id, str) and item_id.strip()

        if not has_valid_id:
            dlg_value = final_item.get("dlg")
            if isinstance(dlg_value, str) and dlg_value.strip():
                pending_items.append(
                    PendingTranslationItem(
                        index=index,
                        item_path=f"{item_path}.dlg",
                        item_id=None,
                        desc=final_item.get("desc"),
                        original_dlg=dlg_value,
                    )
                )
            continue

        existing_item = existing_map.get(item_id)

        if existing_item and isinstance(existing_item.get("dlg"), str):
            final_item["dlg"] = existing_item["dlg"]
            reused_ids_count += 1
            continue

        dlg_value = final_item.get("dlg")
        if isinstance(dlg_value, str) and dlg_value.strip():
            pending_items.append(
                PendingTranslationItem(
                    index=index,
                    item_path=f"{item_path}.dlg",
                    item_id=item_id,
                    desc=final_item.get("desc"),
                    original_dlg=dlg_value,
                )
            )

    total_original_items = len(original_list)
    pending_translation_count = len(pending_items)
    batch_count = math.ceil(pending_translation_count / batch_size) if pending_translation_count > 0 else 0

    print(f"Total de itens no arquivo original: {total_original_items}")
    print(f"Total de itens pendentes para tradução: {pending_translation_count}")
    print(f"Total de ids reaproveitados: {reused_ids_count}")

    if pending_translation_count == 0:
        print("Nenhum item novo para traduzir nesta execução.\n")
    else:
        print(f"Processando em {batch_count} batch(s) de até {batch_size} itens cada.\n")

    for batch_index in range(batch_count):
        start = batch_index * batch_size
        end = min(start + batch_size, pending_translation_count)
        batch_items = pending_items[start:end]

        print(f"[batch {batch_index + 1}/{batch_count}] Traduzindo itens pendentes {start} até {end - 1}...")

        for pending in batch_items:
            translated_dlg = translator.translate_dialogue(pending.original_dlg, pending.item_path)
            result_items[pending.index]["dlg"] = translated_dlg

            if pending.item_id:
                new_ids_count += 1
                append_text_line(new_ids_log_path, pending.item_id)
            else:
                translated_without_id_count += 1
                append_json_line(
                    no_id_items_log_path,
                    {
                        "index": pending.index,
                        "desc": pending.desc,
                        "original_dlg": pending.original_dlg,
                        "translated_dlg": translated_dlg,
                    },
                )

        print(f"   -> batch concluído ({len(batch_items)} itens)\n")

    final_data = dict(original_data)
    final_data["dataList"] = result_items

    return IncrementalProcessResult(
        data=final_data,
        new_ids_count=new_ids_count,
        reused_ids_count=reused_ids_count,
        translated_without_id_count=translated_without_id_count,
        new_ids_log_path=new_ids_log_path,
        no_id_items_log_path=no_id_items_log_path,
        pending_translation_count=pending_translation_count,
        batch_count=batch_count,
    )