# Sistema Modular de Clasificación Bibliométrica con SBERT

## Descripción general
Este sistema permite clasificar artículos científicos de forma automática según su relevancia temática, impacto bibliométrico y tipo metodológico.  
Está diseñado para apoyar:
```text
- Revisiones sistemáticas
- Estudios bibliométricos
- Procesos de selección de literatura académica
- Pre-filtrado automatizado para PRISMA
```
El sistema utiliza modelos de lenguaje basados en SBERT para calcular similitud semántica entre los artículos y el tema de investigación.

## Funcionalidades principales
```text
- Clasificación por relevancia temática mediante SBERT
- Detección automática de artículos seminales
- Identificación del tipo metodológico del estudio
- Generación de lista de lectura prioritaria
- Rescate automático desde media relevancia
- Auditoría PRISMA de artículos descartados
- Exportación de resultados en Excel y CSV
```
## Requisitos del sistema

### Versión de Python
- Python 3.10 o superior

### Librerías necesarias
```text
- pandas >= 2.0
- numpy >= 1.23
- sentence-transformers >= 2.2
- openpyxl >= 3.1
```
## Instalación
pip install pandas numpy sentence-transformers openpyxl

Opcional (entorno virtual recomendado):
```text
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy sentence-transformers openpyxl
```
## Estructura del dataset
El sistema puede trabajar con cualquier dataset bibliométrico, siempre que contenga las siguientes columnas obligatorias:
```text
- Title
- Abstract
- Author Keywords
- Index Keywords
- Year
- Cited by
```
Notas importantes:
```text
- El archivo puede ser CSV o Excel
- Los nombres de columnas deben coincidir exactamente
- Las columnas pueden estar vacías, pero deben existir
```
## Configuración del archivo de entrada
En el archivo config.py modifica la ruta:

INPUT_FILE = "ruta/a/tu/dataset.csv"

## Ejecución del sistema
```text
1. Abrir una terminal en la carpeta del proyecto
2. Ejecutar:
   python main.py
```
## Flujo del algoritmo
```text
1. Lectura del dataset
2. Limpieza del texto
3. Construcción del texto semántico
4. Cálculo de similitud con SBERT
5. Clasificación por relevancia
6. Clasificación metodológica
7. Cálculo de citas por año
8. Detección de artículos seminales
9. Rescate desde media relevancia
10. Generación de auditoría PRISMA
11. Exportación de resultados
```
## Archivos de salida
```text
- RESULTADO_MODULAR.xlsx
- TODOS_CLASIFICADOS.csv

Contenido del Excel:
```text
- 0_TODOS_CLASIFICADOS
- 1_LECTURA_PRIORITARIA
- 2_AUDITORIA
- STATS
```
## Columnas generadas por el sistema
```text
- score_semantic     → similitud semántica con el tema
- FINAL_SCORE        → score final de relevancia
- DECISION           → clasificación temática
- TipoMetodologico   → tipo de estudio
- CitasPorAño        → citas normalizadas por año
- EsSeminal          → indicador de artículo seminal
- In_lectura         → selección para lectura prioritaria
```
## Tipos de clasificación generados

### Relevancia temática
```text
- 🔥 ALTA RELEVANCIA
- ✅ MEDIA RELEVANCIA
- ⚠️ BAJA RELEVANCIA
- ❌ DESCARTAR
```
### Tipo metodológico
```text
- Empírico
- Teórico
- Review
- Indeterminado
```
## Personalización del sistema
En el archivo config.py puedes modificar:
```text
- TOPIC_TEXT     → texto del tema (ancla semántica)
- TH_HIGH        → umbral de alta relevancia
- TH_MID         → umbral de media relevancia
- TH_LOW         → umbral de baja relevancia
- RESCUE_RATE    → porcentaje de rescate
- RESCUE_MIN     → mínimo de artículos rescatados
- AUDIT_RATE     → porcentaje de auditoría
- AUDIT_MIN      → tamaño mínimo de auditoría
- AUDIT_MAX      → tamaño máximo de auditoría
```
## Casos de uso
```text
- Revisiones sistemáticas PRISMA
- Estudios bibliométricos
- Meta-análisis
- Filtrado automatizado de literatura científica
- Análisis de tendencias de investigación
```
## Licencia
Se recomienda usar:
- MIT License
o
- Apache 2.0
****
