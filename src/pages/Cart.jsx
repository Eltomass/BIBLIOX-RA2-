import React from 'react';
import PurchaseCart from '../components/transactions/PurchaseCart';
import PaymentForm from '../components/transactions/PaymentForm';
import { useTransactions } from '../hooks/useTransactions';

const Cart = () => {
  const { cart, removeFromCart, payCart } = useTransactions();

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Carrito</h1>
      <PurchaseCart items={cart} onRemove={removeFromCart} onCheckout={() => {}} />
      <PaymentForm onPay={payCart} />
    </div>
  );
};

export default Cart;
