# Registro IA S10 - Complemento nuevo

Fecha: 2026-10-11 (America/Bogota). Responsable de la solicitud y selección: Nilver García Pimentel. Herramienta: ChatGPT/Codex. Este complemento amplía el registro S10 añadido al final de [docs/ia.md](ia.md), conservando su historia. No se inventa una revisión humana que aún no haya ocurrido.

| Para qué se utilizó | Qué se aceptó y cómo se verificó | Qué se rechazó y motivo |
|---|---|---|
| Elegir un solo escenario operativo reproducible con el tiempo disponible | Cliente integrador incompatible con OpenAPI v2; se confirma 422 real en la API pública y se ejecutan tres fases nuevas | Fallo inducido de MySQL: sin control autorizado de contenedores no era ejecutable aquí. No se simula una ejecución pública con mocks. |
| Crear observador HTTP y adaptación explícita del consumidor | GET públicos, UUID de correlación, conservación de muestras, umbral antes de ejecutar, resumen calculado y versión del proveedor | Reutilizar EC-01/N+1 como resultado S10: no demostraría un estímulo operativo nuevo. |
| Diseñar prueba de frontera y recuperación del consumidor | Pruebas comprueban que sale no alcanza el servicio, que venta permite leer y que códigos/IDs aparecen en los logs | Cambiar automáticamente el enum del proveedor: amplía contrato y exige desplegar un cambio sin necesidad acreditada. |
| Documentar decisión, medidas y trazabilidad | ADR nuevo, adendas arc42/C4, matriz y vínculos a JSONL/JSON y workflow nuevos | Reescribir documentos o ADR aceptados existentes: contradice la instrucción del usuario y borra contexto histórico. |
| Preparar evidencia de entrega | Contenido completo en Git; se consigna exclusión de PDF sustentada en la revisión docente adjunta | Elaborar PDF: el usuario informa que no está habilitado y la revisión docente indica que está excluido. |
| Interpretar los resultados | Métricas derivadas de todas las muestras, pruebas locales y respuesta HTTPS; límites declarados | Afirmar 5/5, Sonar cerrado, logs privados extraídos, ausencia de SQL productivo o recuperación de MySQL: no existe esa evidencia. |

Las comprobaciones automatizadas reducen errores, pero no sustituyen el entendimiento del equipo. El guion de la evidencia S10 explicita qué se debe demostrar en vivo. La aceptación y calificación docente siguen pendientes.
