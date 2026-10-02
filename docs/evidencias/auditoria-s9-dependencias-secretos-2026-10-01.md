# Auditoría S9 - Dependencias y secretos

**Proyecto:** CampusMarket
**Semana:** S9
**Fecha:** 2026-10-01

---

## 1. Dependencias

Para la porción S9 correspondiente a la materialización del Catálogo se revisaron:

- `requirements.txt`
- `frontend/campusmarket/pubspec.yaml`

No se incorporaron nuevas dependencias como consecuencia de la implementación de Catálogo.

La solución utiliza capacidades ya presentes en el proyecto:

- FastAPI;
- Pydantic;
- Pytest;
- TestClient;
- biblioteca estándar de Python.

Por tanto, no existen nuevas dependencias propuestas por IA que deban incorporarse al sistema para esta porción.

---

## 2. Búsqueda de secretos de alto riesgo

Se ejecutó:

git grep -n -I -E "AKIA|AIza|sk-[A-Za-z0-9]|ghp_|github_pat_|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY"

Resultado:
Sin coincidencias.

No se detectaron:
- claves privadas;
- tokens GitHub;
- claves OpenAI;
- claves Google;
- patrones AWS revisados.

## 3. Revisión de referencias a credenciales
Se ejecutó:
git grep -n -I -E "PASSWORD|SECRET|TOKEN|API_KEY"

Las coincidencias fueron revisadas individualmente.
Variables de entorno
Referencias como:
- CAMPUSMARKET_DB_PASSWORD
- SONAR_TOKEN
corresponden a nombres de variables de entorno o documentación de configuración.
No contienen el valor de una credencial productiva.
Placeholders documentales
El README utiliza:
<PASSWORD_LOCAL>

como marcador explícito e indica que no debe sustituirse por una credencial real dentro de un archivo versionado.
Credenciales efímeras de CI
El workflow backend-tests.yml contiene:
MYSQL_ROOT_PASSWORD: root_ci
MYSQL_PASSWORD: campusmarket_ci
CAMPUSMARKET_DB_PASSWORD: campusmarket_ci

Estos valores pertenecen exclusivamente al servicio MySQL efímero creado durante GitHub Actions.
No corresponden a la base de datos desplegada ni otorgan acceso a un recurso persistente externo.
Se clasifican como datos de prueba reproducibles del entorno CI, no como secretos productivos.

## 4. Resultado
Control	Resultado
Nuevas dependencias S9	Ninguna
Tokens detectados	Ninguno
Claves privadas detectadas	Ninguna
Credenciales productivas hardcodeadas detectadas	Ninguna
Placeholders documentales	Sí, controlados
Credenciales efímeras de CI	Sí, identificadas y limitadas al entorno de pruebas


Resultado de auditoría: sin evidencia de secretos productivos incorporados por la porción S9.
