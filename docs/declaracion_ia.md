# Declaración de uso de inteligencia artificial

| Campo | Detalle |
|---|---|
| Herramienta | Claude (Anthropic), modelo Claude Sonnet 5.5, en un entorno de ejecución con terminal y Git |
| Finalidad | Diseñar el sistema base con deuda técnica deliberada; diagnosticar code smells; proponer y aplicar refactorings; escribir pruebas y herramientas de métricas; redactar la documentación y el borrador del informe |
| Grado de intervención | **Alto** en la producción inicial del código, las pruebas y el borrador de los documentos. La revisión, ejecución, comprensión, ajuste y defensa oral corresponden al equipo `[COMPLETAR/AJUSTAR por el equipo]` |
| Verificación humana | Todo el código se ejecutó (29 pruebas, golden master, métricas). El equipo debe volver a ejecutarlo y poder explicar cada decisión |
| Evidencia del intercambio | Registro de prompts a continuación; el equipo debe adjuntar además la exportación de la conversación (PDF) |

## Registro de prompts

| N.º | Prompt (texto del usuario) | Adjuntos | Resultado |
|---|---|---|---|
| 1 | "estoy estudiando metodologia de sistemas 2. resolve el practico adjunto" | TP Unidad 4 – Semana 2 | Resolución teórica de branching, PRs, CONTRIBUTING, hooks (material de estudio previo) |
| 2 | "por favor, resolve el tp" | TP Unidad 4 – Semana 3 | Resolución teórica de CI/CD, SemVer, rollback, Blue-Green/Canary (material de estudio previo) |
| 3 | "tenemos que resolver el tp integrador" | `TP_MS2V2.pdf` (consigna del TPI) | Repositorio completo con tags, sistema base y refactorizado, pruebas, documentación e informe PDF (este trabajo) |

## Qué hizo la herramienta en el prompt 3 (resumen de pasos)

1. Leyó la consigna y extrajo requisitos (8 etapas, tags obligatorios, entregables).
2. Creó el sistema base `gestor.py` con problemas reales de diseño y un escenario determinista (*golden master*).
3. Redactó el diagnóstico (13 code smells), con evidencia por línea y métricas medidas con `tools/metricas.py`.
4. Refactorizó en tres commits, ejecutando las pruebas en cada paso.
5. Escribió las pruebas unitarias, la herramienta de cobertura y la documentación.
6. Realizó una revisión del código con checklist y aplicó las correcciones (H1 y H2).
7. Generó el informe PDF y el ZIP.

## Prompts propios del equipo
`[El equipo debe agregar aquí cada prompt adicional que utilice (ajustes, preguntas, correcciones) con fecha y finalidad.]`
