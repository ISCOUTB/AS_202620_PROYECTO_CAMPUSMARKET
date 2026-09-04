# Evidencia de arranque con un solo comando

**Fecha de verificación:** 04/09/2026  
**Entorno:** Windows  
**Proyecto:** CampusMarket

## Objetivo

Verificar de forma ejecutable que CampusMarket puede iniciar su backend y
frontend mediante un único comando, atendiendo el hallazgo identificado en
la retroalimentación de la Evidencia S4.

## Comando ejecutado

Desde la raíz del repositorio se ejecutó:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1
```

El script utilizado corresponde a:

[`scripts/run_s4.ps1`](../../scripts/run_s4.ps1)

## Resultado observado

La ejecución del comando completó correctamente las siguientes acciones:

1. Inició el backend de CampusMarket con FastAPI y Uvicorn.
2. Ejecutó la resolución de dependencias del frontend mediante `flutter pub get`.
3. Inició Flutter Web utilizando Google Chrome.
4. El frontend quedó disponible en:

   `http://localhost:3000`

5. El backend quedó disponible en:

   `http://localhost:8000`

Durante la ejecución del backend, Uvicorn informó:

```text
Application startup complete.
```

El frontend inició correctamente y mostró la interfaz de creación de
publicaciones correspondiente al corte vertical de CampusMarket.

## Verificación del backend

Con la aplicación en ejecución se consultó manualmente el endpoint:

```text
http://localhost:8000/health
```

La respuesta obtenida fue:

```json
{
  "status": "ok",
  "service": "campusmarket-api"
}
```

Esta respuesta confirma que el backend se encontraba disponible después de
ejecutar el script de arranque.

## Verificación del frontend

Google Chrome abrió correctamente CampusMarket en:

```text
http://localhost:3000
```

La interfaz mostró el formulario **Publicar un producto**, correspondiente al
corte vertical implementado en S4.

El recorrido arquitectónico asociado es:

**Flutter Web → FastAPI → módulo publicaciones → SQLite**

## Procedimiento reproducible

Para repetir esta verificación en Windows:

1. Ubicarse en la raíz del repositorio.
2. Tener disponibles Python 3.12, Flutter y Google Chrome.
3. Instalar previamente las dependencias Python indicadas en el README.
4. Ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1
```

5. Comprobar el frontend en `http://localhost:3000`.
6. Comprobar el backend mediante `http://localhost:8000/health`.

## Resultado de la verificación

**Resultado: exitoso.**

El 04/09/2026 se verificó mediante ejecución local que
`scripts/run_s4.ps1` inicia correctamente el frontend y el backend de
CampusMarket utilizando un solo comando.

De esta forma queda atendido el pendiente señalado en la retroalimentación
de S4 respecto a dejar evidencia verificable del arranque del prototipo.
