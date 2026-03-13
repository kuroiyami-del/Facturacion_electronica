import { TrendingUp, FileText, Users, DollarSign, ArrowUpRight, ArrowDownRight } from 'lucide-react';

export function DashboardPage() {
  const stats = [
    {
      title: 'Total Facturas',
      value: '247',
      icon: FileText,
      change: '+12%',
      isPositive: true,
      color: 'blue',
    },
    {
      title: 'Ingresos Totales',
      value: '$124,580,250',
      icon: DollarSign,
      change: '+8%',
      isPositive: true,
      color: 'green',
    },
    {
      title: 'Pendientes',
      value: '18',
      icon: FileText,
      change: '-5%',
      isPositive: true,
      color: 'yellow',
    },
    {
      title: 'Clientes Activos',
      value: '89',
      icon: Users,
      change: '+15%',
      isPositive: true,
      color: 'purple',
    },
  ];

  const recentInvoices = [
    { id: 'FAC-2026-005', cliente: 'Distribuidora Nacional', monto: 31200.00, estado: 'emitida' },
    { id: 'FAC-2026-006', cliente: 'Industrias del Sur', monto: 12450.50, estado: 'pendiente' },
    { id: 'FAC-2026-007', cliente: 'Grupo Empresarial Norte', monto: 18990.00, estado: 'emitida' },
  ];

  const getColorClasses = (color: string) => {
    const colors: Record<string, { bg: string; icon: string }> = {
      blue: { bg: 'bg-blue-100', icon: 'text-blue-600' },
      green: { bg: 'bg-green-100', icon: 'text-green-600' },
      yellow: { bg: 'bg-yellow-100', icon: 'text-yellow-600' },
      purple: { bg: 'bg-purple-100', icon: 'text-purple-600' },
    };
    return colors[color] || colors.blue;
  };

  const getStatusColor = (estado: string) => {
    switch (estado) {
      case 'emitida':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'pendiente':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 2,
    }).format(amount);
  };

  return (
    <div className="p-6">
      {/* Encabezado */}
      <div className="mb-6">
        <h1 className="text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Resumen general de tu sistema de facturación</p>
      </div>

      {/* Tarjetas de estadísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          const colors = getColorClasses(stat.color);

          return (
            <div key={stat.title} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${colors.bg} rounded-lg flex items-center justify-center`}>
                  <Icon className={`w-6 h-6 ${colors.icon}`} />
                </div>
                <span className={`flex items-center text-xs gap-1 ${stat.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                  {stat.isPositive ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                  {stat.change}
                </span>
              </div>
              <h3 className="text-gray-900 mb-1">{stat.title}</h3>
              <p className="text-gray-600">{stat.value}</p>
            </div>
          );
        })}
      </div>

      {/* Gráficos y actividad reciente */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de ingresos */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-gray-900 mb-1">Ingresos Mensuales</h3>
              <p className="text-gray-500">Últimos 6 meses</p>
            </div>
            <button className="text-blue-600 hover:text-blue-700">
              Ver más
            </button>
          </div>

          {/* Simulación de gráfico */}
          <div className="flex items-end justify-between h-48 gap-4">
            {[65, 45, 80, 55, 70, 90].map((height, index) => (
              <div key={index} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full bg-blue-500 rounded-t-lg transition-all hover:bg-blue-600" style={{ height: `${height}%` }}></div>
                <span className="text-xs text-gray-500">{['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'][index]}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Facturas recientes */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-gray-900 mb-1">Facturas Recientes</h3>
              <p className="text-gray-500">Últimas operaciones</p>
            </div>
            <button className="text-blue-600 hover:text-blue-700">
              Ver todas
            </button>
          </div>

          <div className="space-y-4">
            {recentInvoices.map((invoice) => (
              <div key={invoice.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex-1">
                  <p className="text-blue-600">{invoice.id}</p>
                  <p className="text-gray-600 text-sm">{invoice.cliente}</p>
                </div>
                <div className="text-right">
                  <p className="text-gray-900">{formatCurrency(invoice.monto)}</p>
                  <span className={`inline-block text-xs px-2 py-1 rounded-full border mt-1 ${getStatusColor(invoice.estado)}`}>
                    {invoice.estado === 'emitida' ? 'Emitida' : 'Pendiente'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Acciones rápidas */}
      <div className="mt-6 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="mb-2">¿Listo para crear una nueva factura?</h3>
            <p className="text-blue-100">Comienza a facturar en segundos</p>
          </div>
          <button className="bg-white text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition-colors shadow-lg">
            Crear Factura
          </button>
        </div>
      </div>
    </div>
  );
}
