# =========================================================
# core/bibliometrics.py
# Cálculos bibliométricos y detección de influencia relativa
# =========================================================

import pandas as pd
from datetime import datetime


def compute_citations_per_year(df):
    """
    Calcula las citas por año implementando control técnico 
    para fechas omitidas que evita sesgos e invenciones metodológicas.
    """
    print("📊 Calculando citas por año...")
    current_year = datetime.now().year

    # Marcar registros sin fecha antes de forzar numéricos
    # Asumimos que algo sin 'Year' no puede tratarse limpiamente.
    df["YearMissing"] = df["Year"].isna() | (df["Year"] == "")
    
    df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)
    df["Year_Parsed"] = pd.to_numeric(df["Year"], errors="coerce")
    
    # Actualizar la bandera si al parsear resultó irrecuperable
    df["YearMissing"] = df["YearMissing"] | df["Year_Parsed"].isna() | (df["Year_Parsed"] == 0)

    # Para los válidos, calculamos su edad de exposición
    years_alive = (current_year - df["Year_Parsed"] + 1).clip(lower=1)
    
    # Asignamos nulo (0.00 artificial conservador) para los inválidos
    df["CitasPorAño"] = df["Cited by"] / years_alive
    df.loc[df["YearMissing"], "CitasPorAño"] = 0.0  # Anular impacto

    print(f"✅ Citas procesadas. Omisiones temporales identificadas: {df['YearMissing'].sum()}")
    return df


def detect_seminal(df):
    """
    Detecta artículos con métricas elevadísimas respecto al corpus local.
    Sustituye heurísticas 'Seminales' por 'AltaInfluenciaRelativa'.
    """
    print("🏛️ Evaluando influencia histórica bibliométrica...")

    if "CitasPorAño" not in df.columns:
        df = compute_citations_per_year(df)

    mask_relevance = df["DECISION"].isin(["🔥 ALTA RELEVANCIA", "✅ MEDIA RELEVANCIA"])
    
    if mask_relevance.sum() > 10:
        threshold = df.loc[mask_relevance, "CitasPorAño"].quantile(0.90)
    else:
        threshold = df["CitasPorAño"].quantile(0.90)

    # Identificar Alta Influencia solo cuando supera umbral y POSEE AÑO
    df["AltaInfluenciaRelativa"] = (df["CitasPorAño"] >= threshold) & (~df["YearMissing"])

    print(f"📌 Umbral dinámico evaluado: {round(threshold, 2)} citas/año")
    print(f"⭐ Documentos etiquetados por Alta Influencia Relativa: {df['AltaInfluenciaRelativa'].sum()}")

    # Expurgar la columna transitoria de parseo usada internamente
    df.drop(columns=["Year_Parsed"], inplace=True, errors="ignore")

    return df
