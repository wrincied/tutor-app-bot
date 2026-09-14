"""Translate free-form notify text into the student's bot language."""

from __future__ import annotations

import asyncio
import logging
import os
from functools import lru_cache

logger = logging.getLogger(__name__)

# Bot UI codes → Google Cloud Translate BCP-47-ish codes
_LANG_TO_TRANSLATE: dict[str, str] = {
    "en": "en",
    "de": "de",
    "ru": "ru",
    "uk": "uk",
    "by": "be",
    "kz": "kk",
}


def translate_target(lang: str | None) -> str | None:
    code = (lang or "").strip().lower()
    return _LANG_TO_TRANSLATE.get(code)


@lru_cache(maxsize=1)
def _client():
    from google.cloud import translate_v2 as translate

    project = (os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT") or "").strip()
    if project:
        return translate.Client(project=project)
    return translate.Client()


def _translate_sync(text: str, target: str) -> str:
    result = _client().translate(text, target_language=target, format_="text")
    out = result.get("translatedText") if isinstance(result, dict) else None
    return str(out or text)


async def translate_text(text: str, *, target_lang: str | None) -> str:
    """Translate `text` into bot UI language. On failure returns original text."""
    raw = (text or "").strip()
    if not raw:
        return ""
    if os.environ.get("TRANSLATE_DISABLED", "").strip() == "1":
        return raw
    target = translate_target(target_lang)
    if not target:
        return raw
    try:
        return await asyncio.to_thread(_translate_sync, raw, target)
    except Exception as exc:  # noqa: BLE001 — never block notifications on translate
        logger.warning("translate failed target=%s: %s", target, exc)
        return raw
