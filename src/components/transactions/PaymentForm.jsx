import React, { useState } from 'react';
import PropTypes from 'prop-types';

const PaymentForm = ({ onPay }) => {
  const [method, setMethod] = useState('tarjeta');
  const [processing, setProcessing] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setProcessing(true);
    try {
      const res = await onPay(method);
      alert(`Pago ${res.ok ? 'exitoso' : 'fallido'} por ${new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(res.total)} via ${method}.`);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-3">
      <div className="text-sm font-semibold">Método de pago</div>
      <div className="flex gap-3 text-sm">
        <label className="flex items-center gap-2">
          <input type="radio" name="method" value="tarjeta" checked={method==='tarjeta'} onChange={(e)=>setMethod(e.target.value)} /> Tarjeta
        </label>
        <label className="flex items-center gap-2">
          <input type="radio" name="method" value="transferencia" checked={method==='transferencia'} onChange={(e)=>setMethod(e.target.value)} /> Transferencia
        </label>
        <label className="flex items-center gap-2">
          <input type="radio" name="method" value="efectivo" checked={method==='efectivo'} onChange={(e)=>setMethod(e.target.value)} /> Efectivo
        </label>
      </div>
      <button type="submit" disabled={processing} className="px-3 py-2 bg-secondary text-white rounded-md disabled:opacity-50">{processing ? 'Procesando…' : 'Pagar'}</button>
    </form>
  );
};

PaymentForm.propTypes = {
  onPay: PropTypes.func.isRequired,
};

export default PaymentForm;
