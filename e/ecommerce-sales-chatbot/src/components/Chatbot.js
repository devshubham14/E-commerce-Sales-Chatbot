import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const ChatContainer = styled.div`
  max-width: 600px;
  margin: 40px auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.15);
  display: flex;
  flex-direction: column;
  height: 70vh;
`;

const ChatHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem 0.5rem 1.5rem;
  border-bottom: 1px solid #eee;
  background: white;
`;

const Title = styled.h3`
  margin: 0;
  color: #667eea;
  font-weight: bold;
`;

const ResetButton = styled.button`
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #c0392b;
  }
`;

const ChatHistory = styled.div`
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background: #f8f9fa;
`;

const MessageRow = styled.div`
  display: flex;
  flex-direction: column;
  align-items: ${props => (props.sender === 'user' ? 'flex-end' : 'flex-start')};
  margin-bottom: 1.2rem;
`;

const MessageBubble = styled.div`
  background: ${props => (props.sender === 'user' ? '#667eea' : '#e2e8f0')};
  color: ${props => (props.sender === 'user' ? 'white' : '#333')};
  padding: 0.8rem 1.2rem;
  border-radius: 18px;
  max-width: 70%;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.07);
`;

const Timestamp = styled.span`
  font-size: 0.75rem;
  color: #888;
  margin-top: 0.2rem;
`;

const ChatForm = styled.form`
  display: flex;
  padding: 1rem;
  border-top: 1px solid #eee;
  background: #f8f9fa;
`;

const ChatInput = styled.input`
  flex: 1;
  padding: 0.8rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
`;

const SendButton = styled.button`
  margin-left: 1rem;
  padding: 0.8rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #764ba2;
  }
`;

const Chatbot = () => {
  const { token } = useAuth();
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [resetting, setResetting] = useState(false);
  const chatEndRef = useRef(null);

  // Fetch chat history on mount
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get('/api/chat/history');
        setMessages(res.data);
      } catch (err) {
        setMessages([]);
      }
    };
    fetchHistory();
  }, []);

  // Scroll to bottom on new message
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleInputChange = (e) => setInput(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/chat', { message: input });
      // Refetch history to get both user and bot messages (with timestamps)
      const history = await axios.get('/api/chat/history');
      setMessages(history.data);
      setInput('');
    } catch (err) {
      // Optionally show error
    }
    setLoading(false);
  };

  const handleReset = async () => {
    setResetting(true);
    try {
      await axios.post('/api/chat/reset');
      setMessages([]);
    } catch (err) {
      // Optionally show error
    }
    setResetting(false);
  };

  return (
    <ChatContainer>
      <ChatHeader>
        <Title>Chatbot Assistant</Title>
        <ResetButton onClick={handleReset} disabled={resetting}>
          {resetting ? 'Resetting...' : 'Reset Conversation'}
        </ResetButton>
      </ChatHeader>
      <ChatHistory>
        {messages.map((msg, idx) => (
          <MessageRow key={msg.id || idx} sender={msg.sender}>
            <MessageBubble sender={msg.sender}>{msg.message}</MessageBubble>
            <Timestamp>{new Date(msg.timestamp).toLocaleString()}</Timestamp>
          </MessageRow>
        ))}
        <div ref={chatEndRef} />
      </ChatHistory>
      <ChatForm onSubmit={handleSubmit}>
        <ChatInput
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
          disabled={loading}
        />
        <SendButton type="submit" disabled={loading || !input.trim()}>
          {loading ? 'Sending...' : 'Send'}
        </SendButton>
      </ChatForm>
    </ChatContainer>
  );
};

export default Chatbot;