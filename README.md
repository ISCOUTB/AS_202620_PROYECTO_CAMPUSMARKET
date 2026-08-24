# CampusMarket

Marketplace universitario para la compra, venta y alquiler de productos.

## Integrantes

- Joshua tenorio alvarez
- Camilo martinez berrio
- Nilver garcia pimentel

## Descripción
CampusMarket es una plataforma orientada a estudiantes universitarios
que busca facilitar la publicación, búsqueda, venta y alquiler de
productos nuevos o usados dentro de la comunidad estudiantil.

El proyecto será desarrollado durante el curso de Arquitectura de
Software.


## Problema
Los estudiantes universitarios compran durante su formación diferentes productos y materiales que posteriormente pueden dejar de utilizar, como libros, calculadoras, accesorios, dispositivos electrónicos y otros elementos relacionados o no con sus estudios.

Aunque estos productos podrían ser aprovechados por otros estudiantes, no siempre existe un medio organizado para ofrecerlos. Las publicaciones suelen realizarse en grupos de mensajería o redes sociales, donde pueden perder visibilidad rápidamente y no existe una clasificación adecuada de los artículos.

Además, un estudiante que necesita un producto específico puede tener dificultades para saber si otro miembro de la comunidad universitaria lo tiene disponible para vender o alquilar.

Por esta razón, se plantea desarrollar CampusMarket, una plataforma que permita organizar las publicaciones de productos y facilite la conexión entre estudiantes interesados en vender, alquilar o adquirir artículos.

## Objetivo General
Diseñar e implementar un prototipo funcional de una plataforma de marketplace universitario que permita a los estudiantes publicar, buscar y gestionar productos disponibles para venta o alquiler, utilizando una arquitectura de software modular, escalable y mantenible.

## Beneficiarios
Los principales beneficiarios serán los estudiantes universitarios, tanto quienes desean ofrecer productos como quienes buscan adquirirlos o alquilarlos.

También se identifica al administrador de la plataforma como stakeholder, ya que tendrá la responsabilidad de supervisar el funcionamiento del sistema y gestionar contenido cuando sea necesario.

De forma indirecta, la comunidad universitaria puede beneficiarse al fomentar la reutilización y circulación de productos que todavía tienen vida útil.
## Estrategia arquitectónica

CampusMarket adopta un **monolito modular** para la organización interna del backend, de acuerdo con la decisión registrada en el ADR-0001.

El backend se encuentra organizado inicialmente en los siguientes módulos:

- `usuarios`: registro, autenticación y gestión básica de usuarios.
- `publicaciones`: creación, modificación y gestión de publicaciones.
- `catalogo`: consulta, búsqueda y filtrado de productos.
- `administracion`: supervisión y gestión básica del contenido.

La aplicación aún no contiene lógica de negocio. En esta etapa se mantiene únicamente el esqueleto ejecutable requerido para continuar el desarrollo incremental del proyecto.

## Tecnologías

- **Frontend:** Flutter / Dart.
- **Backend:** FastAPI / Python.
- **Base de datos prevista:** MySQL.

## Esqueleto ejecutable

El backend puede iniciarse desde la raíz del repositorio con un solo comando:

```bash
python -m uvicorn backend.app.main:app --reload
