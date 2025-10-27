import React from 'react';
import PropTypes from 'prop-types';
import { BookOpen, Heart, MessageCircle, ShoppingCart } from 'lucide-react';
import { useParallax } from '../../hooks/useParallax';

const currency = (v) => new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(v);

const BookCard = ({ book, onRent, onPurchase, onAskAI, onDetails, onFavorite }) => {
  const parallaxOffset = useParallax(0.2, true);

  return (
    <div className="bg-white rounded-xl shadow hover:shadow-lg transition-shadow overflow-hidden border">
      <div className="relative h-48 bg-gray-100 overflow-hidden">
        <img
          src={book.portada}
          alt={book.titulo}
          className="absolute inset-0 w-full h-full object-cover will-change-transform"
          style={{ transform: `translateY(${parallaxOffset}px)` }}
          loading="lazy"
        />
      </div>
      <div className="p-4 space-y-2">
        <h3 className="text-base font-semibold line-clamp-1">{book.titulo}</h3>
        <p className="text-sm text-gray-600">Por: {book.autor}</p>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <span>⭐ {book.rating.toFixed(1)}</span>
          <span>({book.reseñas} reseñas)</span>
        </div>
        <div className="flex items-center justify-between text-sm">
          <span className={`${book.estado === 'disponible' ? 'text-green-600' : book.estado === 'prestado' ? 'text-red-600' : 'text-amber-600'}`}>● {book.estado}</span>
          <span className="text-gray-600">{book.copias?.disponibles}/{book.copias?.total} copias</span>
        </div>
        <div className="flex items-center justify-between text-sm">
          <span>Arriendo: <strong>{currency(book.precio_arriendo)}</strong></span>
          <span>Compra: <strong>{currency(book.precio_venta)}</strong></span>
        </div>
        <div className="pt-2 grid grid-cols-2 gap-2">
          <button onClick={() => onRent?.(book)} className="px-3 py-2 text-sm rounded-md bg-secondary text-white hover:bg-emerald-600">Arrendar</button>
          <button onClick={() => onPurchase?.(book)} className="px-3 py-2 text-sm rounded-md bg-primary text-white hover:bg-primary/90 flex items-center justify-center gap-1">
            <ShoppingCart className="h-4 w-4" /> Comprar
          </button>
          <button onClick={() => onAskAI?.(book)} className="col-span-2 px-3 py-2 text-sm rounded-md bg-white border hover:bg-gray-50 flex items-center justify-center gap-1">
            <MessageCircle className="h-4 w-4" /> Preguntar sobre libro
          </button>
          <div className="col-span-2 flex items-center justify-between text-xs text-gray-600">
            <button onClick={() => onDetails?.(book)} className="hover:text-primary inline-flex items-center gap-1"><BookOpen className="h-3 w-3" /> Ver detalles</button>
            <button onClick={() => onFavorite?.(book)} className="hover:text-rose-600 inline-flex items-center gap-1"><Heart className="h-3 w-3" /> Favorito</button>
          </div>
        </div>
      </div>
    </div>
  );
};

BookCard.propTypes = {
  book: PropTypes.object.isRequired,
  onRent: PropTypes.func,
  onPurchase: PropTypes.func,
  onAskAI: PropTypes.func,
  onDetails: PropTypes.func,
  onFavorite: PropTypes.func,
};

export default BookCard;
