import React from 'react';
import PropTypes from 'prop-types';

const FilterPanel = ({ filters, onChange }) => {
  const set = (key, value) => onChange({ ...filters, [key]: value });

  return (
    <div className="flex flex-wrap items-center gap-3 text-sm">
      <div className="flex items-center gap-2">
        <label className="text-gray-600">Estado</label>
        <select value={filters.estado} onChange={(e) => set('estado', e.target.value)} className="border rounded-md px-2 py-1">
          <option>Todos</option>
          <option>disponible</option>
          <option>prestado</option>
          <option>reservado</option>
        </select>
      </div>
      <div className="flex items-center gap-2">
        <label className="text-gray-600">Género</label>
        <select value={filters.genero} onChange={(e) => set('genero', e.target.value)} className="border rounded-md px-2 py-1">
          <option>Todos</option>
          <option>Ficción</option>
          <option>No ficción</option>
          <option>Técnico</option>
        </select>
      </div>
    </div>
  );
};

FilterPanel.propTypes = {
  filters: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default FilterPanel;
