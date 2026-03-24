-- =============================================================================
-- FactuPlus - Esquema de Base de Datos PostgreSQL / Supabase
-- Archivo: database/schema.sql
-- Descripción: Crea todas las tablas, índices, constraints y tipos ENUM.
-- =============================================================================

-- Habilitar extensión para UUIDs (opcional, usamos SERIAL por defecto)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- TIPOS ENUM
-- =============================================================================

CREATE TYPE rol_usuario      AS ENUM ('ADMIN', 'FACTURADOR', 'AUDITOR');
CREATE TYPE tipo_documento   AS ENUM ('CC', 'NIT', 'CE', 'PA', 'TI');
CREATE TYPE tipo_persona     AS ENUM ('NATURAL', 'JURIDICA');
CREATE TYPE tipo_impuesto    AS ENUM ('IVA_0', 'IVA_5', 'IVA_19', 'EXENTO', 'EXCLUIDO');
CREATE TYPE estado_factura   AS ENUM ('BORRADOR', 'EMITIDA', 'VALIDADA_DIAN', 'RECHAZADA', 'ANULADA');
CREATE TYPE tipo_factura     AS ENUM ('ESTANDAR', 'CON_DESCUENTO', 'CON_RETENCION', 'EXPORTACION');
CREATE TYPE medio_pago       AS ENUM ('EFECTIVO', 'TRANSFERENCIA', 'TARJETA_CREDITO', 'TARJETA_DEBITO', 'CHEQUE', 'CREDITO');
CREATE TYPE estado_pago      AS ENUM ('PENDIENTE', 'PAGADO', 'PARCIAL', 'VENCIDO');

-- =============================================================================
-- TABLA: empresa
-- =============================================================================

