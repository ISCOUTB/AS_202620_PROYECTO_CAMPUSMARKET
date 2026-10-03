# Cierre documental S8, S9 y MVP — CampusMarket

**Fecha:** 2026-10-03  
**Base auditada:** `master` oficial  
**Commit oficial de referencia:** `acf757bf56812bee07fa0215fb828e0fa0055d6b`  
**PR de integración del MVP:** `#49 - Mvp autenticacion producto`

---

## Propósito

Este documento **no reemplaza ni reescribe** las evidencias históricas de S8 y S9.
Su objetivo es cerrar los pendientes que en esos archivos eran correctos en el
momento de su redacción, pero que después quedaron resueltos por la evolución del
repositorio y por la integración del MVP.

Se mantiene la misma regla de auditoría usada en S7:

**requisito → implementación → ejecución real → prueba → evidencia → hash**.

---

# Resultado de cierre

El MVP fue integrado al `master` oficial mediante el PR #49. El merge produjo el
commit:

```text
acf757bf56812bee07fa0215fb828e0fa0055d6b
```

Sobre ese mismo hash de `master` finalizaron correctamente los workflows principales
que verifican backend, Flutter, persistencia con Compose y flujo funcional Web/Android.

Por tanto, no se usa el resultado de una rama o de otro SHA como sustituto de la
validación del estado oficial.

---

# Matriz de cierre auditable

| Criterio | Estado | Evidencia verificable |
|---|---|---|
| S8 integrado posteriormente en `master` | **CUMPLE** | La historia posterior a S8 está integrada y el `master` oficial de referencia es `acf757bf...` |
| Pipeline oficial sobre `master` | **CUMPLE** | Backend, Flutter, Compose y flujo Web/Android finalizaron `success` sobre `acf757bf...` |
| S9 con commit y CI verificables | **CUMPLE** | La evidencia S9 conserva su hash histórico y run; este cierre no los sustituye |
| Evolución S9 → MVP trazable | **CUMPLE** | README, `docs/aspectos.md`, C4, arc42, ADR y auditoría MVP enlazan la evolución posterior |
| Autenticación y sesión reales | **CUMPLE** | Registro/login/perfil/logout con sesiones opacas revocables; ADR-0012 y pruebas del MVP |
| Propiedad server-side de publicaciones | **CUMPLE** | Identidad derivada de sesión; EC-02 con dos cuentas y mutaciones ajenas rechazadas |
| Cuatro contextos delimitados | **CUMPLE** | `usuarios`, `publicaciones`, `catalogo`, `administracion`; C4 L3 y pruebas de modularidad/erosión |
| Contrato vigente | **CUMPLE** | `contracts/openapi-v2.json` comparado contra FastAPI por prueba contractual |
| Web y Android | **CUMPLE** | Workflow de flujo real aprobado para Chrome escritorio, móvil y Android |
| Persistencia y recreación | **CUMPLE** | Workflow Compose aprobado con MySQL y volumen de imágenes |
| SonarQube Cloud | **CUMPLE CON OBSERVACIÓN** | Quality Gate passed y 0 Security Hotspots; Sonar reporta 14 issues nuevos y 0.0 % coverage en new code |
| Despliegue público del nuevo MVP | **PENDIENTE** | El despliegue público histórico de S8 existe, pero el MVP integrado en `acf757bf...` aún debe desplegarse y verificarse por separado |

**Recuento de cierre documental:** 11 criterios cerrados y 1 pendiente deliberado de la siguiente fase: despliegue público del MVP.

---

# 1. Cierre posterior de S8

La evidencia original `docs/evidencias/evidencia-s8-2026-09-27.md` termina con dos
pendientes históricos:

```text
[ ] integrar S8 en master
[ ] comprobar pipeline verde sobre el commit final de master
```

Esos ítems describían correctamente el estado **antes de la entrega de S8** y no se
eliminan para preservar la cronología.

Con posterioridad, la evolución del proyecto sí fue integrada en `master`. El estado
de referencia utilizado para este cierre es el merge del MVP:

```text
master = acf757bf56812bee07fa0215fb828e0fa0055d6b
```

Además, los workflows oficiales ejecutados por `push` sobre ese hash finalizaron
correctamente:

| Workflow | Run | Resultado |
|---|---:|---|
| Compose y persistencia del MVP | `37153952423` | `success` |
| Pruebas del backend | `37153952486` | `success` |
| Validación Flutter MVP | `37153952520` | `success` |
| Flujo real Web y Android | `37153952567` | `success` |

