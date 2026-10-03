# ADR-0013 — Materializar reportes y moderación mínima

- Estado: Aceptado
- Fecha: 2026-10-03
- Relación: extiende ADR-0001, ADR-0009 y ADR-0012.

## Contexto

Administración es un contexto declarado pero vacío. Un marketplace requiere
un mecanismo para reportar contenido abusivo y retirarlo del catálogo.
Un dashboard de métricas ficticias no materializa esa responsabilidad.

## Alternativas

1. Mantener el contexto vacío: no atiende reportes ni cumple el MVP de cuatro contextos.
2. Panel amplio con roles, analítica, pagos y bloqueo de cuentas: excede el alcance.
3. Reporte autenticado, cola de revisión y decisión de ocultar o descartar.

## Decisión

Adoptar la tercera alternativa. Administración posee `reportes_publicacion`,
con motivo, autor, publicación, estado y resolución. Cada usuario puede
reportar una publicación una vez; no se admiten reportes sobre la propia.
Solo un moderador puede listar reportes o resolverlos.

Habilitar moderadores por `CAMPUSMARKET_ADMIN_EMAILS` en configuración del
servidor. Registro y perfil no aceptan roles ni privilegios. Usar una única
capacidad de moderación, sin jerarquía de roles. Administración solicita a
publicaciones ocultar contenido por su servicio; no escribe tablas ajenas.
Resolver como descartado no altera la publicación. Resolver como ocultado
la retira del catálogo, preservando imágenes, propietario e historial.

## Trade-offs

- La configuración define quién modera; cambiarla requiere operación del servidor.
- No hay apelaciones, restauración ni sanciones de cuentas en este MVP.
- Referencias entre contextos son IDs; no se acoplan los repositories.
- Ocultar y registrar resolución son transacciones separadas. El ocultado
  es idempotente; un fallo puede reintentarse sin volver a mostrar contenido.

## Consecuencias y trazabilidad

La cola muestra reportes reales o un estado vacío. El catálogo excluye contenido
oculto, y el propietario conserva acceso a su publicación y al estado de moderación.
No hay botones simulados. C4: Administración → servicio de Publicaciones;
Usuarios suministra identidad/capacidad. Pruebas en `test_administracion.py` y
auditoría de límites; evidencia en auditoría final del MVP.
