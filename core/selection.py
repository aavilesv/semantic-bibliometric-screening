# =========================================================
# core/selection.py
# Rescate desde media relevancia y auditoría PRISMA
# =========================================================

import pandas as pd

def apply_rescue(df, rescue_rate, rescue_min):
    """
    Aplica rescate dinámico inyectando los hiperparámetros.
    """
    print("🔄 Aplicando rescate desde media relevancia...")

    df_high = df[df["DECISION"] == "🔥 ALTA RELEVANCIA"].copy()
    df_mid = df[df["DECISION"] == "✅ MEDIA RELEVANCIA"].copy()

    rescue_n = max(rescue_min, int(len(df_mid) * rescue_rate))

    rescue = (
        df_mid.sort_values("FINAL_SCORE", ascending=False)
        .head(rescue_n)
        .copy()
    )

    df_final = pd.concat([df_high, rescue]).drop_duplicates()
    df["In_lectura"] = df.index.isin(df_final.index)

    print(f"📌 Artículos ALTA relevancia: {len(df_high)}")
    print(f"📌 Artículos MEDIA relevancia: {len(df_mid)}")
    print(f"📌 Artículos rescatados: {len(rescue)}")
    print(f"📚 Total lectura prioritaria: {len(df_final)}")

    return df, df_final


def generate_audit(df, df_final, audit_rate, audit_min, audit_max):
    """
    Genera muestra de auditoría PRISMA inyectando hiperparámetros.
    """
    print("🎲 Generando muestra de auditoría...")

    df_excluded = df[~df["In_lectura"]].copy()

    audit_n = int(len(df_excluded) * audit_rate)
    audit_n = max(audit_min, min(audit_max, audit_n))
    audit_n = min(audit_n, len(df_excluded))

    if audit_n > 0:
        audit_sample = df_excluded.sample(audit_n, random_state=42)
    else:
        audit_sample = df_excluded

    print(f"🧪 Tamaño muestra auditoría: {len(audit_sample)}")

    return audit_sample
