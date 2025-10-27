import React, { createContext, useContext, useEffect, useMemo, useState, useCallback } from 'react';

const STORAGE_CART = 'lx_cart_items';
const STORAGE_LOANS = 'lx_loans';
const TransactionsContext = createContext(null);

export const TransactionsProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    const saved = localStorage.getItem(STORAGE_CART);
    return saved ? JSON.parse(saved) : [];
  });
  const [loans, setLoans] = useState(() => {
    const saved = localStorage.getItem(STORAGE_LOANS);
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_CART, JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    localStorage.setItem(STORAGE_LOANS, JSON.stringify(loans));
  }, [loans]);

  const addToCart = useCallback((book) => {
    setCart(prev => {
      if (prev.find(i => i.id === book.id)) return prev;
      return [...prev, { id: book.id, titulo: book.titulo, precio_venta: book.precio_venta, portada: book.portada }];
    });
  }, []);

  const removeFromCart = useCallback((id) => setCart(prev => prev.filter(i => i.id !== id)), []);
  const clearCart = useCallback(() => setCart([]), []);

  const rentBook = useCallback((book) => {
    const due = new Date();
    due.setDate(due.getDate() + 14);
    setLoans(prev => [...prev, { id: book.id, titulo: book.titulo, dueAt: due.toISOString() }]);
    alert(`Arriendo iniciado: "${book.titulo}" hasta ${due.toLocaleDateString('es-CL')}`);
  }, []);

  const payCart = useCallback(async (method = 'tarjeta') => {
    await new Promise(r => setTimeout(r, 800));
    const total = cart.reduce((s, i) => s + (i.precio_venta || 0), 0);
    clearCart();
    return { ok: true, method, total };
  }, [cart, clearCart]);

  const value = useMemo(() => ({ cart, addToCart, removeFromCart, clearCart, payCart, loans, rentBook }), [cart, addToCart, removeFromCart, clearCart, payCart, loans, rentBook]);

  return <TransactionsContext.Provider value={value}>{children}</TransactionsContext.Provider>;
};

export const useTransactions = () => {
  const ctx = useContext(TransactionsContext);
  if (!ctx) throw new Error('useTransactions debe usarse dentro de TransactionsProvider');
  return ctx;
};
