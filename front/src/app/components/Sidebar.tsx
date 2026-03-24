import { LayoutDashboard, FileText, Users, BarChart3, Settings, LogOut } from 'lucide-react';
import { Link, useLocation } from 'react-router';
import { useAuth } from '../contexts/AuthContext';

interface SidebarProps {
  activeItem?: string;
  onItemClick?: (item: string) => void;
}

export function Sidebar({ activeItem, onItemClick }: SidebarProps) {
  const location = useLocation();
  const { logout } = useAuth();

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, path: '/' },
    { id: 'facturas', label: 'Facturas', icon: FileText, path: '/facturas' },
    { id: 'clientes', label: 'Clientes', icon: Users, path: '/clientes' },
    { id: 'reportes', label: 'Reportes', icon: BarChart3, path: '/reportes' },
  ];

  const isActive = (path: string) => {
    if (activeItem) {
      return menuItems.find(item => item.id === activeItem)?.path === path;
    }
    return location.pathname === path;
  };

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
            <FileText className="w-6 h-6 text-white" strokeWidth={2.5} />
          </div>
          <div>
            <h2 className="text-gray-900">FacturaExpress</h2>
            <p className="text-gray-500 text-xs">Sistema de facturación</p>
          </div>
        </div>
      </div>

      {/* Menú de navegación */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);

            return (
              <li key={item.id}>
                <Link
                  to={item.path}
                  onClick={() => onItemClick?.(item.id)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    active
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Configuración y Cerrar sesión */}
      <div className="p-4 border-t border-gray-200 space-y-2">
        <button
          className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors w-full"
        >
          <Settings className="w-5 h-5" />
          <span>Configuración</span>
        </button>
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-colors w-full"
        >
          <LogOut className="w-5 h-5" />
          <span>Cerrar sesión</span>
        </button>
      </div>
    </div>
  );
}
