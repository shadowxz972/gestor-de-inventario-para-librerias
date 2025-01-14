

# Gestor de inventario para librerias

---
## Descripción

Este proyecto es una **API RESTful** construida con **FastAPI** y **SQLAlchemy**. Gestiona libros y ventas de los libros. Además, permite la gestión de usuarios y autenticación mediante tokens JWT. Proporciona endpoints protegidos que solo son accesibles mediante un sistema de autenticación basado en roles (usuarios normales y administradores).

### Funcionalidades principales

- **Autenticación con JWT**:
  - Generación de tokens de acceso para usuarios autenticados.
  - Protección de rutas según el rol (`is_admin`).
- **Gestión de usuarios**:
  - Crear, leer, actualizar y eliminar usuarios.
  - Creación automática de un usuario administrador por defecto.
- **Gestion de libros**
  - Crear, leer, actualizar y eliminar libros.
- **Gestion de ventas**
  - Crear, leer, actualizar y eliminar ventas.
  - Actualiza la cantidad de libros de acuerdo a la cantidad vendida.
- **Swagger UI**:
  - Documentación interactiva para probar los endpoints disponibles.

---

## Requisitos

Asegúrate de tener instalados los siguientes programas antes de iniciar el proyecto:

- **Python 3.10+**
- requirements.txt

---

## Instalación y configuración

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/shadowxz972/gestor-de-inventario-para-librerias.git
   cd gestor-de-inventario-para-librerias
   ```

2. **Crear un entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```


## Uso

1. **Ejecutar el servidor**:

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Acceso a la API**:

   Una vez el servidor esté activo, puedes acceder al siguiente endpoint:

   - **Swagger UI**: `http://127.0.0.1:8000/docs`

3. **Endpoints importantes**:

   | Método | Endpoint                  | Descripción                                   |
   |--------|---------------------------|-----------------------------------------------|
   | POST   | `/auth/login`             | Autenticar un usuario y obtener un token JWT. |
   | POST   | `/users/create`           | Crear un nuevo usuario.                       |
   | DELETE | `/users/delete/{user_id}` | Eliminar un usuario (borrado lógico).         |
   | PUT    | `/users/change_password`  | Cambia la contraseña del usuario logueado.    |

---

## Pruebas

Para probar la API, puedes usar las siguientes herramientas:

- **Swagger UI**: Accede a la documentación interactiva y prueba los endpoints directamente desde tu navegador.
- **Postman** o **cURL**: Realiza solicitudes manuales a los endpoints protegidos.

---


## Estructura del proyecto

```
.
├── app
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── auth
│   │   ├── config.py            # Configuraciones de seguridad
│   │   └── functions.py         # Funciones de seguridad
│   ├── crud
│   │   └── ...                  # Funciones crud para los modelos
│   ├── database
│   │   └── config.py            # Configuración de la base de datos
│   ├── models
│   │   └── ...                  # Modelos de SQL Alchemy
│   ├── routers
│   │   └── ...                  # Endpoints
│   ├── schemas
│   │   └── ...                  # Esquemas para validación con pydantic
│   ├── validators
│   │   ├── constants.py         # Constantes
│   │   └── ...                  # Funciones validadoras para los modelos
│   └── utils.py                 # Utilidades extras para la aplicacion
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos para ignorar en el git
└── README.md                    # Documentación del proyecto
```
