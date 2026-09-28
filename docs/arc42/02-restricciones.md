# Restricciones - CampusMarket

Las siguientes restricciones delimitan el desarrollo de CampusMarket y
condicionan las decisiones arquitectónicas que puede tomar el equipo. Se
identifican a partir del contexto académico, las condiciones del proyecto,
la evolución arquitectónica y el alcance definido para el prototipo.

---

## R-01. Tiempo de desarrollo

**Tipo:** Organizativa  
**Origen:** Asignatura / calendario académico

CampusMarket debe alcanzar un prototipo funcional dentro del semestre
académico.

**Justificación:** El proyecto se desarrolla de manera incremental durante
el curso y debe producir un sistema funcional y verificable dentro del
periodo establecido. Esta condición limita el alcance y la complejidad que
puede asumir el equipo, por lo que las funcionalidades seleccionadas deben
poder implementarse, probarse y documentarse durante el semestre.

---

## R-02. Tamaño del equipo

**Tipo:** Organizativa  
**Origen:** Conformación del equipo

CampusMarket será desarrollado por un equipo de tres integrantes.

**Justificación:** La capacidad de desarrollo disponible está limitada al
trabajo de tres integrantes durante el semestre. Por esta razón, las
decisiones arquitectónicas, el número de funcionalidades y la complejidad
de la solución deben ser compatibles con los recursos humanos disponibles.

---

## R-03. Repositorio y control de versiones

**Tipo:** Técnica / organizativa  
**Origen:** Metodología de trabajo del curso

El código fuente, la documentación arquitectónica y las evidencias
incrementales de CampusMarket deberán mantenerse versionados en el
repositorio del proyecto.

**Justificación:** El repositorio constituye el punto de referencia para
verificar la evolución del sistema y la correspondencia entre documentación,
implementación y evidencias. Además, permite mantener trazabilidad sobre los
cambios realizados por el equipo durante el semestre.

---

## R-04. Análisis de calidad del código

**Tipo:** Técnica  
**Origen:** Herramientas de calidad utilizadas en el proyecto

El repositorio de CampusMarket deberá mantenerse integrado con el proyecto
oficial de SonarQube Cloud durante el desarrollo.

**Justificación:** La integración permite analizar de manera continua
características relacionadas con la calidad y seguridad del código y obtener
evidencia verificable sobre problemas detectados durante el desarrollo. Esta
condición debe considerarse al organizar el repositorio y el flujo de trabajo
del proyecto.

---

## R-05. Alcance funcional del prototipo

**Tipo:** Organizativa / alcance  
**Origen:** Alcance definido por el equipo

La versión inicial de CampusMarket no incluirá pagos en línea, procesamiento
bancario, servicios de envío ni logística de entrega.

**Justificación:** Estas funcionalidades requieren integraciones con servicios
externos y aumentan considerablemente la complejidad técnica y operativa del
sistema. Excluirlas permite concentrar el esfuerzo del equipo en las
capacidades principales del marketplace: gestión de usuarios, publicación
de productos, búsqueda, filtrado y gestión de publicaciones.

---

## R-06. Plataforma web

**Tipo:** Técnica  
**Origen:** Alcance tecnológico inicial

CampusMarket será desarrollado como una aplicación web accesible desde
navegadores modernos.

**Justificación:** La aplicación permite que los estudiantes accedan a
CampusMarket desde computadores, tabletas o teléfonos mediante un navegador,
sin requerir la instalación de una aplicación de escritorio. Esta decisión
mantiene el proyecto dentro de un alcance tecnológico adecuado para el
semestre.

Durante S8 esta restricción se materializa mediante Flutter Web publicado en
GitHub Pages.

---

## R-07. Persistencia sin nueva infraestructura durante el primer corte

**Tipo:** Técnica / despliegue  
**Origen:** Restricción definida por el equipo para la evaluación arquitectónica S5

Durante el primer corte, CampusMarket debía mantener SQLite como mecanismo
de persistencia y conservar el backend como una única aplicación monolítica
modular, sin dividirlo en nuevos servicios desplegables.

