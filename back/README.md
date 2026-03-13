# Backend — Facturación Electrónica Colombia

## Requisitos
- Python 3.10+
- PostgreSQL instalado y corriendo

## Pasos para arrancar

### 1. Crear la base de datos en PostgreSQL
Abre psql o pgAdmin y ejecuta:
```sql
CREATE DATABASE facturacion_db;
```

### 2. Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
```
Edita `.env` con tus datos de PostgreSQL:
```
DATABASE_URL=postgresql://TU_USUARIO:TU_CONTRASEÑA@localhost:5432/facturacion_db
SECRET_KEY=una_clave_secreta_larga_y_aleatoria
```

### 4. Arrancar el servidor
```bash
uvicorn main:app --reload
```

### 5. Ver la documentación interactiva
Abre en tu navegador: http://localhost:8000/docs

---

## Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /auth/register | Registrar usuario |
| POST | /auth/login | Iniciar sesión |
| GET | /clients/ | Listar clientes |
| POST | /clients/ | Crear cliente |
| PUT | /clients/{id} | Actualizar cliente |
| DELETE | /clients/{id} | Eliminar cliente |
| GET | /invoices/ | Listar facturas |
| POST | /invoices/ | Crear factura |
| GET | /invoices/{id} | Detalle de factura |
| PATCH | /invoices/{id}/send | Enviar factura (DIAN) |
| GET | /products/ | Listar productos |
| POST | /products/ | Crear producto |
| GET | /dashboard/stats | Estadísticas del dashboard |

---

## Conectar con React

En tu proyecto React, crea un archivo `src/api.js`:

```javascript
const BASE_URL = "http://localhost:8000";

export async function getClients() {
  const res = await fetch(`${BASE_URL}/clients/`);
  return res.json();
}

export async function createInvoice(data) {
  const res = await fetch(`${BASE_URL}/invoices/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function getDashboardStats() {
  const res = await fetch(`${BASE_URL}/dashboard/stats`);
  return res.json();
}
```
