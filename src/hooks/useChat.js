'use client';
import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { askAssistant } from '../services/chatAPI';

/**
 * Contexto de chat para compartir estado entre componentes (chat persistente).
 */
const ChatContext = createContext(null);

/**
 * Proveedor del contexto de chat.
 * - Persiste historial en sessionStorage.
 * - Gestión de estados: abierto/cerrado, escribiendo, mensajes.
 * - Envío de mensajes al backend con fallback informativo.
 */
export const ChatProvider = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(() => {
    const saved = sessionStorage.getItem('chat_messages');
    return saved ? JSON.parse(saved) : [];
  });
  const [isTyping, setIsTyping] = useState(false);

  // Persistencia del historial de conversación por sesión
  useEffect(() => {
    sessionStorage.setItem('chat_messages', JSON.stringify(messages));
  }, [messages]);

  const toggleOpen = () => setIsOpen(v => !v);

  /**
   * Enviar mensaje al backend y manejar respuesta/errores.
   */
  const sendMessage = async (text) => {
    if (!text?.trim()) return;
    const userMsg = { id: crypto.randomUUID(), role: 'user', text, ts: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);
    try {
      const answer = await askAssistant(text);
      const botMsg = { id: crypto.randomUUID(), role: 'assistant', text: answer || 'Sin respuesta', ts: Date.now() };
      setMessages(prev => [...prev, botMsg]);
    } catch (e) {
      // Fallback: avisar claramente al usuario que el backend no está disponible
      const botMsg = { id: crypto.randomUUID(), role: 'assistant', text: 'No pude contactar al backend en http://localhost:8000. Verifica que esté corriendo.', ts: Date.now() };
      setMessages(prev => [...prev, botMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const value = useMemo(() => ({ isOpen, toggleOpen, messages, sendMessage, isTyping }), [isOpen, messages, isTyping]);

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

/**
 * Hook para acceder al contexto del chat.
 */
export const useChatContext = () => {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error('useChatContext debe usarse dentro de ChatProvider');
  return ctx;
};
