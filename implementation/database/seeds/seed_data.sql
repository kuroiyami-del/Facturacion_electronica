-- =============================================================================
-- FactuPlus - Datos de prueba para desarrollo
-- Archivo: database/seeds/seed_data.sql
-- Ejecutar DESPUÉS de schema.sql
-- Contraseña de todos los usuarios de prueba: Admin123*
-- Hash bcrypt generado con passlib: $2b$12$...
-- =============================================================================

-- Empresa de demostración
INSERT INTO empresa (nombre, nit, razon_social, direccion, ciudad, telefono, email, prefijo_factura, resolucion_dian)
VALUES (
    'FactuPlus Demo S.A.S',
    '900123456-7',
    'FACTUPLUS DEMO SOCIEDAD POR ACCIONES SIMPLIFICADA',
    'Carrera 15 # 93-75 Of. 401',
    'Bogotá D.C.',
    '601-3456789',
    'facturacion@factuplus.co',
    'FE',
    '18764000001234'
);

-- Usuario administrador (password: Admin123*)
INSERT INTO usuario (empresa_id, nombre, apellido, email, password_hash, rol)
VALUES (
    1,
    'Administrador',
    'Sistema',
    'admin@factuplus.co',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LKFDEChDSJqm9BHHC',
    'ADMIN'
);

-- Usuario facturador (password: Admin123*)
INSERT INTO usuario (empresa_id, nombre, apellido, email, password_hash, rol)
VALUES (
    1,
    'Carlos',
    'Ramírez',
    'facturador@factuplus.co',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LKFDEChDSJqm9BHHC',
    'FACTURADOR'
);

-- Clientes de prueba
INSERT INTO cliente (tipo_documento, numero_documento, tipo_persona, nombre, email, telefono, ciudad)
VALUES
    ('CC',  '12345678',       'NATURAL',   'Juan Pablo Torres',        'juan.torres@email.com',    '3001234567', 'Bogotá'),
    ('NIT', '900987654-3',    'JURIDICA',  'Comercializadora XYZ S.A.','contacto@xyz.com',         '6014567890', 'Medellín'),
    ('CC',  '87654321',       'NATURAL',   'María Fernanda López',     'maria.lopez@gmail.com',    '3109876543', 'Cali'),
    ('NIT', '800100200-1',    'JURIDICA',  'Distribuidora ABC Ltda.',  'ventas@distribuidoraabc.co','6057654321', 'Barranquilla'),
    ('CE',  'CE987654',       'NATURAL',   'Robert Johnson',           'robert.j@company.com',     '3205556677', 'Bogotá');

-- Productos de prueba
INSERT INTO producto (codigo, nombre, descripcion, precio_unitario, tipo_impuesto, porcentaje_iva, stock, unidad_medida)
VALUES
    ('PROD-001', 'Laptop Empresarial 15"',      'Laptop Core i7 16GB RAM 512GB SSD',    3500000.00, 'IVA_19', 19.00, 50,  'UND'),
    ('PROD-002', 'Mouse Inalámbrico',            'Mouse ergonómico 2.4GHz',               85000.00,  'IVA_19', 19.00, 200, 'UND'),
    ('PROD-003', 'Teclado Mecánico',             'Teclado retroiluminado Switch Blue',    220000.00, 'IVA_19', 19.00, 150, 'UND'),
    ('PROD-004', 'Monitor 24" Full HD',          'Monitor IPS 75Hz HDMI',               900000.00,  'IVA_19', 19.00, 80,  'UND'),
    ('PROD-005', 'Servicio Consultoría TI',      'Hora de consultoría tecnológica',       150000.00, 'IVA_19', 19.00, 999, 'HR'),
    ('PROD-006', 'Papel Bond Resma',             'Resma papel bond 75g 500 hojas',        18000.00,  'IVA_19', 19.00, 500, 'UND'),
    ('PROD-007', 'Software Licencia Anual',      'Licencia de uso anual FactuPlus',      480000.00,  'IVA_19', 19.00, 999, 'LIC'),
    ('PROD-008', 'Headset USB Profesional',      'Auriculares con micrófono USB',        195000.00,  'IVA_19', 19.00, 120, 'UND'),
    ('MED-001',  'Medicamento Genérico A',       'Medicamento exento de IVA',             25000.00,  'EXENTO', 0.00,  300, 'UND'),
    ('EXP-001',  'Servicio Exportación',         'Servicio para mercado internacional',   500000.00, 'IVA_0',  0.00,  999, 'SRV');