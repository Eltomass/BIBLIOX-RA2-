import React from 'react';
import PropTypes from 'prop-types';

const DEFAULTS = [
  '¿Cuál es el período de préstamo?',
  '¿Cómo renovar un libro?',
  '¿Cuánto cuesta la multa por día?',
  '¿Cómo buscar un libro específico?'
];

const QuickActions = ({ onPick }) => {
  return (
    <div className="flex flex-wrap gap-2 mb-2">
      {DEFAULTS.map((q) => (
        <button key={q} onClick={() => onPick(q)} className="text-xs px-2 py-1 rounded-full bg-white border hover:bg-gray-50">
          {q}
        </button>
      ))}
    </div>
  );
};

QuickActions.propTypes = {
  onPick: PropTypes.func.isRequired,
};

export default QuickActions;
