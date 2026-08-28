# C4 Nivel 1 - Contexto de CampusMarket

El diagrama de contexto vigente de CampusMarket se mantiene como **diagrama como código** en:

[`01-contexto.puml`](./01-contexto.puml)

## Propósito

El C4 Nivel 1 muestra a CampusMarket como un único sistema y representa únicamente los actores externos que interactúan con él.

En este nivel no se muestran contenedores, módulos, componentes ni detalles internos de implementación.

## Actores externos

### Estudiante

Miembro de la comunidad universitaria que utiliza CampusMarket para:

- publicar productos;
- consultar productos;
- buscar productos disponibles.

### Administrador

Usuario responsable de supervisar las publicaciones y apoyar la gestión del contenido disponible en CampusMarket.

## Sistema bajo diseño

**CampusMarket** es un marketplace universitario orientado a centralizar la publicación, consulta y búsqueda de productos dentro de la comunidad universitaria.

## Relaciones principales

- **Estudiante → CampusMarket:** publica, consulta y busca productos mediante la interfaz web.
- **Administrador → CampusMarket:** supervisa publicaciones y contenido mediante la interfaz web.

Durante el desarrollo local del prototipo se utiliza comunicación mediante **HTTP**.

El uso de **HTTPS** corresponde a un despliegue externo futuro y no se documenta como si ya estuviera implementado en el entorno local actual.

## Alcance

Para la Evidencia S4 se mantienen fuera del alcance actual:

- pagos electrónicos;
- procesamiento bancario;
- envíos y logística;
- servicios externos de transporte.

Actualmente no se representan sistemas externos adicionales porque esas integraciones no forman parte del prototipo implementado.

## Relación con el C4 Nivel 2

El C4 Nivel 1 representa CampusMarket como una única caja.

El C4 Nivel 2 realiza un acercamiento al interior de esa caja y muestra los contenedores principales del sistema:

- Frontend Web;
- Backend API;
- Persistencia local.

Los actores externos definidos en este nivel se mantienen coherentes con el C4 Nivel 2.

## Fuente canónica

El archivo [`01-contexto.puml`](./01-contexto.puml) es la fuente versionada y vigente del C4 Nivel 1.

Cualquier modificación del diagrama debe realizarse sobre ese archivo para evitar mantener versiones contradictorias de la arquitectura.
