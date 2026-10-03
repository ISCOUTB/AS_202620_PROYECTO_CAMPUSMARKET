# ADR-0014 — Habilitar moderadores por identificador interno

- Estado: Aceptado
- Fecha: 2026-10-03
- Reemplaza únicamente el mecanismo de habilitación por correo de ADR-0013.
  El resto de la decisión de reportes y moderación permanece aplicable.

## Contexto

El MVP no verifica propiedad del correo. Una lista de correos privilegiados
permitiría que otra persona registrase uno antes que su titular. La revisión
de seguridad detectó esta debilidad antes de implementarla.

## Alternativas

1. Allowlist de correo: insegura sin verificación de correo.
2. Sistema de roles y verificación de correo: mayor alcance y dependencias.
3. Allowlist de IDs de cuentas existentes, comprobadas por el operador.

## Decisión

Usar `CAMPUSMARKET_ADMIN_USER_IDS`, vacío por defecto, suministrado fuera del
repositorio. El operador verifica la cuenta ya registrada y configura su ID;
registro y edición de perfil nunca aceptan el identificador ni privilegios.
No hay primer usuario administrador ni ascenso automático.

## Trade-offs y consecuencias

Configuración sencilla y sin dependencia adicional. El operador debe comprobar
la identidad real del moderador; el ID no acredita identidad por sí solo.
Reaprovisionar una base de datos requiere revisar la allowlist, pues los IDs
pertenecen a esa base. No reutilizar configuración entre entornos sin verificar.

## Trazabilidad

Corrige una propuesta de IA rechazada. `usuarios/service.py:public_user`,
`usuarios/dependencies.py:moderador_actual` y `test_administracion.py`.
No se reescribe el ADR-0013 aceptado.
