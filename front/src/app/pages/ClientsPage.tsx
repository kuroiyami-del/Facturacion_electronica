import { Plus, Filter, Download, Mail, Phone, MapPin, Edit2, Trash2, MoreVertical } from 'lucide-react';

interface Client {
  id: string;
  nombre: string;
  nit: string;
  email: string;
  telefono: string;
  ciudad: string;
  totalFacturas: number;
  totalCompras: number;
}

const clients: Client[] = [
  {
    id: '1',
    nombre: 'Corporación ABC S.A.',
    nit: '900.123.456-7',
    email: 'contacto@abc.com',
    telefono: '+57 310 234 5678',
    ciudad: 'Bogotá',
    totalFacturas: 45,
    totalCompras: 15420500,
  },
  {
    id: '2',
    nombre: 'Inversiones XYZ Ltda.',
    nit: '800.987.654-3',
    email: 'info@xyz.com',
    telefono: '+57 315 876 5432',
    ciudad: 'Medellín',
    totalFacturas: 32,
    totalCompras: 8750000,
  },
  {
    id: '3',
    nombre: 'Comercial El Progreso',
    nit: '700.456.789-1',
    email: 'ventas@progreso.com',
    telefono: '+57 320 567 8901',
    ciudad: 'Cali',
    totalFacturas: 28,
    totalCompras: 22300750,
  },
  {
    id: '4',
    nombre: 'Tecnología Digital S.A.',
    nit: '600.321.654-9',
    email: 'digital@tecnologia.com',
    telefono: '+57 318 432 1098',
    ciudad: 'Barranquilla',
    totalFacturas: 15,
    totalCompras: 5890250,
  },
  {
    id: '5',
    nombre: 'Distribuidora Nacional',
    nit: '500.789.123-5',
    email: 'contacto@distribuidora.com',
    telefono: '+57 312 789 0123',
    ciudad: 'Cartagena',
    totalFacturas: 52,
    totalCompras: 31200000,
  },
];

export function ClientsPage() {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  return (
    <div className="p-6">
      {/* Encabezado de sección */}
      <div className="mb-6">
        <h1 className="text-gray-900 mb-2">Gestión de Clientes</h1>
        <p className="text-gray-600">Administra tu base de datos de clientes</p>
      </div>

      {/* Estadísticas rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Mail className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-gray-500">Total Clientes</p>
              <h3 className="text-gray-900">89</h3>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Phone className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-gray-500">Clientes Activos</p>
              <h3 className="text-gray-900">67</h3>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <MapPin className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-gray-500">Ciudades</p>
              <h3 className="text-gray-900">12</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Acciones y filtros */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
        <div className="flex flex-wrap items-center gap-3">
          <button className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all shadow-md hover:shadow-lg">
            <Plus className="w-4 h-4" />
            <span>Agregar Cliente</span>
          </button>
          <button className="inline-flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Filter className="w-4 h-4" />
            <span>Filtrar</span>
          </button>
          <button className="inline-flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Download className="w-4 h-4" />
            <span>Exportar</span>
          </button>
        </div>

        <div className="relative">
          <input
            type="text"
            placeholder="Buscar cliente..."
            className="pl-4 pr-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
          />
        </div>
      </div>

      {/* Tabla de clientes */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 text-left text-gray-700">Cliente</th>
                <th className="px-6 py-4 text-left text-gray-700">NIT</th>
                <th className="px-6 py-4 text-left text-gray-700">Contacto</th>
                <th className="px-6 py-4 text-left text-gray-700">Ciudad</th>
                <th className="px-6 py-4 text-right text-gray-700">Total Facturas</th>
                <th className="px-6 py-4 text-right text-gray-700">Total Compras</th>
                <th className="px-6 py-4 text-center text-gray-700">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {clients.map((client) => (
                <tr key={client.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    <span className="text-gray-900">{client.nombre}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-gray-600">{client.nit}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 text-gray-600 text-sm">
                        <Mail className="w-3 h-3" />
                        {client.email}
                      </div>
                      <div className="flex items-center gap-2 text-gray-600 text-sm">
                        <Phone className="w-3 h-3" />
                        {client.telefono}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin className="w-4 h-4" />
                      {client.ciudad}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className="text-gray-900">{client.totalFacturas}</span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className="text-gray-900">{formatCurrency(client.totalCompras)}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center justify-center gap-2">
                      <button
                        title="Editar cliente"
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        title="Eliminar cliente"
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                      <button
                        title="Más opciones"
                        className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      >
                        <MoreVertical className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Paginación */}
      <div className="mt-6 flex items-center justify-between">
        <p className="text-gray-600">
          Mostrando 1-5 de 89 clientes
        </p>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            Anterior
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            1
          </button>
          <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            2
          </button>
          <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            3
          </button>
          <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            Siguiente
          </button>
        </div>
      </div>
    </div>
  );
}
