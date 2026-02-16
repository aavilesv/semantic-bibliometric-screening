# =========================================================
# core/scoring.py
# Clasificación semántica con SBERT
# =========================================================

import numpy as np                              # Operaciones numéricas
from sentence_transformers import SentenceTransformer, util  # SBERT
from config import MODEL_NAME, TH_HIGH, TH_MID, TH_LOW, TOPIC_TEXT


def load_model():
    """
    Carga el modelo SBERT definido en config.py.
    """
    print("⏳ Cargando modelo semántico SBERT...")
    model = SentenceTransformer(MODEL_NAME)
    print("✅ Modelo cargado correctamente.")
    return model


def normalize(scores):
    """
    Normaliza los scores entre 0 y 1.
    Evita división por cero si todos los scores son iguales.
    """

    smin = scores.min()     # Valor mínimo
    smax = scores.max()     # Valor máximo

    # Si todos los scores son iguales
    if smax == smin:
        return np.zeros_like(scores)

    # Normalización min-max
    return (scores - smin) / (smax - smin)


def compute_scores(model, texts):
    """
    Calcula la similitud semántica entre cada artículo
    y el texto del tema.
    """

    print("🧠 Calculando similitud semántica...")

    # Embedding del texto del tema
    ref_embedding = model.encode(
        TOPIC_TEXT,
        convert_to_tensor=True
    )

    # Embeddings de los artículos
    article_embeddings = model.encode(
        texts.tolist(),
        convert_to_tensor=True,
        show_progress_bar=True
    )

    # Cálculo de similitud coseno
    raw_scores = util.cos_sim(
        article_embeddings,
        ref_embedding
    ).cpu().numpy().flatten()

    # Normalización de scores
    norm_scores = normalize(raw_scores)

    print("✅ Similitud semántica calculada.")

    return norm_scores


def classify(score):
    """
    Clasifica un artículo según su score semántico.
    """

    # Alta relevancia
    if score >= TH_HIGH:
        return "🔥 ALTA RELEVANCIA"

    # Media relevancia
    if score >= TH_MID:
        return "✅ MEDIA RELEVANCIA"

    # Baja relevancia
    if score >= TH_LOW:
        return "⚠️ BAJA RELEVANCIA"

    # Descartado
    return "❌ DESCARTAR"
