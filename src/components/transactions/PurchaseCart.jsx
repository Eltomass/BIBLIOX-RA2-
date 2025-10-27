import React from 'react';
import PropTypes from 'prop-types';

const currency = (v) => new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(v);

const PurchaseCart = ({ items, onRemove, onCheckout }) => {
  const total = items.reduce((s, i) => s + (i.precio_venta || 0), 0);
  return (
    <div className="space-y-3">
      <ul className="divide-y border rounded-md bg-white">
        {items.length === 0 && <li className="p-3 text-sm text-gray-600">Tu carrito está vacío.</li>}
        {items.map(i => (
          <li key={i.id} className="p-3 flex items-center gap-3">
            <img src={i.portada} alt={i.titulo} className="w-10 h-14 object-cover rounded" />
            <div className="flex-1">
              <div className="text-sm font-medium">{i.titulo}</div>
              <div className="text-xs text-gray-600">{currency(i.precio_venta)}</div>
            </div>
            <button onClick={() => onRemove(i.id)} className="text-xs px-2 py-1 border rounded hover:bg-gray-50">Quitar</button>
          </li>
        ))}
      </ul>
      <div className="flex items-center justify-between">
        <div className="text-sm">Total</div>
        <div className="font-semibold">{currency(total)}</div>
      </div>
      <button disabled={!items.length} onClick={onCheckout} className="w-full px-3 py-2 bg-primary text-white rounded-md disabled:opacity-40">Proceder al pago</button>
    </div>
  );
};

PurchaseCart.propTypes = {
  items: PropTypes.array.isRequired,
  onRemove: PropTypes.func.isRequired,
  onCheckout: PropTypes.func.isRequired,
};

export default PurchaseCart;