Esto cierra los pendientes históricos de integración/CI sin alterar la evidencia S8
original ni atribuirle funcionalidades posteriores que no existían en esa semana.

---

# 2. Normalización de lectura de S9

La evidencia `docs/evidencias/evidencia-s9-2026-10-01.md` ya contiene los elementos
materiales exigidos para la semana: porción real, trazabilidad, ADR, pruebas,
mutación controlada, restauración a verde, medición EC-01, uso de IA, dependencias,
secretos, decisión sobre componente generativo y CI.

Para facilitar la revisión automática, su lectura se normaliza con la siguiente
cadena resumida:

```text
ASP-01
  ↓
EC-01
  ↓
C4
  ↓
ADR-0009
  ↓
backend/app/catalogo/
  ↓
pruebas funcionales
  ↓
prueba de erosión
  ↓
mutación roja / restauración verde
  ↓
medición EC-01
  ↓
evidencia S9
```

La medición histórica de S9 se conserva exactamente como evidencia de esa semana;
no se sustituye por mediciones posteriores del MVP.

---

# 3. Cierre de la auditoría MVP

`docs/evidencias/auditoria-mvp-continuacion-2026-10-03.md` fue redactado durante la
rama de continuación y por ello termina con estados transitorios: Sonar pendiente,
PR oficial aún no creado/mergeado y despliegue aún no ejecutado.

La evolución posterior resolvió los dos primeros puntos:

- PR oficial #49 creado e integrado;
- merge oficial en `acf757bf56812bee07fa0215fb828e0fa0055d6b`;
- workflows principales de `master` aprobados sobre ese mismo hash;
- SonarQube Cloud informó **Quality Gate passed** y **0 Security Hotspots**.

La observación de Sonar se conserva completa y sin maquillarla:

```text
Quality Gate: passed
New issues: 14
Accepted issues: 0
Security Hotspots: 0
Coverage on New Code: 0.0 %
Duplication on New Code: 0.0 %
```

Por tanto, **Quality Gate verde no se interpreta como “cero issues”**.

---

# 4. Estado vigente antes del despliegue del MVP

A nivel de código y verificación automática, el estado oficial puede resumirse así:

```text
Producto MVP                 CERRADO PARA DESPLIEGUE
Backend / MySQL              VERIFICADO
Flutter Web                  VERIFICADO
Android                      VERIFICADO
Compose / persistencia       VERIFICADO
Contrato OpenAPI v2          VERIFICADO
Modularidad / erosión        VERIFICADO
Autenticación / propiedad    VERIFICADO
Sonar Quality Gate           PASSED, con observaciones registradas
Despliegue público MVP       PENDIENTE
```

No se declara el proyecto totalmente cerrado hasta que el nuevo MVP sea desplegado
y se verifique en el entorno público elegido.

---

# 5. Regla para la siguiente fase

El siguiente bloque debe ejecutarse desde el `master` oficial y producir evidencia
para el **mismo SHA que se despliegue**:

1. seleccionar el entorno de despliegue exigido por el curso;
2. versionar cualquier decisión arquitectónica nueva mediante ADR, sin reescribir ADR aceptados;
3. desplegar backend, persistencia y frontend según la topología elegida;
4. verificar `/health`, login, catálogo, creación/edición, imágenes, autorización y administración;
5. registrar URL pública, SHA desplegado, configuración no sensible y pruebas reales;
6. actualizar la vista de despliegue y el README únicamente con resultados comprobados.

La persistencia de imágenes requiere atención específica: el volumen local/Compose
es válido para desarrollo y pruebas; cualquier despliegue que no garantice
persistencia durable debe resolver esa brecha antes de considerar la capacidad de
imágenes cerrada en producción.

---

# Referencias

- `README.md`
- `docs/aspectos.md`
- `docs/evidencias/evidencia-s7-2026-09-15.md`
- `docs/evidencias/evidencia-s8-2026-09-27.md`
- `docs/evidencias/evidencia-s9-2026-10-01.md`
- `docs/evidencias/auditoria-mvp-continuacion-2026-10-03.md`
- `contracts/openapi-v2.json`
- `.github/workflows/backend-tests.yml`
- `.github/workflows/flutter-mvp.yml`
- `.github/workflows/compose-mvp.yml`
- `.github/workflows/mvp-flujo-real.yml`

---

# Conclusión

La evidencia semanal permanece histórica y auditable. Este cierre añade el estado
posterior sin modificar el significado de S8 o S9. El repositorio oficial queda con
una cadena explícita entre evolución semanal, MVP integrado, validación automática y
la única fase material todavía pendiente: **despliegue público verificable del MVP**.
