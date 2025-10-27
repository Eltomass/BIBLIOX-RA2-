import React from 'react';
import BookCard from '../components/books/BookCard';
import { mockBooks } from '../data/mockBooks';
import SearchBar from '../components/search/SearchBar';
import FilterPanel from '../components/search/FilterPanel';
import { useBooks } from '../hooks/useBooks';
import { useTransactions } from '../hooks/useTransactions';
import RentalProcess from '../components/transactions/RentalProcess';

const Catalog = () => {
  const { query, setQuery, filters, setFilters, books } = useBooks(mockBooks);
  const { addToCart, rentBook } = useTransactions();

  const handleAskAI = (book) => {
    console.log('Ask AI about', book.titulo);
  };

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Catálogo</h1>
      <div className="grid gap-3 md:grid-cols-3">
        <SearchBar value={query} onChange={setQuery} />
        <div className="md:col-span-2"><FilterPanel filters={filters} onChange={setFilters} /></div>
      </div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {books.map((b) => (
          <div key={b.id} className="space-y-2">
            <BookCard
              book={b}
              onPurchase={() => addToCart(b)}
              onRent={() => rentBook(b)}
              onAskAI={handleAskAI}
            />
            <RentalProcess book={b} onRent={rentBook} />
          </div>
        ))}
        {books.length === 0 && (
          <div className="text-sm text-gray-600">No se encontraron libros.</div>
        )}
      </div>
    </div>
  );
};

export default Catalog;
