# 6. Vista de ejecución

## 6.1 Escenario S4 - Crear una publicación

El corte vertical de la Semana 4 implementa el caso de uso **crear una publicación de producto**.

1. El estudiante abre el formulario Flutter ubicado en `frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart`.
2. La interfaz valida los campos básicos y envía una solicitud `POST /publicaciones` mediante `publicaciones_api.dart`.
3. FastAPI recibe la solicitud en `backend/app/publicaciones/router.py`.
4. El servicio `backend/app/publicaciones/service.py` normaliza los datos del caso de uso.
5. `backend/app/publicaciones/repository.py` guarda la publicación en SQLite.
6. El backend devuelve `201 Created` con la publicación persistida y su identificador.
7. Flutter informa al estudiante que la publicación fue creada.

## 6.2 Verificación automatizada

`backend/tests/test_publicaciones_vertical.py` ejecuta el recorrido HTTP → lógica → persistencia utilizando una base SQLite temporal. La prueba crea una publicación, comprueba que el archivo de persistencia exista y vuelve a consultar las publicaciones para verificar que el dato guardado pueda recuperarse.

Este escenario evidencia que las cajas principales del C4 Nivel 2 tienen una implementación correspondiente y que el flujo documentado es ejecutable.
