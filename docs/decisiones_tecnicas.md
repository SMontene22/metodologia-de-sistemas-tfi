# Decisiones técnicas (registro estilo ADR)

| ID | Decisión | Contexto | Alternativas | Consecuencias |
|---|---|---|---|---|
| ADR-1 | Capturar un *golden master* **antes** de refactorizar | Hay que demostrar que no hay regresiones | Escribir pruebas unitarias después | Seguridad inmediata; el escenario normaliza resultados para correr en ambas versiones |
| ADR-2 | Cambio en paralelo (estructura nueva + migración + borrado) | Reescribir de golpe es riesgoso | Editar `gestor.py` en el lugar | Cada commit queda verde; el historial muestra la evolución |
| ADR-3 | Mantener el formato del archivo JSON | Los datos existentes no deben perderse | Cambiar el esquema | Compatibilidad total, probada con un fixture real |
| ADR-4 | Excepciones en lugar de códigos de retorno | Los códigos pierden la causa y se ignoran | Tipo `Resultado`/`Either` | Jerarquía clara; el escenario las traduce a la misma salida observable |
| ADR-5 | Solo biblioteca estándar (`unittest`, `trace`, `ast`) | Facilitar la ejecución en cualquier equipo | pytest, coverage, radon | Cero dependencias; métricas propias en `tools/` |
| ADR-6 | Reglas por tipo como tabla de datos | Eliminar `if/elif` duplicados (OCP) | Una subclase por tipo | Menos código; si las reglas crecieran en complejidad se evaluaría polimorfismo |
