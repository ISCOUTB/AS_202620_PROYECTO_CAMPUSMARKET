# ADR-0009 - Materializar el catálogo sin romper las fronteras del monolito modular

**Estado:** Aceptado
**Fecha:** 2026-10-01
**Aspecto relacionado:** ASP-01 - Consulta y búsqueda de productos
**Escenario principal:** EC-01 - Consulta de productos

---

## 1. Contexto

CampusMarket adopta un monolito modular como estilo arquitectónico principal, de acuerdo con ADR-0001.

Los contextos delimitados vigentes son:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

Hasta S8, la funcionalidad materializada se ha concentrado principalmente en:

- creación de publicaciones;
- persistencia en MySQL;
- contrato HTTP/JSON;
- pruebas automatizadas;
- observabilidad;
- despliegue.

Sin embargo, el aspecto **ASP-01 - Consulta y búsqueda de productos** y el escenario **EC-01 - Consulta de productos** todavía no están materializados completamente.

EC-01 define que:

- un estudiante realiza una búsqueda o aplica un filtro;
- el sistema opera con un catálogo de hasta 1.000 publicaciones;
- en 10 búsquedas consecutivas, al menos 9 deben mostrar resultados en un máximo de 2 segundos.

Durante S6 también se definió la siguiente regla de propiedad de datos:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

La entidad `publicaciones` pertenece al contexto **Gestión de Publicaciones**.

El escritor productivo actual es:

`backend/app/publicaciones/repository.py`

También se documentó el riesgo MOD-01:

> Catálogo podría acceder directamente a la tabla `publicaciones`.

Por esta razón, la materialización del catálogo debe incorporar búsqueda, filtrado y consulta sin convertir al módulo `catalogo` en un segundo propietario de los datos.

---

## 2. Problema

CampusMarket necesita evolucionar de un formulario aislado de creación de publicaciones hacia una experiencia funcional de marketplace.

El usuario debe poder:

- entrar al catálogo;
- consultar publicaciones;
- buscar productos;
- aplicar filtros;
- ver el detalle de una publicación.

La implementación debe respetar las fronteras del monolito modular ya definidas.

El principal riesgo es implementar el catálogo mediante acceso directo a MySQL o mediante importaciones internas del repositorio de `publicaciones`, lo que produciría erosión arquitectónica.

---

## 3. Fuerzas y restricciones

La decisión está condicionada por:

- ADR-0001: CampusMarket continúa siendo un monolito modular;
- la propiedad de escritura de `publicaciones` pertenece a Gestión de Publicaciones;
- EC-01 exige una respuesta medible;
- se debe mantener una arquitectura simple y mantenible;
- no existe evidencia actual que justifique microservicios;
- la solución debe poder probarse automáticamente;
- S9 exige trazabilidad entre decisión, código, prueba y evidencia;
- la IA puede apoyar la implementación, pero la decisión arquitectónica pertenece al equipo.

---

## 4. Alternativas consideradas

### 4.1 Catálogo accede directamente a MySQL

El módulo `catalogo` ejecuta consultas directamente sobre la tabla `publicaciones`.

#### Ventajas

- implementación rápida;
- acceso directo a filtros y consultas;
- menor cantidad inicial de código.

#### Desventajas

- acopla `catalogo` al esquema físico de la base de datos;
- duplica conocimiento de persistencia;
- debilita la propiedad de datos definida en S6;
- facilita futuras escrituras indebidas desde `catalogo`;
- contradice el tratamiento del riesgo MOD-01.

**Decisión:** descartada.

---

### 4.2 Crear un microservicio independiente para Catálogo

El catálogo se convierte en un servicio desplegable independiente.

#### Ventajas

- escalado independiente;
- aislamiento operativo;
- autonomía tecnológica.

#### Desventajas

- aumenta la complejidad de despliegue;
- introduce fallos de red;
- requiere observabilidad adicional;
- incrementa costos;
- no existe evidencia que justifique actualmente separar el catálogo.

**Decisión:** descartada para el estado actual del proyecto.

---

### 4.3 Catálogo consume una capacidad explícita de lectura de Publicaciones

El contexto `catalogo` será responsable de búsqueda, filtrado y presentación de resultados.

Los datos serán obtenidos mediante una capacidad explícita de lectura provista por el módulo `publicaciones`.

El módulo `catalogo` no accederá directamente al repositorio de persistencia.

La escritura continuará siendo responsabilidad exclusiva de Gestión de Publicaciones.

#### Ventajas

- preserva las fronteras del monolito modular;
- mantiene un único propietario de los datos;
- evita duplicar persistencia;
- permite materializar ASP-01;
- mantiene una única unidad de despliegue;
- permite crear pruebas automáticas de modularidad.

#### Costos

- requiere una interfaz interna clara;
- añade coordinación entre contextos;
- requiere pruebas adicionales.

**Decisión:** seleccionada.

---

## 5. Decisión

CampusMarket materializará el contexto **Catálogo** como responsable de:

- consulta de publicaciones;
- búsqueda por texto;
- filtrado;
- composición de resultados;
- consulta del detalle de una publicación.

El módulo `catalogo` no será propietario de la persistencia.

Se establecen las siguientes reglas:

1. `publicaciones` mantiene la propiedad de escritura de la entidad `publicaciones`.
2. `catalogo` no ejecutará `INSERT`, `UPDATE` ni `DELETE` sobre `publicaciones`.
3. `catalogo` no importará directamente `backend/app/publicaciones/repository.py`.
4. `catalogo` consumirá una capacidad explícita de lectura de `publicaciones`.
5. La comunicación permanecerá dentro del mismo proceso.
6. No se introducirá un nuevo servicio desplegable.
7. No se introducirá una base de datos adicional.
8. Flutter seguirá comunicándose con FastAPI mediante HTTP/JSON.

