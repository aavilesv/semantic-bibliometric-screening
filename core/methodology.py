# =========================================================
# core/methodology.py
# Clasificación metodológica heurística de artículos
# =========================================================

def classify_methodology(row):
    """
    Infiere el tipo metodológico evaluando acumulativamente múltiples columnas.
    Actúa como capa heurística descriptiva, no como clasificación absoluta.
    """
    
    # Consolidar campos de evaluación
    title = str(row.get("Title", "")).lower()
    abstract = str(row.get("Abstract", "")).lower()
    keywords = str(row.get("bothkeywords", "")).lower()
    
    # Si todo carece de texto, es indeterminado por omisión
    if not title and not abstract and not keywords:
        return "Indeterminado"

    text = f"{title} {abstract} {keywords}"
    
    # Contadores de categoría
    scores = {
        "Review": 0,
        "Empírico": 0,
        "Teórico": 0
    }

    # =========================
    # DETECCIÓN DE REVIEWS
    # =========================
    review_terms = [
        "systematic review", "literature review", "meta-analysis",
        "meta analysis", "bibliometric", "state of the art", 
        "scoping review", "narrative review"
    ]
    scores["Review"] += sum(1 for term in review_terms if term in text)

    # =========================
    # DETECCIÓN DE ESTUDIOS EMPÍRICOS
    # =========================
    empirical_terms = [
        "experiment", "survey", "questionnaire", "regression", "dataset", 
        "sample", "empirical", "statistical analysis", "panel data", 
        "case study", "quantitative", "qualitative", "interview", "participants"
    ]
    scores["Empírico"] += sum(1 for term in empirical_terms if term in text)

    # =========================
    # DETECCIÓN DE ESTUDIOS TEÓRICOS
    # =========================
    theoretical_terms = [
        "conceptual framework", "theoretical framework", "conceptual model", 
        "theoretical model", "proposes a model", "conceptual analysis", 
        "theoretical perspective", "proposes a framework", "theory building"
    ]
    scores["Teórico"] += sum(1 for term in theoretical_terms if term in text)

    # =========================
    # LÓGICA DE ASIGNACIÓN
    # =========================
    
    # 1. Si destaca claramente una categoría, se asigna.
    # 2. Si predominan y empatan Empírico y Teórico, es Mixto.
    # 3. Si gana Review y Empírico, usualmente predomina Review (Meta-análisis), pero depende del usuario.
    
    max_score = max(scores.values())
    
    if max_score == 0:
        return "Indeterminado"

    # Buscar categorías que empatan en la posición líder
    top_categories = [k for k, v in scores.items() if v == max_score]
    
    if len(top_categories) == 1:
        return top_categories[0]
        
    if "Empírico" in top_categories and "Teórico" in top_categories:
        return "Mixto"
        
    if "Review" in top_categories:
        return "Review" # Meta-análisis empírico tiene fuerte corte de Review

    return "Indeterminado"
