# Estándar corporativo: Fabric Apps

## Diseño visual

Usa los tokens y clases base de `corporativo/estilo-app.css` como punto de
partida; no son una aplicación completa. La app tiene fondo gris muy claro,
superficies blancas, texto oscuro, azul como acción principal, tipografía
Segoe UI, espaciado múltiplo de 4 px y bordes suaves.

Estructura mínima: título y propósito, filtros con etiquetas, contenido
principal y fecha de actualización cuando sea conocida. Una acción principal
por pantalla; secundarios con menor énfasis. Evita gráficos decorativos y
aplica la selección de `reportes.md`.

Valores base: título principal 28 px y semibold; título de sección 20 px;
texto 16 px y texto auxiliar 14 px. Usa espacios de 4, 8, 16, 24 o 32 px,
tarjetas con radio de 8 px y contenido de hasta 1280 px de ancho. Muestra las
tarjetas en una cuadrícula adaptable: hasta tres columnas en escritorio y
una en móvil. El botón principal es azul con texto blanco; el secundario es
blanco con borde y texto azul. Los elementos y series usan los tokens, no
colores arbitrarios. Para un botón secundario aplica las clases `corp-button`
y `corp-button-secondary`. Cualquier excepción se documenta y aprueba.

Todos los controles deben funcionar con teclado y tener foco visible. Usa
HTML semántico y etiquetas accesibles; no comuniques estado solo con color.
Texto con contraste mínimo 4,5:1. Incluye estados de carga, error y vacío,
mensajes comprensibles y un diseño adaptable a móvil. No registres datos
sensibles en consola, URLs ni telemetría.

## Acceso y preparación para producción

Autenticación no equivale a autorización de datos: valida por separado el
permiso de la app, el conector y la fuente, la identidad efectiva y RLS/OLS
cuando corresponda. Nunca pongas secretos ni tokens en el cliente o en Git.
Usa el SDK, conectores y mecanismos de secretos compatibles y vigentes.

Antes de desplegar: revisar amenazas y permisos mínimos, pruebas de identidad
y aislamiento, accesibilidad, manejo de errores, calidad de datos, rendimiento,
observabilidad sin datos sensibles, licencias, capacidad y coste. Acordar
entornos, responsable, aprobación y reversión. El despliegue y la compartición
requieren autorizaciones separadas.

[Fabric Apps](https://learn.microsoft.com/en-us/fabric/apps/overview)
· [Conectores](https://learn.microsoft.com/en-us/fabric/apps/connectors)
