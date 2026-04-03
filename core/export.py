# =========================================================
# core/export.py
# Exportación de resultados a Excel y CSV
# =========================================================

import pandas as pd
from pathlib import Path
import datetime


def reorder_columns(df):
    priority_cols = [
        "Title", "DECISION", "FINAL_SCORE", "TipoMetodologico", 
        "EsSeminal", "CitasPorAño", "Year", "Cited by", "In_lectura", "bothkeywords"
    ]
    existing_priority = [col for col in priority_cols if col in df.columns]
    skip_cols = ["isValid", "text_semantic", "score_semantic"]
    other_cols = [col for col in df.columns if col not in existing_priority and col not in skip_cols]
    final_order = existing_priority + other_cols + [c for c in skip_cols if c in df.columns]
    
    return df[final_order]


def export_results(df, df_final, audit, input_file, config_meta=None):
    """
    Exporta los resultados a Excel adjuntando configuración metodológica.
    """
    print("💾 Estructurando y exportando resultados...")

    input_path = Path(input_file)
    output_dir = input_path.parent
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    excel_path = output_dir / f"RESULTADO_MODULAR_{timestamp}.xlsx"
    csv_path = output_dir / f"TODOS_CLASIFICADOS_{timestamp}.csv"

    df = reorder_columns(df)
    df_final = reorder_columns(df_final)
    audit = reorder_columns(audit)

    df_all_sorted = df.sort_values(["In_lectura", "FINAL_SCORE"], ascending=[False, False])
    df_final_sorted = df_final.sort_values("FINAL_SCORE", ascending=False)

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_all_sorted.to_excel(writer, sheet_name="0_TODOS_CLASIFICADOS", index=False)
        df_final_sorted.to_excel(writer, sheet_name="1_LECTURA_PRIORITARIA", index=False)
        audit.to_excel(writer, sheet_name="2_AUDITORIA", index=False)

        stats = df["DECISION"].value_counts().to_frame("Total")
        stats.to_excel(writer, sheet_name="STATS")

        if config_meta is not None:
            df_meta = pd.DataFrame(list(config_meta.items()), columns=["Parametro", "Valor"])
            df_meta.to_excel(writer, sheet_name="3_METADATA", index=False)

    df_all_sorted.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"✅ Excel generado: {excel_path}")
    print(f"✅ CSV generado:   {csv_path}")
