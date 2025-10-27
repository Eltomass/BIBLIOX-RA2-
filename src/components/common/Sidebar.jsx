import React from 'react';
import { Link } from 'react-router-dom';
import FinesWidget from '../user/FinesWidget';

const Sidebar = () => {
  return (
    <aside className="hidden lg:block w-72 shrink-0 border-r border-gray-200 bg-white">
      <div className="p-4 space-y-6">
        <div>
          <h3 className="text-sm font-semibold text-gray-600">Accesos rápidos</h3>
          <div className="mt-2 space-y-1 text-sm">
            <Link to="/catalog" className="block hover:text-primary">Buscar libros</Link>
            <Link to="/loans" className="block hover:text-primary">Mis préstamos</Link>
            <Link to="/profile" className="block hover:text-primary">Perfil</Link>
          </div>
        </div>
        <FinesWidget />
      </div>
    </aside>
  );
};

export default Sidebar;
