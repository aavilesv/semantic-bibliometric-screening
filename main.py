# =========================================================
# main.py
# Orquestador del sistema de priorización de afinidad
# =========================================================

import config
from core.io_utils import read_input
from core.text_builder import build_semantic_text
from core.scoring import load_model, compute_scores, classify
from core.methodology import classify_methodology
from core.bibliometrics import compute_citations_per_year, detect_seminal
from core.selection import apply_rescue, generate_audit
from core.export import export_results
import datetime


def main():
    """
    Ejecuta el pipeline de recuperación y prioridad temática vectorial.
    """
    print("=" * 60)
    print("📊 SISTEMA DE PRIORIZACIÓN DE AFINIDAD SEMÁNTICA (RANKING)")
    print("=" * 60)

    meta = {
        "Fecha de Análisis": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Modelo Embedding": config.MODEL_NAME,
        "Target Dataset": config.INPUT_FILE,
        "Foco Temático (Control)": config.TOPIC_TEXT.strip()[:65] + "...",
        "Benchmark High": config.TH_HIGH,
        "Benchmark Mid": config.TH_MID,
        "Benchmark Low": config.TH_LOW,
        "Tasa de Rescate Secundario": config.RESCUE_RATE,
        "Muestra de Auditoría PRISMA": config.AUDIT_RATE
    }

    print("\n📂 Ingiriendo bibliografía base de repositorios...")
    df = read_input(config.INPUT_FILE)

    print("\n📝 Compilando corpus referencial...")
    df = build_semantic_text(df, config.TEXT_COLS)

    model = load_model(config.MODEL_NAME)

    df["FINAL_SCORE"] = 0.0
    df["DECISION"] = "❌ Omisión (Base metadata insuficiente)"
    df["TipoMetodologico"] = "Indeterminado"

    valid_mask = df["isValid"] == True
    
    if valid_mask.sum() > 0:
        scores = compute_scores(model, df.loc[valid_mask, "text_semantic"], config.TOPIC_TEXT)
        
        df.loc[valid_mask, "FINAL_SCORE"] = scores
        
        df.loc[valid_mask, "DECISION"] = df.loc[valid_mask, "FINAL_SCORE"].apply(
            lambda x: classify(x, config.TH_HIGH, config.TH_MID, config.TH_LOW)
        )
        
        print("\n🔬 Compilando heurísticas metodológicas base multicampo...")
        # Pasamos la fila entera mediante df.apply(axis=1) para la versión multi-columna nueva
        df.loc[valid_mask, "TipoMetodologico"] = df.loc[valid_mask].apply(classify_methodology, axis=1)

    print("\n📈 Evaluando métricas de citación en cuarentena local...")
    df = compute_citations_per_year(df)
    df = detect_seminal(df)

    print("\n🔄 Generando sub-sectores de control y rescatística de apoyo...")
    df, df_final = apply_rescue(df, config.RESCUE_RATE, config.RESCUE_MIN)
    audit = generate_audit(df, df_final, config.AUDIT_RATE, config.AUDIT_MIN, config.AUDIT_MAX)

    export_results(df, df_final, audit, config.INPUT_FILE, meta)

    print("\n✅ Tarea finalizada. Matriz de Afinidad lista y validada.")
    print("=" * 60)

if __name__ == "__main__":
    main()
