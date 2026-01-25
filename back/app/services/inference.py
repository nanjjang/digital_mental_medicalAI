from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

LABELS = ["normal", "depression", "suicide", "anxiety"]


def _is_emoji(char: str) -> bool:
    return (
        "\U0001F300" <= char <= "\U0001FAFF"
        or "\U0001F1E6" <= char <= "\U0001F1FF"
        or "\U00002600" <= char <= "\U000026FF"
        or "\U00002700" <= char <= "\U000027BF"
    )


def _calc_features(text: str) -> np.ndarray:
    length = len(text)
    if length == 0:
        return np.zeros((1, 3), dtype=np.float32)
    special_count = sum(1 for ch in text if not ch.isalnum() and not ch.isspace())
    emoji_count = sum(1 for ch in text if _is_emoji(ch))
    special_ratio = special_count / length
    emoji_ratio = emoji_count / length
    return np.array([[float(length), float(special_ratio), float(emoji_ratio)]], dtype=np.float32)


def _resolve_model_path() -> Path:
    env_path = os.getenv("MODEL_PATH")
    if env_path:
        return Path(env_path)
    base = Path(__file__).resolve().parents[1] / "models"
    int8_path = base / "model.int8.onnx"
    if int8_path.exists():
        return int8_path
    full_path = base / "model.onnx"
    if full_path.exists():
        return full_path
    raise FileNotFoundError("ONNX model not found in app/models")


def _infer_max_length(inputs: list[ort.NodeArg]) -> int:
    for node in inputs:
        if "input_ids" in node.name:
            shape = node.shape or []
            for dim in shape:
                if isinstance(dim, int) and dim > 0:
                    return dim
    return 128


@dataclass
class InferenceResult:
    label: str
    scores: dict[str, float]


class ModelRunner:
    def __init__(self) -> None:
        self.model_path = _resolve_model_path()
        self.session = ort.InferenceSession(str(self.model_path), providers=["CPUExecutionProvider"])
        self.inputs = self.session.get_inputs()
        self.max_length = _infer_max_length(self.inputs)
        tokenizer_name = os.getenv("TOKENIZER_NAME", "roberta-base")
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def _build_inputs(self, text: str) -> dict[str, np.ndarray]:
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="np",
        )
        feed: dict[str, np.ndarray] = {}
        for node in self.inputs:
            name = node.name
            if "input_ids" in name:
                feed[name] = encoding["input_ids"]
            elif "attention_mask" in name:
                feed[name] = encoding["attention_mask"]
            elif "token_type_ids" in name:
                feed[name] = np.zeros_like(encoding["input_ids"])
            else:
                feed[name] = _calc_features(text)
        return feed

    def predict(self, text: str) -> InferenceResult:
        feed = self._build_inputs(text)
        outputs = self.session.run(None, feed)
        logits = outputs[0]
        logits = logits.astype(np.float32)
        exps = np.exp(logits - np.max(logits))
        probs = (exps / np.sum(exps)).reshape(-1)
        scores = {label: float(probs[idx]) for idx, label in enumerate(LABELS)}
        label = LABELS[int(np.argmax(probs))]
        return InferenceResult(label=label, scores=scores)


@lru_cache(maxsize=1)
def get_model_runner() -> ModelRunner:
    return ModelRunner()
