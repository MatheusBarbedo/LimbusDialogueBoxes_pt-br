import logging
import re
import time
from dataclasses import dataclass, field

from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)


@dataclass
class DialogueTranslator:
    target_language: str = "pt"
    sleep_seconds: float = 0.05
    tag_regex: re.Pattern = field(default_factory=lambda: re.compile(r"<[^>]+>"))
    cache: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.translator = GoogleTranslator(source="auto", target=self.target_language)

    def _protect_tags(self, text: str) -> tuple[str, list[str]]:
        tags: list[str] = []

        def replace(match: re.Match) -> str:
            index = len(tags)
            tags.append(match.group(0))
            return f"__TAG_{index}__"

        protected_text = self.tag_regex.sub(replace, text)
        return protected_text, tags

    @staticmethod
    def _restore_tags(text: str, tags: list[str]) -> str:
        for index, tag in enumerate(tags):
            text = text.replace(f"__TAG_{index}__", tag)
        return text

    def translate_dialogue(self, text: str, json_path: str) -> str:
        if not isinstance(text, str):
            logger.warning("%s | valor não é string: %r", json_path, text)
            return text

        if not text.strip():
            return text

        if text in self.cache:
            return self.cache[text]

        protected_text, tags = self._protect_tags(text)
        lines = protected_text.split("\n")
        translated_lines: list[str] = []

        for line_index, line in enumerate(lines, start=1):
            if not line.strip():
                translated_lines.append(line)
                continue

            try:
                translated_line = self.translator.translate(line)

                if translated_line is None or not isinstance(translated_line, str):
                    logger.warning(
                        "%s | linha %s retornou inválido | conteúdo: %r",
                        json_path,
                        line_index,
                        line,
                    )
                    translated_line = line

            except Exception:
                logger.exception(
                    "%s | erro ao traduzir linha %s | conteúdo: %r",
                    json_path,
                    line_index,
                    line,
                )
                translated_line = line

            translated_lines.append(translated_line)
            time.sleep(self.sleep_seconds)

        result = "\n".join(translated_lines)
        result = self._restore_tags(result, tags)

        self.cache[text] = result
        return result