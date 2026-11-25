# Estándar corporativo: gráficos y reportes

## Selección obligatoria de gráficos

| Pregunta | Visual principal | Regla |
|---|---|---|
| Una cifra y su contexto | Tarjeta | Indicar unidad y periodo; comparación solo si está validada |
| Evolución temporal | Línea | Tiempo ordenado, escala coherente y unidades visibles |
| Comparar categorías | Barras horizontales | Ordenar por valor; eje de valor desde cero |
| Comparar pocos periodos | Columnas | Orden cronológico; eje de valor desde cero |
| Parte de un total | Barras apiladas | Solo cuando las partes sean comparables y sumen el total |
| Dos medidas y su relación | Dispersión | Ejes y unidades claros; sin afirmar causalidad |
| Detalle y comprobación | Tabla o matriz | Columnas relevantes, encabezados claros y formato consistente |

No usar gráficos 3D, donut, tarta, velocímetros ni mapas por defecto. No
truncar ejes de barras o columnas para exagerar diferencias. Evitar dobles
ejes; si fueran imprescindibles, justificar y revisar. Para muchas categorías,
usar un filtro o un Top N claramente etiquetado, sin ocultar el alcance.
Una excepción requiere justificación y aprobación en el PR.

## Diseño común

Importa `corporativo/tema-powerbi.json` en Power BI Desktop desde
**Vista > Temas > Examinar temas**. Es una base: revisa los visuales, ya que un
tema no controla todas las propiedades ni elimina formatos manuales existentes.

- Fondo claro, texto oscuro y fuente Segoe UI. Mantén el color de una misma
  categoría coherente dentro del informe.
- Página 16:9 con una pregunta principal; título descriptivo, filtros visibles y
  unidades en títulos o etiquetas. Prioriza lectura de izquierda a derecha.
- Como base, hasta 5 visuales informativos por página y hasta 8 categorías
  visibles en comparaciones. Más requieren justificación y revisión; si se
  usa Top N, indica el criterio y el alcance.
- Usa pocas visualizaciones, sin duplicar información. No ocultes resultados
  vacíos ni los confundas con cero.
- Texto y datos esenciales con contraste mínimo 4,5:1; no uses solo el color
  para comunicar estado. Añade texto alternativo a visuales informativos y
  revisa el orden de tabulación, teclado y uso sin percepción del color.
- Reutiliza el modelo y medidas aprobados, valida filtros, periodo, moneda,
  totales, identidad efectiva y RLS/OLS aplicables antes de publicar.

Un informe es apto para revisión cuando tiene responsable, fuente y medidas
confirmadas, evidencia de pruebas funcionales y de accesibilidad y plan de
promoción y reversión. Un tema no asegura accesibilidad ni seguridad.

[Accesibilidad de reportes](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports)
· [Temas JSON](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom)