La respuesta arquitectónica al reto no incorporaría una base de datos externa,
colas, cachés distribuidas ni nuevos servicios desplegables.

Esta restricción no implicaba que el frontend, el backend y la persistencia
fueran un único contenedor C4. La topología correspondiente a esa etapa era:

**Frontend Web → Backend API → SQLite**

El límite impuesto por R-07 consistía en evitar que el backend monolítico
modular fuera dividido o reemplazado por nueva infraestructura como respuesta
al reto arquitectónico del primer corte.

**Justificación:** La restricción limitó deliberadamente el espacio de
solución para evaluar si el corte vertical podía responder de manera
controlada ante una condición adversa de persistencia sin resolver el
problema mediante infraestructura adicional.

La línea base medida antes de aplicar cualquier cambio mostró que, ante un
bloqueo temporal de SQLite, la creación de una publicación respondió con
HTTP `500` después de `7.323 s`, sin producir una escritura parcial.

Después de liberar SQLite, el sistema recuperó la operación normal mediante
HTTP `201` en `0.007 s`.

Esta evidencia permitió localizar el problema en el comportamiento de la
relación entre el Backend API y SQLite, sin justificar una modificación de la
topología durante esa evaluación.

La respuesta arquitectónica del primer corte mantuvo SQLite, conservó el
backend como una única aplicación monolítica modular y aplicó mecanismos
internos de degradación controlada definidos en ADR-0002.

Posteriormente, esta restricción dejó de describir la persistencia vigente del
proyecto. La evolución posterior hacia MySQL se registró mediante ADR-0004,
manteniendo R-07 y ADR-0002 como evidencia histórica del primer corte.

**Escenario de calidad relacionado:**  
[EC-05 - Degradación ante bloqueo temporal de persistencia](./10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)

**Decisión arquitectónica histórica relacionada:**  
[ADR-0002 - Manejo de bloqueo temporal de SQLite](../adr/0002-manejo-bloqueo-sqlite.md)

**Decisión de evolución posterior:**  
[ADR-0004 - Migrar la persistencia de SQLite a MySQL](../adr/0004-migrar-persistencia-a-mysql.md)

