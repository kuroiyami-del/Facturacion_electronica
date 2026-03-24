import { Plus, Filter, Download } from 'lucide-react';
import { InvoiceTable } from '../components/InvoiceTable';

export function InvoicesPage() {
  return (
    <div className="p-6">
      {/* Encabezado de sección */}
      <div className="mb-6">
        <h1 className="text-gray-900 mb-2">Gestión de Facturas</h1>
        <p className="text-gray-600">Administra y controla todas tus facturas electrónicas</p>
      </div>

      {/* Acciones y filtros */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
        <div className="flex flex-wrap items-center gap-3">
          <button className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all shadow-md hover:shadow-lg">
            <Plus className="w-4 h-4" />
            <span>Crear Nueva Factura</span>
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

        <div className="flex items-center gap-2">
          <span className="text-gray-600">Mostrar:</span>
          <select className="px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option>Todas</option>
            <option>Emitidas</option>
            <option>Pendientes</option>
            <option>Rechazadas</option>
          </select>
        </div>
      </div>

      {/* Tabla de facturas */}
      <InvoiceTable />

      {/* Paginación */}
      <div className="mt-6 flex items-center justify-between">
        <p className="text-gray-600">
          Mostrando 1-7 de 247 facturas
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
