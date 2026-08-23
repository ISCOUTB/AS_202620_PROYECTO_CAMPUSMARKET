@startuml
title CampusMarket - Diagrama de Contexto (C4 Nivel 1)
caption Evidencia S2 - Arquitectura de Software - Agosto 2026

left to right direction
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle
skinparam rectangle {
  RoundCorner 20
}
skinparam actor {
  BorderColor #1F3A5F
  FontColor #1F3A5F
}
skinparam rectangle {
  BorderColor #1F3A5F
  FontColor #1F3A5F
}
skinparam note {
  BackgroundColor #F9F9F9
  BorderColor #A0A0A0
}

actor "Estudiante" as estudiante
actor "Administrador" as admin

rectangle "CampusMarket\n\nMarketplace universitario para la publicación,\nbúsqueda, venta y alquiler de productos\nnuevos o usados dentro de la comunidad\nestudiantil." as campus #EAF2FB

rectangle "Comunidad estudiantil" as comunidad #F8F8F8
note right of comunidad
Representa el entorno de uso del sistema:
- estudiantes compradores
- estudiantes vendedores
- estudiantes que alquilan productos
end note

estudiante --> campus : Consulta productos,\npublica artículos,\nedita publicaciones propias,\nfiltra resultados\n[HTTPS]
admin --> campus : Supervisa usuarios y publicaciones,\nmodera contenido,\napoya la gestión del sistema\n[HTTPS]

campus --> comunidad : Facilita el intercambio de productos\ny la reutilización de artículos

note bottom of campus
Funciones principales del sistema:
- Registro e inicio de sesión
- Publicación de productos
- Venta y alquiler
- Búsqueda y filtros
- Administración de publicaciones

Fuera del alcance en S2:
- pagos en línea
- envíos
- logística de entrega
end note

legend right
|= Elemento |= Descripción |
| Estudiante | Usuario que publica, busca, compra o alquila productos |
| Administrador | Responsable de supervisar el contenido |
| CampusMarket | Sistema principal del proyecto |
| Flechas | Indican interacción, propósito y tecnología |
endlegend

@enduml
