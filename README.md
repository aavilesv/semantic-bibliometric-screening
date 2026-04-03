# Sistema Rankeador de Afinidad Semántica SBERT

## Descripción general
Este sistema funciona de manera eficiente y rastreable como un modelo inmersivo de **priorización y recuperación temática asistida** para registros científicos de Scopus/Web of Science. 
No actúa como clasificador rígido o decisor binario, sino como un tabulador algorítmico continuo. Su objetivo principal es encontrar la mayor correlación semántica cruzada entre el corpus y tu tema ancla.

## Principios Teóricos
El sistema asienta su arquitectura en "Dense Retrieval" bajo modelos orientados SBERT:
- **Ponderación Jerárquica Textual:** Inyección contextual de directivas que priman la lectura de los campos `Title` e `Index/Author Keywords` íntegros compuestos, en lugar de diluirlos dentro del `Abstract`.
- **Dimensionalidad Coseno Directa:** Exclusión de métricas "dobles" o normalizaciones alteradas, ofreciendo un `FINAL_SCORE` continuo del -1 al 1.
- **Transparencia Heurística:** Todas las sugerencias categóricas procedimentales en el sistema son de caracter de Apoyo Interpretativo auxiliar, no verdades dogmáticas irreprochables computadas.

## Instalación
`pip install pandas numpy sentence-transformers openpyxl`

## Estructura del dataset
El sistema operará óptimamente sobre base Scopus / WOS:
```text
- Title
- Abstract
- Author Keywords
- Index Keywords
- Year
- Cited by
```
*Si faltan años ('Year') el modelo suspenderá los computos temporales de forma prudente evitando inyectar años sustitutivos por defecto que induzcan sesgos silentes.*

## Operatividad
Configura tus hiperparámetros de umbral referencial, modelo embebedor y ancla objetivo dentro de `config.py`.

```text
python main.py
```

## Salida de Datos

Las matrices xlsx se ordenan por defecto de forma descendente continua en función a la Afinidad (Score).
Output: `RESULTADO_MODULAR_YYYYMMDD_HHMM.xlsx`

Hojas en el libro de trabajo de priorización:
```text
- 0_RANKING_GENERAL
- 1_PRIORIZADOS
- 2_AUDITORIA
- 3_METADATA (Métricas y versión de la ejecución formalizadas para reproducibilidad científica)
- ESTADISTICAS_REFERENCIALES
```

## Semántica de Variables
Dadas las premisas metodológicas, la interpretación principal es:
- **FINAL_SCORE**    → Ratio vectorial crudo dictaminando superioridad de correlación matemática (Norte del Ranking).
- **DECISION**       → Clasificación complementaria interpretativa ("ALTA", "MEDIA", "BAJA").
- **bothkeywords**   → Fusión rigurosa de N-gramas (conceptos de varias palabras) extraída conservando la dimensionalidad ';'.
- **TipoMetodologico** → Inferencia en acumulación de evidencias mediante conteo multicampo, sujeta a verificación humana (Mixto, Teórico, Empírico, Review, etc).
- **AltaInfluenciaRelativa** → Variable estadística de percentil dinámico. Substituye al antiguo "Seminal" para transparentar mediciones directas sobre los artículos tope referenciados en función a sus pares filtrados en base de tiempo válido.
- **YearMissing**    → Bandera explicatoria técnica para documentos carentes de un tiempo oficial y estricto reportado, permitiendo aislarlos de analíticas temporales dudosas.
