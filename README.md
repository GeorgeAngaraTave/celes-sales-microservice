

<p align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="Imagen 1" width="500"/>
</p>

# Prueba Técnica – Python Developer  
Microservicio de Ventas (FastAPI + JWT + Parquet)

Este proyecto implementa un microservicio en **FastAPI** para consultar datos de ventas almacenados en archivos **Parquet**.  
Incluye autenticación con **JWT**, conexión opcional con **Firebase Auth**, consultas con agregaciones y filtros por fechas, pruebas automatizadas y pipeline de CI.

---

## 🚀 1. Tecnologías utilizadas
- **FastAPI**
- **Python 3.10+**
- **Pandas + PyArrow**
- **JWT (JSON Web Tokens)**
- **Firebase Admin SDK** (opcional)
- **pytest**
- **Uvicorn**
- **GitHub Actions (CI)**

---

## 📁 2.Estructura del Proyecto y Descripción de Carpetas

A continuación se describe la función de cada carpeta para facilitar la
comprensión de la arquitectura:

### **`app/`**

Directorio principal del microservicio. Contiene la API, servicios,
seguridad y configuración.

### **`app/main.py`**

Punto de entrada de FastAPI.\
Registra los routers y define el endpoint raíz `/`.

### **`app/core/`**

Componentes transversales del proyecto:

-   **`config.py`**\
    Variables de entorno y parámetros globales.

-   **`security.py`**\
    Implementación del JWT (creación y validación), y esquema Bearer
    Token.

-   **`firebase.py`**\
    Validación de ID Token con Firebase Admin SDK.\
    Soporta Service Account o credenciales ADC de `gcloud`.

### **`app/api/`**

Define los endpoints del microservicio:

-   **`routes_auth.py`** -- Endpoints de autenticación\
-   **`routes_sales.py`** -- Endpoints de ventas y reportes

### **`app/services/`**

Lógica de negocio compartida:

-   **`datamart.py`** -- Lectura de Parquet, filtros y agregaciones

### **`tests/`**

Pruebas unitarias del proyecto.

-   **`test_auth.py`** -- Pruebas de autenticación\
-   **`test_sales.py`** -- Pruebas de agregación usando un datamart
    simulado

### **`.github/workflows/ci.yml`**

Pipeline CI de GitHub Actions: - Instala dependencias\
- Ejecuta flake8\
- Corre pytest

### **`data/` (ignorada por Git)**

Carpeta donde se colocan los archivos `.parquet`.

```
app/
  main.py
  core/
    config.py
    security.py
    firebase.py
  api/
    routes_auth.py
    routes_sales.py
  services/
    datamart.py
tests/
  test_auth.py
  test_sales.py
.github/workflows/ci.yml
README.md
```

---

## ⚙️ 3. Configuración del entorno

### Archivo `.env`
```
SECRET_KEY=prueba-celes-123
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATAMART_PATH=./data

# conexión a Firebase
FIREBASE_PROJECT_ID=tu-proyecto
FIREBASE_CREDENTIALS_FILE=./firebase-service-account.json
```
- `DATAMART_PATH` apunta a la carpeta donde dejaste los `.parquet` (`data_chunk*.parquet`).

> 💡 Si cambiaste el nombre de columnas en el código (archivo `app/services/datamart.py`), ajusta también aquí
> las instrucciones de negocio según el esquema real de tu datamart.
---

## 📦 4. Instalación

```bash
pip install -r requirements.txt
```

Crear carpeta `/data/` y colocar los archivos Parquet:
> ⚠️ La carpeta `data/` (donde van los `.parquet`) **no** se versiona. Debes crearla localmente en la raíz del proyecto
> y copiar allí los archivos descomprimidos del ZIP entregado en la prueba.

```
data_chunk000000000000.snappy.parquet
data_chunk000000000001.snappy.parquet
...
```

Ejecutar el servidor:

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs  
Redoc: http://localhost:8000/redoc  

---

## 🔐 5. Autenticación

### A) Login local (pruebas)
```
POST /auth/login
username=admin
password=admin
```

### B) Login con Firebase
```
POST /auth/firebase
{
  "id_token": "ID_TOKEN_FIREBASE"
}
```

## Generar id_token usando la API REST de Firebase (sin front)

Puedes obtener el id_token llamando al REST API de Firebase Auth (Identity Toolkit) desde Postman, curl o Python.

### Llamar al endpoint REST signInWithPassword

```
curl "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=TU_API_KEY" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"123456\",\"returnSecureToken\":true}"

```

---

## 🛡 6. Uso del JWT

Todos los endpoints requieren:

```
Authorization: Bearer <access_token>
```

En Swagger se usa el botón **Authorize**.

---

## 📊 7. Endpoints

### ➤ `GET /`
```
{ "message": "Prueba Técnica - Python Developer" }
```
Todos los endpoints aceptan un rango de fechas opcional (`start_date`, `end_date`) en formato `YYYY-MM-DD`.

### ➤ Ventas agrupadas
- `GET /sales/employee`  
  Ventas por empleado (`KeyEmployee`) en un periodo.

- `GET /sales/product`  
  Ventas por producto (`KeyProduct`) en un periodo.

- `GET /sales/store`  
  Ventas por tienda (`KeyStore`) en un periodo.

### ➤ Resumen (total + promedio)
- `GET /sales/employee/summary`  
  Venta **total** y **promedio** por empleado.

- `GET /sales/product/summary`  
  Venta **total** y **promedio** por producto.

- `GET /sales/store/summary`  
  Venta **total** y **promedio** por tienda.

Parámetros:
```
?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
> 🔁 Todos los endpoints usan el mismo motor de agregación sobre el datamart para facilitar mantenimiento.

---

## 🧪 8. Pruebas

```bash
pytest
```

Incluye:
- Autenticación
- Generación y validación de JWT
- Agregación de ventas

---

## 🔄 9. CI / GitHub Actions

`ci.yml` ejecuta:
1. Instalación de dependencias  
2. Linter (flake8)  
3. Pruebas (pytest)

---

## 🏁 10. Resultado

Este microservicio cumple con:

✔ JWT propio  
✔ Integración opcional con Firebase  
✔ Lectura de Parquet  
✔ Agregaciones por dimensiones  
✔ Seguridad con Bearer Token  
✔ Pruebas unitarias  
✔ CI/CD  
✔ Endpoint raíz `/`  

---

**Autor:**  
Jorge Luis Angarita Tavera  
Python Developer – Prueba Técnica
