import { Outlet, NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, Users, Package, FileText,
  LogOut, PlusCircle, ChevronRight,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'

const NAV_ITEMS = [
  { to: '/dashboard',      label: 'Dashboard',   icon: LayoutDashboard },
  { to: '/facturas',       label: 'Facturas',     icon: FileText },
  { to: '/clientes',       label: 'Clientes',     icon: Users },
  { to: '/productos',      label: 'Productos',    icon: Package },
]

const PAGE_TITLES = {
  '/dashboard':      'Dashboard',
  '/facturas':       'Facturas Electrónicas',
  '/facturas/nueva': 'Nueva Factura',
  '/clientes':       'Gestión de Clientes',
  '/productos':      'Catálogo de Productos',
}

export default function Layout() {
  const { user, logout } = useAuth()
  const { pathname } = useLocation()
  const title = PAGE_TITLES[pathname] || 'FactuPlus'

  return (
    <div className="app-layout">
      {/* ── Sidebar ─────────────────────────────────────────────── */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <h1>Factu<span>Plus</span></h1>
          <p>Facturación Electrónica</p>
        </div>

        <nav className="sidebar-nav">
          <p className="nav-section-title">Menú Principal</p>
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}

          <p className="nav-section-title">Acciones</p>
          <NavLink
            to="/facturas/nueva"
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            <PlusCircle size={16} />
            Nueva Factura
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <button className="nav-link w-full" onClick={logout} style={{ border: 'none', background: 'none', color: 'rgba(255,255,255,.6)' }}>
            <LogOut size={15} />
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* ── Main ────────────────────────────────────────────────── */}
      <div className="main-content">
        <header className="topbar">
          <div className="flex items-center gap-2" style={{ color: 'var(--gray-400)', fontSize: 13 }}>
            <span>FactuPlus</span>
            <ChevronRight size={14} />
            <span style={{ color: 'var(--gray-800)', fontWeight: 600 }}>{title}</span>
          </div>
          <div className="topbar-user">
            <span>{user?.email}</span>
            <div className="avatar">
              {user?.email?.[0]?.toUpperCase() ?? 'U'}
            </div>
          </div>
        </header>

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}