import React from 'react';

const Footer = () => {
  return (
    <footer className="border-t border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 py-4 text-xs text-gray-600 flex items-center justify-between">
        <p>© {new Date().getFullYear()} LibreriaX. Todos los derechos reservados.</p>
        <p>Diseño académico • Azul primario: #1e40af</p>
      </div>
    </footer>
  );
};

export default Footer;
