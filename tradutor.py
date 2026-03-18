import json
import re
import time
import math
import logging
from pathlib import Path
from deep_translator import GoogleTranslator

INPUT_FILE = "BattleSpeechBubbleDlg.json"
OUTPUT_FILE = "BattleSpeechBubbleDlg_ptbr.json"
TEMP_DIR = "temp"
LOG_FILE = "tradutor.log"
CHUNK_SIZE = 200

TAG_REGEX = re.compile(r"<[^>]+>")
cache = {}

translator = GoogleTranslator(source="auto", target="pt")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


def proteger_tags(texto: str):
    tags = []

    def substituir(match):
        indice = len(tags)
        tags.append(match.group(0))
        return f"__TAG_{indice}__"

    texto_protegido = TAG_REGEX.sub(substituir, texto)
    return texto_protegido, tags


def restaurar_tags(texto: str, tags: list[str]):
    for i, tag in enumerate(tags):
        texto = texto.replace(f"__TAG_{i}__", tag)
    return texto


def traduzir_texto(texto: str, caminho_json: str) -> str:
    if not isinstance(texto, str):
        logging.warning(f"{caminho_json} | valor não é string: {repr(texto)}")
        return texto

    if not texto.strip():
        return texto

    if texto in cache:
        return cache[texto]

    texto_protegido, tags = proteger_tags(texto)
    linhas = texto_protegido.split("\n")
    linhas_traduzidas = []

    for indice_linha, linha in enumerate(linhas, start=1):
        if not linha.strip():
            linhas_traduzidas.append(linha)
            continue

        try:
            linha_traduzida = translator.translate(linha)

            if linha_traduzida is None or not isinstance(linha_traduzida, str):
                logging.warning(
                    f"{caminho_json} | linha {indice_linha} retornou inválido | conteúdo: {repr(linha)}"
                )
                linha_traduzida = linha

        except Exception:
            logging.exception(
                f"{caminho_json} | erro ao traduzir linha {indice_linha} | conteúdo: {repr(linha)}"
            )
            linha_traduzida = linha

        linhas_traduzidas.append(linha_traduzida)
        time.sleep(0.05)

    resultado = "\n".join(linhas_traduzidas)
    resultado = restaurar_tags(resultado, tags)

    cache[texto] = resultado
    return resultado


def traduzir_item(item: dict, caminho_base: str) -> dict:
    novo = dict(item)

    if "dlg" in novo:
        novo["dlg"] = traduzir_texto(novo["dlg"], f"{caminho_base}.dlg")

    return novo


def salvar_json(caminho: Path, dados):
    with caminho.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_json(caminho: Path):
    with caminho.open("r", encoding="utf-8") as f:
        return json.load(f)


def processar_chunks(data_list: list, temp_dir: Path):
    total_itens = len(data_list)
    total_chunks = math.ceil(total_itens / CHUNK_SIZE)

    print(f"Total de itens: {total_itens}")
    print(f"Processando em {total_chunks} chunk(s) de até {CHUNK_SIZE} itens cada.\n")

    for chunk_index in range(total_chunks):
        inicio = chunk_index * CHUNK_SIZE
        fim = min(inicio + CHUNK_SIZE, total_itens)

        chunk_file = temp_dir / f"chunk_{chunk_index + 1:04d}.json"

        if chunk_file.exists():
            print(f"[{chunk_index + 1}/{total_chunks}] Já existe: {chunk_file.name} -> pulando")
            continue

        print(f"[{chunk_index + 1}/{total_chunks}] Traduzindo itens {inicio} até {fim - 1}...")

        chunk_original = data_list[inicio:fim]
        chunk_traduzido = []

        for indice_local, item in enumerate(chunk_original):
            indice_global = inicio + indice_local
            caminho = f"root.dataList[{indice_global}]"
            chunk_traduzido.append(traduzir_item(item, caminho))

            if (indice_local + 1) % 50 == 0:
                print(f"   - {indice_local + 1}/{len(chunk_original)} itens do chunk processados")

        salvar_json(chunk_file, chunk_traduzido)
        print(f"   -> salvo em {chunk_file}\n")


def juntar_chunks(temp_dir: Path, output_file: Path, original_data: dict):
    arquivos_chunk = sorted(temp_dir.glob("chunk_*.json"))

    if not arquivos_chunk:
        raise RuntimeError("Nenhum chunk encontrado na pasta temp.")

    data_list_final = []

    for arquivo in arquivos_chunk:
        chunk_data = carregar_json(arquivo)

        if not isinstance(chunk_data, list):
            raise RuntimeError(f"O arquivo {arquivo.name} não contém uma lista válida.")

        data_list_final.extend(chunk_data)

    resultado_final = dict(original_data)
    resultado_final["dataList"] = data_list_final

    salvar_json(output_file, resultado_final)


def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)
    temp_dir = Path(TEMP_DIR)
    temp_dir.mkdir(exist_ok=True)

    logging.info(f"Iniciando tradução do arquivo: {input_path}")

    dados = carregar_json(input_path)

    if "dataList" not in dados or not isinstance(dados["dataList"], list):
        raise RuntimeError("O JSON não possui 'dataList' no formato esperado.")

    processar_chunks(dados["dataList"], temp_dir)
    juntar_chunks(temp_dir, output_path, dados)

    print("\nConcluído.")
    print(f"Arquivo final: {output_path.resolve()}")
    print(f"Pasta temporária: {temp_dir.resolve()}")
    print(f"Log: {Path(LOG_FILE).resolve()}")


if __name__ == "__main__":
    main()