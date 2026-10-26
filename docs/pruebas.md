# Pruebas y verificación del comportamiento

## Estrategia

1. **Prueba de caracterización (golden master).** Antes de tocar el código se escribió
   `escenario.py`, un guion de 36 pasos (34 operaciones, el reporte y la recarga) que ejercita todas las operaciones (registro válido e inválido,
   asignación, cambios de estado válidos e inválidos, cinco criterios de búsqueda, reporte con solicitud
   vencida y recarga desde disco). Su salida en la versión inicial se guardó en
   `docs/evidencias/salida_inicial.txt` (tag `estado-inicial`).
2. **Misma prueba, versión final.** `tests/test_caracterizacion.py` ejecuta el escenario sobre el código
   refactorizado y exige igualdad exacta con la salida inicial. Se ejecutó en cada commit de refactoring.
3. **Pruebas unitarias nuevas** (posibles gracias a la inyección de dependencias).
4. **Compatibilidad de datos:** `tests/fixtures/solicitudes_formato_inicial.json` fue generado por la
   versión inicial real; la versión nueva lo lee y sigue numerando correctamente.

## Casos de prueba

| ID | Caso | Resultado esperado | Archivo |
|---|---|---|---|
| CP-01 | Escenario completo (36 pasos) | Salida idéntica a la versión inicial | `test_caracterizacion.py` |
| CP-02 | Registrar con datos válidos | Estado PENDIENTE, prioridad por defecto del tipo, fecha del reloj | `test_servicio.py` |
| CP-03 | Cada dato inválido (nombre, legajo, mail, tipo, descripción, prioridad, fecha) | `ValidacionError` con el `campo` correcto | `test_servicio.py` |
| CP-04 | Registro inválido | No se persiste nada | `test_servicio.py` |
| CP-05 | Flujo asignar → EN_PROCESO → RESUELTA | Estados correctos | `test_modelos.py` |
| CP-06 | EN_PROCESO sin responsable / transición no permitida | `TransicionInvalida` | `test_modelos.py` |
| CP-07 | Área incorrecta o solicitud cerrada | `AsignacionInvalida` | `test_modelos.py` |
| CP-08 | Vencimiento por SLA (límite exacto y un día después) | No vencida / vencida | `test_modelos.py` |
| CP-09 | Solicitud cerrada nunca vence | `False` | `test_modelos.py` |
| CP-10 | Búsqueda por criterios (AND) | Ids esperados | `test_modelos.py`, `test_servicio.py` |
| CP-11 | Persistir y recargar | Mismos datos, incluido responsable | `test_servicio.py` |
| CP-12 | Archivo JSON corrupto | `ErrorDePersistencia` | `test_servicio.py` |
| CP-13 | Reporte vacío, orden y marca VENCIDA, conteos | Texto esperado | `test_reporte.py` |
| CP-14 | Leer archivo generado por la versión inicial | Datos leídos; el id siguiente continúa | `test_reporte.py` |
| CP-15 | Demo de CLI | Imprime el reporte | `test_cli.py` |

## Resultados

```
$ python -m unittest discover -s tests
Ran 29 tests ... OK
$ python tools/cobertura.py   ->  94 % de líneas de solicitudes/ cubiertas
$ python escenario.py | diff - docs/evidencias/salida_inicial.txt   ->  (sin diferencias)
```

## Diferencias intencionales respecto de la versión inicial

El comportamiento observable del escenario no cambió. Se **mejoró** deliberadamente (y se prueba) lo siguiente:

| Situación | Versión inicial | Versión refactorizada |
|---|---|---|
| Fecha con formato inválido | Se guardaba y rompía el reporte más tarde | `ValidacionError("fecha")` al registrar |
| Archivo JSON corrupto | `except:` vacío → lista vacía; el siguiente guardado **pisaba los datos** | `ErrorDePersistencia` explícito |
| Causa del rechazo | `False` / código numérico | Excepción específica |
| Búsqueda | Un criterio por vez; criterio desconocido devolvía `[]` en silencio | Criterios tipados combinables |

## Cómo reproducir

```bash
python -m unittest discover -s tests -v
python tools/cobertura.py
python tools/metricas.py solicitudes main.py
git show estado-inicial:gestor.py > /tmp/gestor.py   # versión inicial para comparar
```
