# =========================================================
# core/bibliometrics.py
# Cálculos bibliométricos y detección de artículos seminales
# =========================================================

import pandas as pd
from datetime import datetime


def compute_citations_per_year(df):
    """
    Calcula las citas por año para cada artículo de manera protegida.
    """
    print("📊 Calculando citas por año...")
    current_year = datetime.now().year

    df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(current_year)

    years_alive = (current_year - df["Year"] + 1).clip(lower=1)
    df["CitasPorAño"] = df["Cited by"] / years_alive

    print("✅ Citas por año calculadas y sanitizadas.")
    return df


def detect_seminal(df):
    """
    Detecta artículos seminales basándose en el percentil alto
    exclusivo de los documentos que sí son relevantes.
    """
    print("🏛️ Detectando artículos seminales...")

    if "CitasPorAño" not in df.columns:
        df = compute_citations_per_year(df)

    # Filtrar basura para que la media no sea destruida artificialmente
    mask_relevance = df["DECISION"].isin(["🔥 ALTA RELEVANCIA", "✅ MEDIA RELEVANCIA"])
    
    if mask_relevance.sum() > 10:
        threshold = df.loc[mask_relevance, "CitasPorAño"].quantile(0.90)
    else:
        # Fallback si no hay suficientes artículos válidos
        threshold = df["CitasPorAño"].quantile(0.90)

    # El umbral ahora es matemáticamente riguroso
    df["EsSeminal"] = df["CitasPorAño"] >= threshold

    print(f"📌 Umbral dinámico recalibrado de seminalidad: {round(threshold, 2)} citas/año")
    print(f"⭐ Artículos seminales detectados: {df['EsSeminal'].sum()}")

    return df
