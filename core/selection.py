# =========================================================
# core/selection.py
# Rescate desde media relevancia y auditoría PRISMA
# =========================================================

from config import RESCUE_RATE, RESCUE_MIN, AUDIT_RATE, AUDIT_MIN, AUDIT_MAX
import pandas as pd

def apply_rescue(df):
    """
    Aplica rescate desde artículos de media relevancia.
    
    Lógica:
    - Los de ALTA pasan directamente.
    - De los de MEDIA se rescata un porcentaje.
    """

    print("🔄 Aplicando rescate desde media relevancia...")

    # Artículos de alta relevancia
    df_high = df[df["DECISION"] == "🔥 ALTA RELEVANCIA"].copy()

    # Artículos de media relevancia
    df_mid = df[df["DECISION"] == "✅ MEDIA RELEVANCIA"].copy()

    # Cantidad a rescatar
    rescue_n = max(RESCUE_MIN, int(len(df_mid) * RESCUE_RATE))

    # Selección de los mejores de MEDIA
    rescue = (
        df_mid.sort_values("FINAL_SCORE", ascending=False)
        .head(rescue_n)
        .copy()
    )

    # Unión: ALTA + rescate
    df_final = pd.concat([df_high, rescue]).drop_duplicates()

    # Marcar artículos seleccionados
    df["In_lectura"] = df.index.isin(df_final.index)

    print(f"📌 Artículos ALTA relevancia: {len(df_high)}")
    print(f"📌 Artículos MEDIA relevancia: {len(df_mid)}")
    print(f"📌 Artículos rescatados: {len(rescue)}")
    print(f"📚 Total lectura prioritaria: {len(df_final)}")

    return df, df_final


def generate_audit(df, df_final):
    """
    Genera muestra aleatoria de artículos descartados
    para auditoría PRISMA.
    """

    print("🎲 Generando muestra de auditoría...")

    # Artículos no seleccionados para lectura
    df_excluded = df[~df["In_lectura"]].copy()

    # Tamaño de auditoría
    audit_n = int(len(df_excluded) * AUDIT_RATE)

    # Ajuste entre mínimo y máximo
    audit_n = max(AUDIT_MIN, min(AUDIT_MAX, audit_n))
    audit_n = min(audit_n, len(df_excluded))

    # Muestra aleatoria
    if audit_n > 0:
        audit_sample = df_excluded.sample(audit_n, random_state=42)
    else:
        audit_sample = df_excluded

    print(f"🧪 Tamaño muestra auditoría: {len(audit_sample)}")

    return audit_sample
