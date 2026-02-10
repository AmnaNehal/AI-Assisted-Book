import React, { useState } from 'react';
import ChatbotButton from './ChatbotButton';
import ChatbotModal from './ChatbotModal';

// Main chatbot component that combines the button and modal
const RagChatbot: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <ChatbotButton onClick={toggleModal} />
      <ChatbotModal isOpen={isModalOpen} onClose={closeModal} />
    </>
  );
};

export default RagChatbot;

/*
 * To use this component globally in Docusaurus:
 * 1. Import this component in your Docusaurus layout (e.g., in src/theme/Layout/index.js)
 * 2. Add <RagChatbot /> to the layout so it appears on all pages
 * 3. Example:
 *    import React from 'react';
 *    import Layout from '@theme/Layout';
 *    import RagChatbot from '@site/src/components/RagChatbot';
 *    
 *    export default function CustomLayout(props) {
 *      return (
 *        <Layout {...props}>
 *          {props.children}
 *          <RagChatbot />
 *        </Layout>
 *      );
 *    }
 */