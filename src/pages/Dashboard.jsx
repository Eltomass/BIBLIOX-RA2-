import React from 'react';
import { Link } from 'react-router-dom';

const Stat = ({ label, value }) => (
  <div className="p-4 bg-white rounded-lg border">
    <div className="text-xs text-gray-600">{label}</div>
    <div className="text-2xl font-semibold">{value}</div>
  </div>
);

const Dashboard = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">Resumen</h1>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="Libros prestados" value={2} />
        <Stat label="Próximos vencimientos" value={1} />
        <Stat label="Multas pendientes" value={'$1.500'} />
        <Stat label="Reservas activas" value={1} />
      </div>
      <div className="p-4 bg-white rounded-lg border">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-semibold">Explora el catálogo</h2>
            <p className="text-sm text-gray-600">Busca por género, autor o disponibilidad.</p>
          </div>
          <div className="flex gap-2">
            <Link to="/catalog" className="px-3 py-2 bg-primary text-white rounded-md text-sm">Ir al catálogo</Link>
            <Link to="/cart" className="px-3 py-2 bg-secondary text-white rounded-md text-sm">Ver carrito</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
