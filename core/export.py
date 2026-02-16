# =========================================================
# core/export.py
# Exportación de resultados a Excel y CSV
# =========================================================

import pandas as pd
from pathlib import Path
from config import INPUT_FILE


def export_results(df, df_final, audit):
    """
    Exporta los resultados del clasificador.
    
    Genera:
    - Excel con varias hojas.
    - CSV con todos los artículos clasificados.
    """

    print("💾 Exportando resultados...")

    # =========================
    # RUTAS DE SALIDA
    # =========================

    # Ruta del archivo de entrada
    input_path = Path(INPUT_FILE)

    # Carpeta donde se guardarán los resultados
    output_dir = input_path.parent

    # Archivos de salida
    excel_path = output_dir / "RESULTADO_MODULAR.xlsx"
    csv_path = output_dir / "TODOS_CLASIFICADOS.csv"

    # =========================
    # ORDENAR RESULTADOS
    # =========================

    # Ordena todos los artículos:
    # Primero los seleccionados para lectura,
    # luego por score descendente
    df_all_sorted = df.sort_values(
        ["In_lectura", "FINAL_SCORE"],
        ascending=[False, False]
    )

    # Ordena los artículos de lectura prioritaria
    df_final_sorted = df_final.sort_values(
        "FINAL_SCORE",
        ascending=False
    )

    # =========================
    # EXPORTACIÓN A EXCEL
    # =========================

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

        # Hoja 1: Todos los artículos clasificados
        df_all_sorted.to_excel(
            writer,
            sheet_name="0_TODOS_CLASIFICADOS",
            index=False
        )

        # Hoja 2: Lectura prioritaria
        df_final_sorted.to_excel(
            writer,
            sheet_name="1_LECTURA_PRIORITARIA",
            index=False
        )

        # Hoja 3: Auditoría PRISMA
        audit.to_excel(
            writer,
            sheet_name="2_AUDITORIA",
            index=False
        )

        # Hoja 4: Estadísticas de clasificación
        stats = df["DECISION"].value_counts().to_frame("Total")
        stats.to_excel(
            writer,
            sheet_name="STATS"
        )

    # =========================
    # EXPORTACIÓN CSV
    # =========================

    df_all_sorted.to_csv(
        csv_path,
        index=False,
        encoding="utf-8"
    )

    print(f"✅ Excel generado: {excel_path}")
    print(f"✅ CSV generado:   {csv_path}")
