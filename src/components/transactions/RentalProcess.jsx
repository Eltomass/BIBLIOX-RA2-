import React from 'react';
import PropTypes from 'prop-types';

const RentalProcess = ({ book, onRent }) => {
  if (!book) return null;
  return (
    <div className="p-3 border rounded-md bg-white space-y-2">
      <div className="text-sm">Arriendo estándar: 14 días, renovable si disponible.</div>
      <button onClick={() => onRent(book)} className="px-3 py-2 bg-secondary text-white rounded-md text-sm">Confirmar arriendo</button>
    </div>
  );
};

RentalProcess.propTypes = {
  book: PropTypes.object,
  onRent: PropTypes.func.isRequired,
};

export default RentalProcess;
