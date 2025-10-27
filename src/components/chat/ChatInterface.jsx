import React, { useMemo, useRef, useState } from 'react';
import { MessageCircle, X } from 'lucide-react';
import { useChatContext } from '../../hooks/useChat';
import MessageBubble from './MessageBubble';
import QuickActions from './QuickActions';

const ChatInterface = () => {
  const { isOpen, toggleOpen, messages, sendMessage, isTyping } = useChatContext();
  const [input, setInput] = useState('');
  const endRef = useRef(null);

  const containerClasses = useMemo(() => (
    `fixed right-4 bottom-4 z-50 ${isOpen ? 'w-96 h-[520px]' : 'w-14 h-14'} transition-all`
  ), [isOpen]);

  const onSend = () => {
    const text = input;
    setInput('');
    sendMessage(text);
  };

  return (
    <div className={containerClasses}>
      {!isOpen && (
        <button onClick={toggleOpen} className="w-14 h-14 rounded-full bg-primary text-white grid place-items-center shadow-lg">
          <MessageCircle className="h-6 w-6" />
        </button>
      )}
      {isOpen && (
        <div className="bg-white rounded-xl shadow-2xl border border-gray-200 flex flex-col h-full">
          <div className="h-12 px-3 flex items-center justify-between border-b">
            <div className="text-sm font-semibold">BiblioAssist</div>
            <button onClick={toggleOpen} className="p-1 hover:bg-gray-100 rounded">
              <X className="h-4 w-4" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-3 space-y-2 bg-gray-50">
            <QuickActions onPick={(q) => sendMessage(q)} />
            {messages.map(m => (
              <MessageBubble key={m.id} role={m.role} text={m.text} />
            ))}
            {isTyping && (
              <MessageBubble role="assistant" text="Escribiendo…" typing />
            )}
            <div ref={endRef} />
          </div>
          <div className="p-2 border-t bg-white">
            <div className="flex items-center gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && onSend()}
                placeholder="Escribe tu pregunta…"
                className="flex-1 px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
              <button onClick={onSend} className="px-3 py-2 bg-primary text-white rounded-md text-sm hover:bg-primary/90">Enviar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
