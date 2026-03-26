Iteración 1: Implementación del Motor de Cálculo (Patrón Strategy)
"Basado en la estructura actual del backend, implementa el Patrón Strategy para el cálculo de totales. Crea estrategias para CalculoIVA, CalculoRetencion y CalculoDescuento, asegurando que la clase Factura pueda intercambiarlas según sea necesario para cumplir con el RF7"
.
Iteración 2: Generación de Facturas y Patrón Factory
"Implementa la lógica de creación de facturas utilizando el Patrón Factory. Crea una FacturaFactory que reciba un tipo de factura y genere la instancia correcta (estándar o con impuestos). Asegúrate de que cada factura nueva dispare un evento de notificación usando el Patrón Observer"
.
Iteración 3: Integración con el Simulacro DIAN
"Crea un servicio que simule el componente externo 'Servidor DIAN'. Debe tener métodos para validarFactura() y autorizarFactura(). Integra este servicio en el flujo de guardado de facturas, de modo que una factura solo se marque como 'Aprobada' si la DIAN responde exitosamente"
.
Iteración 4: Interfaz de Usuario y Reportes
"En el frontend de React, desarrolla el formulario de creación de facturas. Debe permitir seleccionar un cliente de una lista, buscar productos dinámicamente, mostrar un resumen visual antes de guardar y permitir la descarga de la factura en formato digital (PDF)"
.
Iteración 5: Refactorización a Patrón Repository
"Refactoriza el acceso a la base de datos en el backend utilizando el Patrón Repository. Crea repositorios específicos para Clientes y Facturas para asegurar que el controlador de FastAPI no interactúe directamente con la base de datos, cumpliendo así con el Principio de Inversión de Dependencias (DIP)"