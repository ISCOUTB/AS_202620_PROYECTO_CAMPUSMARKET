# ADR-0017 — Serializar inicialización y migración de identidad

- Estado: Aceptado
- Fecha: 2026-10-03
- Relación: extiende ADR-0004 y ADR-0012. No reescribe esos ADR.

## Contexto

El esquema heredado tenía propietario_id DEFAULT 1. ADR-0012 retira esa
identidad y preserva las filas sin atribuirlas a la primera cuenta. MySQL DDL
hace commit implícito. Inicializadores concurrentes podían observar el default
anterior y uno repetir el borrado de propiedad sobre filas ya autenticadas.

## Alternativas

1. Un Lock de Python: coordina threads, pero no procesos o instancias solapadas.
2. Herramienta nueva de migraciones y un proceso externo: posible evolución,
   pero incorpora dependencia/operación adicional para una única migración.
3. Advisory lock de MySQL por base y contexto durante inicialización:
   disponible en el motor, compartido entre conexiones, sin nuevo paquete.

## Decisión

Elegir 3. Publicaciones obtiene GET_LOCK con nombre
cm:pub:<primeros 40 caracteres SHA-256 del nombre de base>, espera hasta 5 s
y exige retorno 1 antes de cualquier DDL o migración. El cierre de la conexión
libera el lock incluso al fallar; los commits implícitos no lo liberan.
Sin lock devuelve la condición de persistencia ocupada y HTTP 503.

El protocolo se ejecuta antes de los accesos del repository; migrar filas
heredadas conserva su contenido, elimina identidad temporal y retira el default.
Una inicialización posterior debe conservar propietarios reales.

## Trade-offs y consecuencias

- Inicialización concurrente se serializa y puede responder 503.
- El lock no sustituye transacciones ni bloqueos de filas de imágenes.
- Solo Publicaciones escribe sus datos; db.py sigue sin SQL de dominio.
- Los procesos solapados de dos versiones siguen obligados a este protocolo;
  una versión histórica que lo ignora no es compatible para rolling update.
- Migraciones más numerosas justificarían reevaluar un ejecutor dedicado.

## Prueba y evidencia

Una conexión mantiene el lock mientras termina el esquema heredado y agrega
una publicación con propietario real. Otro inicializador debe esperar y, al
continuar, conservar esa propiedad y la fila heredada sin propietario.
La prueba usa MySQL real; la mutación que sustituye GET_LOCK por SELECT 1
debe detectar la pérdida de coordinación.

Fuente: [MySQL locking functions](https://dev.mysql.com/doc/refman/8.4/en/locking-functions.html).
