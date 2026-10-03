# ADR-0012 — Autenticar con sesiones opacas revocables

- Estado: Aceptado
- Fecha: 2026-10-03
- Relación: extiende ADR-0001, ADR-0004 y ADR-0009; elimina la identidad
  temporal del prototipo sin reescribir decisiones aceptadas.

## Contexto

La identidad enviada por Flutter o por parámetros HTTP no prueba propiedad.
EC-02 exige dos usuarios autenticados y 10/10 denegaciones de escritura ajena.
Web y Android comparten FastAPI y MySQL en un monolito modular.

## Alternativas

1. JWT firmado: validación local, pero revocación inmediata exige estado extra.
2. OAuth externo: añade proveedor, configuración y recuperación fuera del MVP.
3. Sesión opaca aleatoria con hash almacenado: revocación inmediata y un solo
   mecanismo para ambos clientes, a cambio de una consulta a MySQL por petición.

## Decisión

Adoptar la tercera opción. `usuarios` posee usuarios y sesiones. Generar 256
bits con `secrets`, enviar token Bearer solo al cliente y almacenar SHA-256
del token en MySQL. Expiración absoluta de 12 horas y logout que elimina
la sesión. Contraseñas con `hashlib.scrypt`, N=2^17, r=8, p=1, salt aleatorio
de 16 bytes, comparación constante y concurrencia de hashing acotada.
No implementar criptografía propia ni añadir librería de JWT.

El cliente conserva el token únicamente en memoria; recargar Web o reiniciar
Android requiere login. No usar localStorage ni un almacenamiento persistente
inseguro. Las mutaciones obtienen la identidad de una dependencia de usuarios;
`propietario_id` solo es campo de salida. Perfil mínimo: nombre y correo;
el correo no se publica en el catálogo.

Extraer la conexión MySQL a infraestructura compartida; cada repository sigue
siendo el único escritor de sus tablas. Catálogo y administración consumen
interfaces de servicio de publicaciones, nunca su repository.

Publicaciones heredadas de la identidad temporal quedan sin propietario y
fuera del catálogo al migrar. No asignarlas al primer usuario registrado.
Recuperarlas requiere atribución explícita respaldada por evidencia del equipo,
fuera del flujo público; no borrar los datos heredados.

## Trade-offs y consecuencias

- Logout efectivo incluso si se reutiliza el token anterior.
- Dependencia de MySQL para autenticar; caída devuelve 503, no acceso permisivo.
- scrypt consume aproximadamente 128 MiB por operación; limitar concurrencia
  y frecuencia de intentos antes de publicar en Internet.
- Token robado es reutilizable hasta expiración/logout; HTTPS es obligatorio.
- Cambia el contrato de creación/gestión: los clientes antiguos se rechazan.
- La sesión no se conserva entre reinicios; es una limitación consciente del MVP.

## Fuentes y trazabilidad

- [Python hashlib](https://docs.python.org/3.12/library/hashlib.html)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- EC-02; C4 Gestión de Usuarios y Gestión de Publicaciones.
- Implementación: `backend/app/usuarios/`, `backend/app/db.py`,
  `backend/app/publicaciones/`, `frontend/campusmarket/lib/usuarios/`.
- Pruebas: `test_usuarios.py`, `test_ec02_autorizacion.py`,
  `test_modularidad_s6.py`; evidencia en auditoría final del MVP.
