# FactuPlus — Sistema de Facturación Electrónica

> Software de facturación electrónica con integración DIAN (simulacro).  
> Stack: **React + FastAPI + PostgreSQL (Supabase)**

---

## Patrones de Diseño Implementados

| Patrón | Ubicación | Propósito |
|--------|-----------|-----------|
| **Singleton** | `app/database/connection.py` | Una única instancia del motor de BD en toda la aplicación |
| **Factory** | `app/factories/factura_factory.py` | Creación de facturas: Estándar, Con Descuento, Con Retención, Exportación |
| **Repository** | `app/repositories/` | Abstracción del acceso a datos: `UsuarioRepository`, `ClienteRepository`, `ProductoRepository`, `FacturaRepository` |
| **Observer** | `app/services/observers/factura_observer.py` | Notificaciones automáticas: Email, Inventario, Auditoría, DIAN |
| **Strategy** | `app/strategies/impuesto_strategy.py` | Algoritmos de cálculo: IVA 0%, IVA 5%, IVA 19%, Retención, Descuento |

---

## Estructura del Proyecto

```
factuplus/
├── backend/
│   ├── app/
│   │   ├── config.py                          # Configuración centralizada (Settings)
│   │   ├── main.py                            # Punto de entrada FastAPI
│   │   ├── database/
│   │   │   ├── base.py                        # Base declarativa SQLAlchemy
│   │   │   └── connection.py                  # ★ Patrón Singleton
│   │   ├── models/
│   │   │   ├── empresa.py
│   │   │   ├── usuario.py
│   │   │   ├── cliente.py
│   │   │   ├── producto.py
│   │   │   ├── factura.py                     # Factura + DetalleFactura
│   │   │   └── pago.py
│   │   ├── repositories/
│   │   │   ├── base_repository.py             # ★ Patrón Repository (genérico)
│   │   │   ├── usuario_repository.py
│   │   │   ├── cliente_repository.py
│   │   │   ├── producto_repository.py
│   │   │   └── factura_repository.py
│   │   ├── factories/
│   │   │   └── factura_factory.py             # ★ Patrón Factory
│   │   ├── strategies/
│   │   │   └── impuesto_strategy.py           # ★ Patrón Strategy
│   │   ├── services/
│   │   │   ├── auth_service.py                # JWT + bcrypt
│   │   │   ├── dian_service.py                # Simulacro DIAN + CUFE
│   │   │   ├── factura_service.py             # Orquestador principal
│   │   │   └── observers/
│   │   │       └── factura_observer.py        # ★ Patrón Observer
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── clientes.py
│   │   │   ├── productos.py
│   │   │   ├── facturas.py
│   │   │   └── dependencies.py                # Inyección de dependencias JWT
│   │   └── schemas/
│   │       └── schemas.py                     # Pydantic v2 schemas
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js                      # Axios + helpers por módulo
│   │   ├── context/
│   │   │   └── AuthContext.jsx                # Context API para autenticación
│   │   ├── components/
│   │   │   └── Layout/
│   │   │       └── Layout.jsx                 # Sidebar + Topbar
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── ClientesPage.jsx
│   │   │   ├── ProductosPage.jsx
│   │   │   ├── FacturasPage.jsx
│   │   │   └── NuevaFacturaPage.jsx
│   │   ├── utils/
│   │   │   └── formatters.js                  # formatCOP, formatDate, badges
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── Dockerfile
├── database/
│   ├── schema.sql                             # DDL completo con ENUMs, índices y triggers
│   └── seeds/
│       └── seed_data.sql                      # Datos de prueba
├── docker-compose.yml
└── README.md
```

---

## Inicio Rápido

### Opción A — Docker Compose (recomendado)

```bash
# Clonar e iniciar
git clone <repo>
cd factuplus
docker-compose up --build

# URLs disponibles:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/api/docs
```

### Opción B — Desarrollo local

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu DATABASE_URL de Supabase

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
# Disponible en http://localhost:3000
```

---

## Configuración de Supabase

1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ir a **SQL Editor** y ejecutar `database/schema.sql`
3. Luego ejecutar `database/seeds/seed_data.sql`
4. Copiar la **Connection String** (URI format) desde Settings → Database
5. Pegar en el `.env` del backend como `DATABASE_URL`

```env
DATABASE_URL=postgresql://postgres.[ref]:[pass]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

---

## Credenciales de Prueba

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| Admin | `admin@factuplus.co` | `Admin123*` | ADMIN |
| Facturador | `facturador@factuplus.co` | `Admin123*` | FACTURADOR |

---

## API Endpoints Principales

```
POST   /api/v1/auth/login          — Autenticación JWT
POST   /api/v1/auth/register       — Registro de usuario

GET    /api/v1/clientes            — Listar clientes
POST   /api/v1/clientes            — Crear cliente
PUT    /api/v1/clientes/{id}       — Actualizar cliente
DELETE /api/v1/clientes/{id}       — Eliminar (soft delete)

GET    /api/v1/productos           — Listar productos
POST   /api/v1/productos           — Crear producto

GET    /api/v1/facturas            — Historial de facturas
POST   /api/v1/facturas            — Crear factura (BORRADOR)
POST   /api/v1/facturas/{id}/emitir  — Emitir + validar DIAN
POST   /api/v1/facturas/{id}/anular  — Anular factura
GET    /api/v1/facturas/resumen    — Resumen de ventas por período
```

Documentación interactiva Swagger disponible en `/api/docs`.

---

## Flujo de una Factura Electrónica

```
1. POST /facturas        → Estado: BORRADOR
       ↓
   Factory selecciona tipo (Estándar / Descuento / Retención / Exportación)
   Strategy calcula IVA y descuentos línea por línea
       ↓
2. POST /facturas/{id}/emitir → Estado: EMITIDA
       ↓
   Observer notifica: Email + Inventario + Auditoría + DIAN
       ↓
3. DianService genera CUFE (SHA-384) + valida (simulacro)
       ↓
4. Estado final: VALIDADA_DIAN ✓  o  RECHAZADA ✗
```

---

## Principios SOLID Aplicados

- **SRP** — Cada clase tiene una única responsabilidad (modelos, repositorios, servicios y estrategias son independientes)
- **OCP** — Nuevos tipos de factura se agregan registrando un Factory sin modificar el existente
- **LSP** — Todos los repositorios son intercambiables ya que heredan de `BaseRepository`
- **ISP** — Los observadores solo implementan el método `actualizar()` que necesitan
- **DIP** — `FacturaService` depende de abstracciones (`FacturaRepository`, `FacturaCreator`) no de implementaciones concretas