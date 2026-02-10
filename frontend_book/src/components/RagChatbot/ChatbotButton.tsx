import React from 'react';
import styles from './styles.module.css';

interface ChatbotButtonProps {
  onClick: () => void;
}

const ChatbotButton: React.FC<ChatbotButtonProps> = ({ onClick }) => {
  return (
    <button className={styles.chatbotButton} onClick={onClick} aria-label="Open chatbot">
      <span className={styles.chatIcon}>💬</span>
    </button>
  );
};

export default ChatbotButton;