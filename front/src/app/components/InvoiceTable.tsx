import { Eye, Edit2, Download, MoreVertical } from 'lucide-react';

interface Invoice {
  id: string;
  numero: string;
  cliente: string;
  fecha: string;
  estado: 'emitida' | 'pendiente' | 'rechazada';
  total: number;
}

const invoices: Invoice[] = [
  { id: '1', numero: 'FAC-2026-001', cliente: 'Corporación ABC S.A.', fecha: '2026-03-10', estado: 'emitida', total: 15420.50 },
  { id: '2', numero: 'FAC-2026-002', cliente: 'Inversiones XYZ Ltda.', fecha: '2026-03-11', estado: 'emitida', total: 8750.00 },
  { id: '3', numero: 'FAC-2026-003', cliente: 'Comercial El Progreso', fecha: '2026-03-12', estado: 'pendiente', total: 22300.75 },
  { id: '4', numero: 'FAC-2026-004', cliente: 'Tecnología Digital S.A.', fecha: '2026-03-12', estado: 'rechazada', total: 5890.25 },
  { id: '5', numero: 'FAC-2026-005', cliente: 'Distribuidora Nacional', fecha: '2026-03-13', estado: 'emitida', total: 31200.00 },
  { id: '6', numero: 'FAC-2026-006', cliente: 'Industrias del Sur', fecha: '2026-03-13', estado: 'pendiente', total: 12450.50 },
  { id: '7', numero: 'FAC-2026-007', cliente: 'Grupo Empresarial Norte', fecha: '2026-03-13', estado: 'emitida', total: 18990.00 },
];

export function InvoiceTable() {
  const getStatusColor = (estado: Invoice['estado']) => {
    switch (estado) {
      case 'emitida':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'pendiente':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'rechazada':
        return 'bg-red-100 text-red-700 border-red-200';
    }
  };

  const getStatusLabel = (estado: Invoice['estado']) => {
    switch (estado) {
      case 'emitida':
        return 'Emitida';
      case 'pendiente':
        return 'Pendiente';
      case 'rechazada':
        return 'Rechazada';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 2,
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(date);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-4 text-left text-gray-700">Número de Factura</th>
              <th className="px-6 py-4 text-left text-gray-700">Cliente</th>
              <th className="px-6 py-4 text-left text-gray-700">Fecha</th>
              <th className="px-6 py-4 text-left text-gray-700">Estado</th>
              <th className="px-6 py-4 text-right text-gray-700">Valor Total</th>
              <th className="px-6 py-4 text-center text-gray-700">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {invoices.map((invoice) => (
              <tr key={invoice.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <span className="text-blue-600">{invoice.numero}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-gray-900">{invoice.cliente}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-gray-600">{formatDate(invoice.fecha)}</span>
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full border ${getStatusColor(invoice.estado)}`}>
                    {getStatusLabel(invoice.estado)}
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <span className="text-gray-900">{formatCurrency(invoice.total)}</span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center justify-center gap-2">
                    <button
                      title="Ver detalles"
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      title="Editar factura"
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      title="Descargar"
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      <Download className="w-4 h-4" />
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
  );
}
