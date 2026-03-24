Actúa como un Arquitecto de Software Senior y Desarrollador Full-Stack. Tu objetivo es implementar el sistema "FactuPlus", un software de facturación electrónica basado en la documentación técnica proporcionada
.
1. Arquitectura y Tecnologías:
Arquitectura: Basada en capas (Frontend, Backend, Base de Datos)
.
Frontend: React
.
Backend: Python con FastAPI
.
Base de Datos: PostgreSQL gestionado a través de Supabase
.
2. Requerimientos Clave:
Implementar módulos para la gestión de Usuarios (Auth/Login), Clientes, Productos y Facturas
.
El sistema debe permitir crear facturas electrónicas, agregar múltiples productos, calcular totales e impuestos automáticamente, y consultar el historial de ventas
.
Debe incluir un simulacro de integración con un Servidor DIAN para validar y autorizar facturas
.
3. Patrones de Diseño a Aplicar (Obligatorio):
Singleton: Para la conexión centralizada a la base de datos en el backend
.
Factory: Para la creación de diferentes tipos de facturas (estándar, con impuestos, con descuentos)
.
Repository: Para separar la lógica de negocio del acceso a datos (UsuarioRepository, ClienteRepository, FacturaRepository)
.
Observer: Para notificar automáticamente a otros módulos cuando se genera una factura
.
Strategy: Para implementar diferentes algoritmos de cálculo de impuestos (IVA, Retención, Descuentos)
.
4. Estructura de Datos: Implementar las tablas siguiendo el diseño relacional: empresa, usuario, cliente, producto, factura, detalle_factura y pago
.
5. Estándares de Código: Aplica principios SOLID (especialmente SRP y DIP) y prácticas de Clean Code (nombres descriptivos, funciones pequeñas y sin duplicación de código)
.
Tarea Inicial: Genera la estructura de carpetas sugerida (backend, frontend, database), los modelos de base de datos en SQLAlchemy (o similar para FastAPI) y la lógica de conexión usando el patrón Singleton.
