# Gestión de Solicitudes Académicas

Trabajo Práctico Integrador – Metodología de Sistemas II (TUP a distancia).
Módulo acotado para registrar solicitudes de estudiantes, clasificarlas por tipo, prioridad y estado,
asignar responsables, buscar y emitir un reporte. El foco del trabajo es la **evolución profesional del
código**: diagnóstico de deuda técnica, refactoring seguro, pruebas y code review.

## Funcionalidades
- Registrar solicitud (validación de datos, prioridad por defecto según el tipo).
- Cambiar estado respetando el flujo `PENDIENTE → EN_PROCESO → RESUELTA/RECHAZADA` (o `RECHAZADA`).
- Asignar responsable según el área que atiende cada tipo.
- Buscar por estado, tipo, prioridad, legajo y texto.
- Reporte con conteo por estado, orden por prioridad y marca `VENCIDA` según el SLA del tipo.
- Persistencia en `solicitudes.json`.

## Tecnologías
Python 3.10+ (solo biblioteca estándar), `unittest`, Git.

## Instalación y uso
```bash
git clone <URL-DEL-REPOSITORIO>
cd tp-solicitudes
python main.py                          # demo: registra una solicitud y muestra el reporte
python -m unittest discover -s tests -v # 29 pruebas
python tools/cobertura.py               # cobertura de líneas
python tools/metricas.py solicitudes    # complejidad, parámetros, longitud
```

Uso como biblioteca:
```python
from solicitudes.modelos import DatosSolicitud, Responsable
from solicitudes.catalogos import Area, Estado
from solicitudes.reloj import RelojSistema
from solicitudes.repositorio import RepositorioJSON
from solicitudes.servicio import ServicioSolicitudes

servicio = ServicioSolicitudes(RepositorioJSON("solicitudes.json"), RelojSistema())
s = servicio.registrar(DatosSolicitud("Ana Perez", "12345", "ana@mail.com", "CERTIFICADO", "Constancia"))
servicio.asignar_responsable(s.id, Responsable("Carlos Ruiz", Area.ALUMNADO))
servicio.cambiar_estado(s.id, Estado.EN_PROCESO)
print(servicio.reporte())
```

## Estructura
```
solicitudes/   catalogos.py  modelos.py  validacion.py  servicio.py  repositorio.py  reporte.py  reloj.py  errores.py  cli.py
tests/         pruebas unitarias, de caracterización y de compatibilidad de datos
tools/         metricas.py, cobertura.py (solo biblioteca estándar)
docs/          diagnóstico, SOLID/Clean Code, refactorings, pruebas, code review, decisiones y evidencias
escenario.py   guion determinista usado como golden master
```

## Tags del repositorio
| Tag | Significado |
|---|---|
| `estado-inicial` | Sistema base con deuda técnica (`gestor.py`) |
| `etapa-diagnostico` | Diagnóstico de calidad y 13 code smells |
| `etapa-refactoring` | Refactorings aplicados; golden master idéntico |
| `etapa-pruebas` | Pruebas unitarias, compatibilidad y cobertura |
| `etapa-docs` | Code review y documentación final |
| `estado-refactorizado` (y `estadorefactorizado`) | Estado final |

Para comparar: `git diff estado-inicial estado-refactorizado --stat`.

## Documentación
Ver [`docs/`](docs/): `diagnostico_code_smells.md`, `solid_clean_code.md`, `refactorings.md`, `pruebas.md`,
`code_review_checklist.md`, `decisiones_tecnicas.md`, `declaracion_ia.md` y `evidencias/`.

> Todos los datos son sintéticos. No se usan datos personales reales.
