# Code review profesional

## 1. Checklist técnico

Criterio de aceptación: **todos los ítems críticos (C) en ✔** y los demás en ✔ o con acción registrada.

| # | Categoría | Ítem | Crit. | Resultado | Evidencia |
|---|---|---|---|---|---|
| 1 | Funcionalidad | El comportamiento externo coincide con la versión inicial | C | ✔ | `test_caracterizacion.py` (diff sin diferencias) |
| 2 | Funcionalidad | Los casos de error informan la causa | C | ✔ | `test_cada_dato_invalido_informa_su_campo` |
| 3 | Pruebas | Todas las pruebas pasan y se ejecutan con un solo comando | C | ✔ | 29 pruebas OK |
| 4 | Pruebas | Cobertura de líneas ≥ 80 % en el código de negocio | | ✔ | 94 % |
| 5 | SRP | Cada módulo/clase tiene una única razón de cambio | C | ✔ | Ver `solid_clean_code.md` |
| 6 | OCP | Agregar un tipo no exige modificar funciones existentes | | ✔ | `REGLAS_POR_TIPO` |
| 7 | DIP | La lógica no depende de archivos, reloj ni `print` | C | ✔ | Inyección en `ServicioSolicitudes` |
| 8 | Legibilidad | Nombres expresivos, sin abreviaturas crípticas | | ✔ | — |
| 9 | Legibilidad | Funciones ≤ 20 líneas y CC ≤ 10 | | ✔ | máx. 10 líneas, CC 10 |
| 10 | Legibilidad | Sin cadenas/números mágicos | | ✔ | Enums y constantes |
| 11 | Errores | Sin `except:` vacíos ni códigos de retorno | C | ✔ | `errores.py` |
| 12 | Recursos | Archivos abiertos con `with`; sin estado global | C | ✔ | `repositorio.py` |
| 13 | Limpieza | Sin código muerto, comentado ni imports sin uso | | ✔ | R8 |
| 14 | Datos | Compatibilidad con archivos existentes | C | ✔ | `test_lee_archivo_generado_por_la_version_inicial` |
| 15 | Datos | Solo datos sintéticos (sin datos personales reales) | C | ✔ | Nombres y legajos ficticios |
| 16 | Repositorio | README, docs, tags y commits ordenados | | ✔ | Ver README |

## 2. Observaciones del review y correcciones

| ID | Hallazgo | Severidad | Feedback | Acción | Estado |
|---|---|---|---|---|---|
| H1 | `escenario.py`: imports dentro de una función, `_CRITERIOS` definido después de su uso y una línea de más de 120 caracteres | Media | "La tabla de criterios debe declararse arriba y ser autoexplicativa." | Se movió a una constante de módulo con `(campo, conversor)` | **Corregido** |
| H2 | `ServicioSolicitudes.hoy()` existía solo para que el llamador armara el reporte: filtraba un detalle interno | Media | "El servicio debería ofrecer el caso de uso completo, no sus piezas." | Se reemplazó por `ServicioSolicitudes.reporte()` + prueba | **Corregido** |
| H3 | `RepositorioJSON` reescribe todo el archivo en cada `guardar` (O(n)) | Baja | Aceptable para el volumen del módulo; igual que la versión inicial | Documentado como mejora futura | Aceptado |
| H4 | `FiltroSolicitudes.coincide` tiene CC = 10 (cadena de `and`) | Baja | Se podría componer una lista de predicados | Mejora futura | Aceptado |
| H5 | Con `RepositorioMemoria`, el servicio y el repositorio comparten la misma instancia mutable de `Solicitud` | Baja | Riesgo de *aliasing* si se agregan más repositorios | Mejora futura (copias/entidades inmutables) | Aceptado |
| H6 | Validación de mail (`@`) y legajo (longitud) es mínima | Baja | Se conserva para no alterar el comportamiento externo | Mejora futura con cambio acordado | Aceptado |
| H7 | La CLI es solo una demostración | Baja | Falta interfaz de línea de comandos real (argparse) | Mejora futura | Aceptado |

## 3. Criterios de aceptación técnica (resultado)

- Salida de la prueba de caracterización idéntica ✔
- 0 smells de prioridad **A** sin resolver ✔ (#1-#6 resueltos)
- Hallazgos de severidad media corregidos ✔ (H1, H2)
- Hallazgos de severidad baja registrados con plan ✔ (H3-H7)
- Documentación y trazabilidad (tags, commits, evidencias) completas ✔
