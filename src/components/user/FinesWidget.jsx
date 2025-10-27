import React from 'react';
import { AlertCircle, Info, MessageCircle } from 'lucide-react';
import { useChatContext } from '../../hooks/useChat';

const FinesWidget = () => {
  const { toggleOpen, sendMessage } = useChatContext();
  const total = 1500;
  const dias = 3;

  const askAboutFines = () => {
    toggleOpen();
    sendMessage('¿Cómo se calculan mis multas y cómo puedo pagarlas?');
  };

  return (
    <div className="p-3 rounded-lg border bg-amber-50 border-amber-200">
      <div className="flex items-start gap-2">
        <AlertCircle className="h-5 w-5 text-amber-600" />
        <div className="flex-1">
          <div className="text-sm font-semibold text-amber-800">Multas pendientes</div>
          <div className="text-sm text-amber-800/90">Monto: ${total.toLocaleString('es-CL')}</div>
          <div className="text-xs text-amber-700">{dias} días en atraso</div>
          <div className="mt-2 flex items-center gap-2">
            <button onClick={askAboutFines} className="px-2 py-1 text-xs rounded-md bg-amber-600 text-white hover:bg-amber-700 inline-flex items-center gap-1">
              <MessageCircle className="h-3 w-3" /> Consultar a IA
            </button>
            <button className="px-2 py-1 text-xs rounded-md bg-white border hover:bg-gray-50 inline-flex items-center gap-1">
              <Info className="h-3 w-3" /> Ver detalles
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinesWidget;
