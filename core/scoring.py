# =========================================================
# core/scoring.py
# Clasificación semántica con SBERT
# =========================================================

import numpy as np
from sentence_transformers import SentenceTransformer, util


def load_model(model_name):
    """
    Carga el modelo SBERT inyectado.
    """
    print(f"⏳ Cargando modelo semántico SBERT ({model_name})...")
    model = SentenceTransformer(model_name)
    print("✅ Modelo cargado correctamente.")
    return model


def compute_scores(model, texts, topic_text):
    """
    Calcula la similitud semántica entre cada artículo y el texto del tema.
    """
    print("🧠 Calculando similitud semántica (Coseno real)...")

    ref_embedding = model.encode(
        topic_text,
        convert_to_tensor=True
    )

    article_embeddings = model.encode(
        texts.tolist(),
        convert_to_tensor=True,
        show_progress_bar=True,
        batch_size=64  # Control de OOM
    )

    raw_scores = util.cos_sim(
        article_embeddings,
        ref_embedding
    ).cpu().numpy().flatten()

    print("✅ Similitud semántica calculada (Coseno crudo).")

    return raw_scores


def classify(score, th_high, th_mid, th_low):
    """
    Clasifica un artículo según su score semántico en bruto y umbrales inyectados.
    """
    if score >= th_high:
        return "🔥 ALTA RELEVANCIA"
    if score >= th_mid:
        return "✅ MEDIA RELEVANCIA"
    if score >= th_low:
        return "⚠️ BAJA RELEVANCIA"
    return "❌ DESCARTAR"
