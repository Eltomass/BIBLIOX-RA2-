import { useMemo, useState } from 'react';

export const useBooks = (books) => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({ genero: 'Todos', estado: 'Todos' });

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return books.filter(b => {
      const matchesQuery = !q || b.titulo.toLowerCase().includes(q) || b.autor.toLowerCase().includes(q);
      const matchesGenero = filters.genero === 'Todos' || (b.genero?.includes?.(filters.genero));
      const matchesEstado = filters.estado === 'Todos' || b.estado === filters.estado;
      return matchesQuery && matchesGenero && matchesEstado;
    });
  }, [books, query, filters]);

  return {
    query,
    setQuery,
    filters,
    setFilters,
    books: filtered,
  };
};
