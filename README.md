# CampusMarket

CampusMarket es un marketplace universitario orientado a centralizar la publicación, consulta, venta y alquiler de productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

## Estrategia arquitectónica

CampusMarket adopta un **monolito modular**, de acuerdo con:

[ADR-0001 - Adoptar un monolito modular](docs/adr/0001-usar-monolito-modular.md)

Las fronteras arquitectónicas definidas para el backend corresponden a las capacidades:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

Para la Evidencia S4, la capacidad implementada y ejercitada por el corte vertical es principalmente:

`publicaciones`

## Tecnologías actuales

- **Frontend:** Flutter / Dart
- **Backend:** FastAPI / Python
- **Persistencia actual del corte S4:** SQLite
- **Persistencia prevista para una evolución posterior:** MySQL

La documentación distingue explícitamente entre lo que existe actualmente y lo que se encuentra previsto para una evolución posterior.

Durante S4, la persistencia realmente implementada y verificada es **SQLite**.

## Requisitos previos

Para ejecutar el corte vertical se requiere:

- Python 3.12
- Flutter instalado y disponible en `PATH`
- Google Chrome
- dependencias Python instaladas

Desde la raíz del repositorio:

```bash
pip install -r backend/requirements.txt