CREATE TABLE IF NOT EXISTS empresa (
    id                  SERIAL PRIMARY KEY,
    nombre              VARCHAR(200)    NOT NULL,
    nit                 VARCHAR(20)     NOT NULL UNIQUE,
    razon_social        VARCHAR(300)    NOT NULL,
    direccion           VARCHAR(300),
    ciudad              VARCHAR(100),
    telefono            VARCHAR(20),
    email               VARCHAR(150),
    regimen             VARCHAR(50)     NOT NULL DEFAULT 'RESPONSABLE_IVA',
    activa              BOOLEAN         NOT NULL DEFAULT TRUE,
    prefijo_factura     VARCHAR(10)     NOT NULL DEFAULT 'FE',
    consecutivo_actual  INTEGER         NOT NULL DEFAULT 1,
    resolucion_dian     VARCHAR(100),
    logo_url            TEXT,
    created_at          TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_empresa_nit ON empresa(nit);

-- =============================================================================
-- TABLA: usuario
-- =============================================================================

CREATE TABLE IF NOT EXISTS usuario (
    id              SERIAL PRIMARY KEY,
    empresa_id      INTEGER         NOT NULL REFERENCES empresa(id) ON DELETE CASCADE,
    nombre          VARCHAR(150)    NOT NULL,
    apellido        VARCHAR(150)    NOT NULL,
    email           VARCHAR(150)    NOT NULL UNIQUE,
    password_hash   VARCHAR(255)    NOT NULL,
    rol             rol_usuario     NOT NULL DEFAULT 'FACTURADOR',
    activo          BOOLEAN         NOT NULL DEFAULT TRUE,
    ultimo_login    TIMESTAMP,
    created_at      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_usuario_email      ON usuario(email);
CREATE INDEX idx_usuario_empresa_id ON usuario(empresa_id);

-- =============================================================================
-- TABLA: cliente
-- =============================================================================

CREATE TABLE IF NOT EXISTS cliente (
    id                  SERIAL PRIMARY KEY,
    tipo_documento      tipo_documento  NOT NULL DEFAULT 'CC',
    numero_documento    VARCHAR(30)     NOT NULL UNIQUE,
    tipo_persona        tipo_persona    NOT NULL DEFAULT 'NATURAL',
    nombre              VARCHAR(200)    NOT NULL,
    razon_social        VARCHAR(300),
    email               VARCHAR(150),
    telefono            VARCHAR(20),
    direccion           VARCHAR(300),
    ciudad              VARCHAR(100),
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cliente_documento ON cliente(numero_documento);
CREATE INDEX idx_cliente_nombre    ON cliente(LOWER(nombre));

-- =============================================================================
-- TABLA: producto
-- =============================================================================

CREATE TABLE IF NOT EXISTS producto (
    id                  SERIAL PRIMARY KEY,
    codigo              VARCHAR(50)     NOT NULL UNIQUE,
    nombre              VARCHAR(200)    NOT NULL,
    descripcion         VARCHAR(500),
    precio_unitario     NUMERIC(15,2)   NOT NULL,
    tipo_impuesto       tipo_impuesto   NOT NULL DEFAULT 'IVA_19',
    porcentaje_iva      NUMERIC(5,2)    NOT NULL DEFAULT 19.00,
    stock               INTEGER         NOT NULL DEFAULT 0,
    unidad_medida       VARCHAR(30)     NOT NULL DEFAULT 'UND',
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_producto_codigo ON producto(codigo);
CREATE INDEX idx_producto_nombre ON producto(LOWER(nombre));

-- =============================================================================
-- TABLA: factura
-- =============================================================================

CREATE TABLE IF NOT EXISTS factura (
    id                  SERIAL PRIMARY KEY,
    empresa_id          INTEGER             NOT NULL REFERENCES empresa(id),
    cliente_id          INTEGER             NOT NULL REFERENCES cliente(id),
    usuario_id          INTEGER             NOT NULL REFERENCES usuario(id),
    numero_factura      VARCHAR(30)         NOT NULL UNIQUE,
    tipo_factura        tipo_factura        NOT NULL DEFAULT 'ESTANDAR',
    estado              estado_factura      NOT NULL DEFAULT 'BORRADOR',
    fecha_emision       DATE                NOT NULL DEFAULT CURRENT_DATE,
    fecha_vencimiento   DATE,
    subtotal            NUMERIC(15,2)       NOT NULL DEFAULT 0.00,
    descuento_total     NUMERIC(15,2)       NOT NULL DEFAULT 0.00,
    base_gravable       NUMERIC(15,2)       NOT NULL DEFAULT 0.00,
    iva_total           NUMERIC(15,2)       NOT NULL DEFAULT 0.00,
    retencion_total     NUMERIC(15,2)       NOT NULL DEFAULT 0.00,
    total               NUMERIC(15,2)       NOT NULL DEFAULT 0.00,
    cufe                VARCHAR(200),
    qr_code             TEXT,
    validada_dian       BOOLEAN             NOT NULL DEFAULT FALSE,
    respuesta_dian      TEXT,
    notas               TEXT,
    created_at          TIMESTAMP           NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP           NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_factura_numero     ON factura(numero_factura);
CREATE INDEX idx_factura_cliente    ON factura(cliente_id);
CREATE INDEX idx_factura_fecha      ON factura(fecha_emision);
CREATE INDEX idx_factura_estado     ON factura(estado);
CREATE INDEX idx_factura_empresa    ON factura(empresa_id);

-- =============================================================================
-- TABLA: detalle_factura
-- =============================================================================

CREATE TABLE IF NOT EXISTS detalle_factura (
    id                      SERIAL PRIMARY KEY,
    factura_id              INTEGER         NOT NULL REFERENCES factura(id) ON DELETE CASCADE,
    producto_id             INTEGER         NOT NULL REFERENCES producto(id),
    cantidad                NUMERIC(10,3)   NOT NULL,
    precio_unitario         NUMERIC(15,2)   NOT NULL,
    porcentaje_descuento    NUMERIC(5,2)    NOT NULL DEFAULT 0.00,
    valor_descuento         NUMERIC(15,2)   NOT NULL DEFAULT 0.00,
    subtotal                NUMERIC(15,2)   NOT NULL,
    porcentaje_iva          NUMERIC(5,2)    NOT NULL DEFAULT 19.00,
    valor_iva               NUMERIC(15,2)   NOT NULL DEFAULT 0.00,
    total_linea             NUMERIC(15,2)   NOT NULL
);

CREATE INDEX idx_detalle_factura_id  ON detalle_factura(factura_id);
CREATE INDEX idx_detalle_producto_id ON detalle_factura(producto_id);

-- =============================================================================
-- TABLA: pago
-- =============================================================================

CREATE TABLE IF NOT EXISTS pago (
    id          SERIAL PRIMARY KEY,
    factura_id  INTEGER         NOT NULL REFERENCES factura(id) ON DELETE CASCADE,
    fecha_pago  DATE            NOT NULL DEFAULT CURRENT_DATE,
    monto       NUMERIC(15,2)   NOT NULL,
    medio_pago  medio_pago      NOT NULL DEFAULT 'EFECTIVO',
    estado      estado_pago     NOT NULL DEFAULT 'PENDIENTE',
    referencia  VARCHAR(100),
    notas       TEXT,
    created_at  TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pago_factura_id ON pago(factura_id);

-- =============================================================================
-- FUNCIÓN: updated_at automático
-- =============================================================================

CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a tablas con updated_at
DO $$
DECLARE
    tbl TEXT;
BEGIN
    FOREACH tbl IN ARRAY ARRAY['empresa','usuario','cliente','producto','factura']
    LOOP
        EXECUTE format(
            'CREATE TRIGGER set_updated_at
             BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();',
            tbl
        );
    END LOOP;
END;
$$;