La dirección conceptual será:

```text
Flutter
   ↓ HTTP/JSON
FastAPI
   ↓
Catálogo
   ↓ capacidad de lectura
Publicaciones
   ↓
Repositorio de Publicaciones
   ↓
MySQL

No se permitirá:
Catálogo
   ✕→ MySQL directamente

Tampoco:
Catálogo
   ✕→ repository.py de Publicaciones

6. Impacto funcional
La decisión permitirá materializar el siguiente flujo:
Inicio / Catálogo
        ↓
Búsqueda
        ↓
Filtros
        ↓
Resultados
        ↓
Detalle de publicación

La interfaz deberá incluir:
- tarjetas de productos;
- búsqueda;
- filtros;
- precio;
- estado;
- categoría;
- detalle;
- estados de carga;
- estado vacío;
- manejo de errores;
- diseño responsive para Flutter Web.
La mejora visual no modifica las fronteras arquitectónicas.
7. Impacto sobre el monolito modular
La decisión no reemplaza ADR-0001.
CampusMarket continúa siendo un monolito modular.
Los módulos continúan formando parte de la misma aplicación y de la misma unidad de despliegue.
La separación corresponde a responsabilidades de dominio y no a servicios distribuidos.
El módulo catalogo agrega comportamiento de lectura sin asumir propiedad sobre los datos de publicaciones.
8. Verificación arquitectónica
Se incorporarán pruebas automáticas que verifiquen que:
- catalogo no importe el repositorio de publicaciones;
- catalogo no utilice directamente PyMySQL;
- catalogo no realice escrituras sobre publicaciones;
- el único escritor productivo continúe perteneciendo a Gestión de Publicaciones.
Estas reglas formarán parte de la auditoría de erosión arquitectónica de S9.
No se considerará suficiente una revisión manual.
9. Verificación de EC-01
La implementación deberá medirse contra el escenario EC-01.
Condiciones:
- catálogo de hasta 1.000 publicaciones;
- 10 búsquedas consecutivas;
- al menos 9 de las 10 deben responder en un máximo de 2 segundos.
La evidencia deberá registrar:
- commit evaluado;
- cantidad de publicaciones;
- consulta aplicada;
- tiempos individuales;
- cantidad de ejecuciones dentro del umbral;
- resultado final.
No se declarará EC-01 como completamente materializado hasta realizar esta medición.
10. Relación con S9
Esta decisión podrá formar parte de la cadena de trazabilidad de la Evidencia S9:
ASP-01
   ↓
EC-01
   ↓
C4
   ↓
ADR-0009
   ↓
Código
   ↓
Pruebas
   ↓
Prueba que falla ante el defecto
   ↓
Medición
   ↓
Evidencia S9

Se realizará una mutación controlada o procedimiento equivalente para demostrar que las pruebas detectan una violación real de las fronteras arquitectónicas.
La mutación no permanecerá en la versión final.
11. Uso de IA
La IA generativa puede apoyar:
- propuestas de interfaz;
- generación de código;
- generación de pruebas;
- documentación;
- alternativas de implementación.
Sin embargo, la decisión arquitectónica pertenece al equipo.
Se rechazará cualquier propuesta de IA que:
- haga que catalogo acceda directamente a MySQL;
- importe directamente el repositorio de publicaciones;
- duplique la propiedad de los datos;
- introduzca una dependencia no verificada;
- cambie el estilo arquitectónico sin un nuevo ADR;
- genere código que el equipo no pueda explicar;
- debilite una regla de modularidad existente.
Las decisiones aceptadas, corregidas y rechazadas se registrarán en docs/ia.md.
12. Consecuencias
Positivas
- se materializa ASP-01;
- se preserva el monolito modular;
- se mantiene la propiedad de datos;
- se evita erosión arquitectónica;
- el producto evoluciona hacia un marketplace real;
- EC-01 se vuelve verificable;
- la implementación puede utilizarse como evidencia S9.
Negativas
- se requiere una interfaz interna explícita;
- se necesitan nuevas pruebas de modularidad;
- se debe medir el rendimiento;
- la implementación inicial será ligeramente más compleja que acceder directamente a MySQL.
13. Criterios de reconsideración
Esta decisión deberá revisarse mediante un nuevo ADR si ocurre alguno de los siguientes casos:
- el catálogo crece a un volumen que justifique otra estrategia;
- EC-01 deja de cumplirse sistemáticamente;
- se necesita escalado independiente;
- se incorpora un motor especializado de búsqueda;
- se introduce una proyección de lectura independiente;
- cambia la propiedad de los datos;
- existe evidencia de que el monolito modular ya no satisface las necesidades del sistema.
ADR-0001 no se modificará como consecuencia de esta decisión.
14. Estado de implementación
Al crear este ADR:
- ASP-01 está definido;
- EC-01 está definido;
- la frontera entre Catálogo y Publicaciones ya existe;
- la propiedad de publicaciones pertenece a Gestión de Publicaciones;
- el catálogo todavía no está materializado completamente;
- la medición EC-01 todavía está pendiente;
- la evidencia S9 todavía está pendiente.
Por estas razones, el estado inicial del ADR es:
Propuesto
Pasará a:
Aceptado
cuando el equipo verifique:
- implementación funcional;
- pruebas arquitectónicas;
- prueba que falle ante una violación controlada;
- medición EC-01;
- evidencia asociada.
