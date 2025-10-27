import React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';
import ChatInterface from '../chat/ChatInterface';
import { ChatProvider } from '../../hooks/useChat';
import { TransactionsProvider } from '../../hooks/useTransactions';

const Layout = ({ children }) => {
  return (
    <ChatProvider>
      <TransactionsProvider>
        <div className="min-h-screen flex flex-col">
          <Header />
          <div className="flex flex-1">
            <Sidebar />
            <main className="flex-1 p-4 lg:p-6">
              {children}
            </main>
          </div>
          <Footer />
          <ChatInterface />
        </div>
      </TransactionsProvider>
    </ChatProvider>
  );
};

export default Layout;
