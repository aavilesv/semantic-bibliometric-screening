# =========================================================
# core/methodology.py
# Clasificación metodológica de artículos
# =========================================================

def classify_methodology(text):
    """
    Clasifica el tipo metodológico de un artículo
    basándose en el abstract.
    
    Posibles salidas:
    - Empírico
    - Teórico
    - Review
    - Indeterminado
    """

    # Si el texto no es válido
    if not isinstance(text, str):
        return "Indeterminado"

    # Convertir a minúsculas para comparación
    t = text.lower()

    # =========================
    # DETECCIÓN DE REVIEWS
    # =========================

    # Palabras clave típicas de revisiones
    review_terms = [
        "systematic review",
        "literature review",
        "meta-analysis",
        "bibliometric analysis",
        "state of the art"
    ]

    if any(term in t for term in review_terms):
        return "Review"

    # =========================
    # DETECCIÓN DE ESTUDIOS EMPÍRICOS
    # =========================

    empirical_terms = [
        "experiment",
        "experimental",
        "survey",
        "questionnaire",
        "regression",
        "dataset",
        "sample",
        "empirical",
        "statistical analysis",
        "panel data",
        "case study"
    ]

    if any(term in t for term in empirical_terms):
        return "Empírico"

    # =========================
    # DETECCIÓN DE ESTUDIOS TEÓRICOS
    # =========================

    theoretical_terms = [
        "conceptual framework",
        "theoretical framework",
        "conceptual model",
        "theoretical model",
        "proposes a model",
        "conceptual analysis",
        "theoretical perspective",
        "proposes a framework"
    ]

    if any(term in t for term in theoretical_terms):
        return "Teórico"

    # =========================
    # SI NO SE DETECTA NADA
    # =========================

    return "Indeterminado"
