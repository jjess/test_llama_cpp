# Proyecto de prueba: TaskFlow API

Actúa como un ingeniero de software sénior. Construye un proyecto Python llamado `taskflow-api`, listo para ejecutarse localmente, con una arquitectura limpia, tipado, pruebas automatizadas y documentación.

No te limites a describir el código: inspecciona el repositorio, crea los archivos necesarios, ejecuta las pruebas disponibles y corrige los errores que encuentres. Si el repositorio ya contiene archivos, inspecciónalos antes de modificar nada y conserva los cambios ajenos al proyecto.

## 1. Tecnologías

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- SQLite
- Pytest y HTTPX
- Ruff para lint y formato
- PyJWT para tokens JWT
- Password hashing con una biblioteca mantenida y apropiada

Utiliza versiones compatibles entre sí y declara las dependencias en `pyproject.toml`.

## 2. Funcionalidad

Implementa una API de gestión de tareas con estos campos:

- `id`: identificador entero.
- `title`: obligatorio, entre 1 y 200 caracteres.
- `description`: opcional, máximo 5000 caracteres.
- `status`: `pending`, `in_progress` o `completed`.
- `priority`: `low`, `medium` o `high`.
- `created_at` y `updated_at`: fechas UTC.
- `due_date`: opcional.
- `owner_id`: usuario propietario.

Cada usuario debe poder consultar y modificar exclusivamente sus propias tareas.

## 3. Autenticación y seguridad

Implementa:

- Registro de usuarios.
- Inicio de sesión y emisión de JWT.
- Contraseñas almacenadas con hash seguro, nunca en texto plano.
- Validación de tokens y expiración.
- Endpoints protegidos.
- Aislamiento de tareas por propietario.
- Validación de entradas y respuestas.
- Gestión uniforme de errores.
- Secretos mediante variables de entorno, sin credenciales reales en el repositorio.

Incluye pruebas para usuarios no autenticados, tokens inválidos y accesos a tareas de otros usuarios. Evita revelar información privada al responder errores.

## 4. Endpoints

Implementa al menos:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `GET /health`

La lista de tareas debe admitir:

- Paginación con `limit` y `offset`.
- Filtrado por `status` y `priority`.
- Búsqueda por texto en título y descripción.
- Ordenación por fecha de creación o vencimiento.
- Ordenación ascendente o descendente.

Valida los parámetros y establece límites razonables para evitar peticiones excesivamente costosas.

## 5. Arquitectura

Organiza el proyecto en módulos separados para:

- Configuración.
- Base de datos y sesiones.
- Modelos ORM.
- Esquemas Pydantic.
- Autenticación y autorización.
- Lógica de negocio.
- Rutas HTTP.
- Excepciones.
- Pruebas.

Evita concentrar toda la aplicación en un único archivo. Utiliza inyección de dependencias de FastAPI y sesiones de base de datos correctamente gestionadas.

## 6. Pruebas automatizadas

Crea pruebas para:

- Registro y login correctos.
- Contraseñas incorrectas.
- Token expirado o inválido.
- Creación, consulta, actualización y borrado de tareas.
- Validación de campos y valores inválidos.
- Paginación y filtros combinados.
- Búsqueda y ordenación.
- Aislamiento entre usuarios.
- Recurso inexistente.
- Rollback o manejo de errores de base de datos cuando corresponda.

Usa una base de datos aislada para las pruebas. Las pruebas no deben depender de servicios externos ni de credenciales reales.

## 7. Calidad y documentación

Crea:

- `README.md` con instalación, configuración y ejemplos de uso.
- `.env.example` con valores ficticios y no secretos.
- `.gitignore`.
- `pyproject.toml`.
- Una estructura de carpetas clara.
- Ejemplos de peticiones HTTP.
- Instrucciones para ejecutar la aplicación y los tests.

Añade instrucciones para ejecutar Ruff y Pytest. No afirmes que las pruebas pasan si no las has ejecutado realmente.

## 8. Criterios de aceptación

El proyecto se considerará terminado cuando:

1. La aplicación arranque localmente.
2. Se pueda registrar un usuario y autenticarse.
3. Se puedan crear y administrar tareas autenticadas.
4. Ningún usuario pueda acceder a las tareas de otro.
5. Los filtros y la paginación funcionen conjuntamente.
6. Las pruebas automatizadas pasen.
7. Ruff no encuentre errores relevantes.
8. La documentación coincida con la implementación.

## 9. Forma de trabajar

Primero inspecciona el entorno y presenta un plan breve. Después implementa el proyecto por etapas, ejecutando las pruebas después de los cambios importantes.

No sustituyas la implementación por pseudocódigo ni dejes funciones esenciales con `TODO`. Si encuentras un fallo, investiga la causa y corrígelo. Evita dependencias innecesarias.

Al terminar, resume los archivos creados, los comandos ejecutados, los resultados reales de las pruebas y cualquier limitación pendiente.