**Evidencia de línea base:**  
[Línea base de bloqueo SQLite](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

**Evidencia posterior:**  
[Medición posterior a ADR-0002](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

---

## R-08. Despliegue público, reproducible y verificable en S8

**Tipo:** Técnica / operación  
**Origen:** Evidencia S8 - despliegue y operación

Durante S8 CampusMarket debe disponer de un entorno accesible externamente y
verificable, de modo que el funcionamiento del corte vertical no dependa
únicamente del equipo local de desarrollo.

El despliegue debe conservar la separación entre los componentes principales:

**Flutter Web → FastAPI → MySQL**

y mantener las fronteras arquitectónicas definidas previamente.

La materialización utilizada durante S8 corresponde a:

- Flutter Web publicado mediante GitHub Pages;
- FastAPI desplegado en Azure App Service;
- MySQL desplegado mediante Azure Database for MySQL Flexible Server;
- comunicación pública mediante HTTPS;
- comunicación entre backend y persistencia mediante conexión segura.

URLs públicas verificadas:

Frontend:

`https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/`

Backend:

`https://campusmarket-s8-api-nilver.azurewebsites.net`

Health check:

`https://campusmarket-s8-api-nilver.azurewebsites.net/health`

**Justificación:** Un sistema que solamente funciona en el entorno local no
permite verificar de forma independiente sus características operativas.
El despliegue público permite validar salud, integración, persistencia,
observabilidad y comportamiento del corte vertical en un entorno real.

**Evidencia relacionada:**  
[07-vista-despliegue.md](./07-vista-despliegue.md)

---

## R-09. Protección de secretos y configuración sensible

**Tipo:** Técnica / seguridad / operación  
**Origen:** Evidencia S8 - despliegue y operación

Las credenciales reales de los servicios desplegados no deben almacenarse
directamente en el código fuente, en los archivos de infraestructura ni en el
repositorio Git.

La configuración sensible debe proporcionarse mediante mecanismos externos al
código, tales como:

- variables de entorno;
- App Settings de Azure;
- parámetros seguros de Bicep.

La contraseña administrativa de MySQL se recibe mediante un parámetro seguro
de la plantilla de infraestructura.

La configuración local también debe evitar el versionamiento de archivos con
credenciales reales.

**Justificación:** Versionar credenciales junto con el código produciría una
exposición innecesaria de información sensible y dificultaría la rotación y
administración de secretos entre ambientes.

**Evidencia relacionada:**

- `infra/main.bicep`;
- configuración mediante App Settings de Azure;
- variables de entorno utilizadas por el backend;
- `.gitignore`;
- [07-vista-despliegue.md](./07-vista-despliegue.md).

---

## R-10. Infraestructura principal versionada como código

**Tipo:** Técnica / operación  
**Origen:** Evidencia S8 - reproducibilidad

Los recursos principales utilizados para ejecutar el backend y la persistencia
de CampusMarket en Azure deben contar con una definición versionada y
reproducible mediante infraestructura como código.

La definición utilizada durante S8 se encuentra en:

`infra/main.bicep`

La plantilla describe los recursos principales necesarios para el entorno,
incluyendo:

- App Service Plan;
- Web App para el Backend API;
- Azure Database for MySQL Flexible Server;
- base de datos `campusmarket`;
- configuración de la aplicación;
- reglas necesarias de acceso a la persistencia;
- parámetros dependientes del entorno.

La plantilla utiliza un parámetro seguro para la contraseña administrativa de
MySQL.

Durante S8 fue compilada mediante:

`az bicep build`

y validada mediante:

`az deployment group validate`

obteniendo:

`provisioningState: Succeeded`

y:

`error: null`

**Justificación:** La infraestructura versionada permite conocer qué recursos
forman parte del despliegue, repetir su configuración y mantener trazabilidad
entre arquitectura, código y entorno operativo.

**Evidencia relacionada:**  
[07-vista-despliegue.md](./07-vista-despliegue.md)

---

## Restricciones legales

En esta etapa del proyecto no se ha identificado una restricción legal
específica impuesta formalmente al prototipo.

Si el alcance de CampusMarket evoluciona e incorpora tratamiento adicional
de datos personales, pagos electrónicos u otros servicios externos, las
restricciones legales aplicables deberán identificarse y documentarse antes
de tomar las decisiones arquitectónicas correspondientes.

---

## Resumen

| ID | Restricción | Tipo | Origen |
|---|---|---|---|
| R-01 | Tiempo de desarrollo | Organizativa | Asignatura / calendario académico |
| R-02 | Equipo de tres integrantes | Organizativa | Conformación del equipo |
| R-03 | Repositorio y control de versiones | Técnica / organizativa | Metodología de trabajo del curso |
| R-04 | Integración con SonarQube Cloud | Técnica | Herramientas de calidad del proyecto |
| R-05 | Alcance funcional limitado | Organizativa / alcance | Definición del equipo |
| R-06 | Aplicación web | Técnica | Alcance tecnológico inicial |
| R-07 | Persistencia sin nueva infraestructura durante el primer corte | Técnica / despliegue | Restricción definida para S5 |
| R-08 | Despliegue público, reproducible y verificable en S8 | Técnica / operación | Evidencia S8 |
| R-09 | Protección de secretos y configuración sensible | Técnica / seguridad / operación | Evidencia S8 |
| R-10 | Infraestructura principal versionada como código | Técnica / operación | Evidencia S8 |

Estas restricciones establecen límites concretos para CampusMarket y permiten
distinguir las condiciones que restringen el espacio de solución de los
requisitos funcionales y de los escenarios de calidad que deben verificarse
mediante evidencia.

Las restricciones históricas se conservan para mantener trazabilidad sobre la
evolución arquitectónica del proyecto. En particular, R-07 describe la
situación del primer corte y no debe interpretarse como la persistencia vigente
de S8, que utiliza MySQL y un entorno público desplegado.
