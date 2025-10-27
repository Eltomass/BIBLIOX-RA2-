import React from 'react';
import PropTypes from 'prop-types';

const MessageBubble = ({ role, text, typing }) => {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] rounded-2xl px-3 py-2 text-sm shadow ${isUser ? 'bg-primary text-white rounded-br-sm' : 'bg-white text-gray-800 rounded-bl-sm border'}`}>
        {typing ? (
          <span className="inline-flex gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }} />
            <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '120ms' }} />
            <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '240ms' }} />
          </span>
        ) : text}
      </div>
    </div>
  );
};

MessageBubble.propTypes = {
  role: PropTypes.oneOf(['user', 'assistant']).isRequired,
  text: PropTypes.string,
  typing: PropTypes.bool,
};

export default MessageBubble;
