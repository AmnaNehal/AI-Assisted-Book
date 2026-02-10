import React from 'react';
import ChatUI from './ChatUI';
import styles from './styles.module.css';

interface ChatbotModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatbotModal: React.FC<ChatbotModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h2>Ask the Book</h2>
          <button className={styles.closeButton} onClick={onClose} aria-label="Close chatbot">
            &times;
          </button>
        </div>
        <div className={styles.modalBody}>
          <ChatUI />
        </div>
      </div>
    </div>
  );
};

export default ChatbotModal;