# CampusMarket

Marketplace universitario para la publicación, consulta, venta y alquiler de productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

## Arquitectura

CampusMarket adopta un **monolito modular** de acuerdo con:

[ADR-0001 - Monolito modular](docs/adr/0001-usar-monolito-modular.md)

Para la Evidencia S4, el corte vertical implementado corresponde principalmente a la capacidad de `publicaciones`.

## Tecnologías actuales

- Frontend: Flutter / Dart
- Backend: FastAPI / Python
- Persistencia S4: SQLite
- Persistencia prevista posteriormente: MySQL

En S4, SQLite es la persistencia realmente implementada.

## Requisitos previos

- Python 3.12
- Flutter disponible en `PATH`
- Google Chrome
- Dependencias Python:

```bash
pip install -r backend/requirements.txt
