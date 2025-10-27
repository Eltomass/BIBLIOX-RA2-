import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { BookOpenText, MessageCircle, ShoppingCart } from 'lucide-react';
import { useChatContext } from '../../hooks/useChat';
import { useTransactions } from '../../hooks/useTransactions';

const Header = () => {
  const { toggleOpen } = useChatContext();
  const { cart } = useTransactions();

  return (
    <header className="bg-primary text-white">
      <div className="mx-auto max-w-7xl px-4 h-14 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2 font-semibold">
          <BookOpenText className="h-6 w-6" />
          <span>LibreriaX</span>
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm">
          <NavLink to="/dashboard" className={({isActive}) => isActive ? 'underline' : 'hover:opacity-90'}>Dashboard</NavLink>
          <NavLink to="/catalog" className={({isActive}) => isActive ? 'underline' : 'hover:opacity-90'}>Catálogo</NavLink>
          <NavLink to="/loans" className={({isActive}) => isActive ? 'underline' : 'hover:opacity-90'}>Mis Préstamos</NavLink>
          <NavLink to="/profile" className={({isActive}) => isActive ? 'underline' : 'hover:opacity-90'}>Perfil</NavLink>
        </nav>
        <div className="flex items-center gap-2">
          <Link to="/cart" className="relative inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 rounded-md px-3 py-1.5 text-sm">
            <ShoppingCart className="h-4 w-4" />
            <span>Carrito</span>
            {cart.length > 0 && (
              <span className="absolute -top-1 -right-1 h-5 min-w-[20px] px-1 rounded-full bg-accent text-white text-xs grid place-items-center">{cart.length}</span>
            )}
          </Link>
          <button onClick={toggleOpen} className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 rounded-md px-3 py-1.5 text-sm">
            <MessageCircle className="h-4 w-4" />
            Chat
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
