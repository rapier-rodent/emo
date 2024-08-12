import React, { useState } from 'react';
import { GoogleGenerativeAI } from '@google/generative-ai';

const apiKey = process.env.REACT_APP_GEMINI_API_KEY; 
const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({
  model: 'gemini-1.5-pro',
  systemInstruction: `EmoSculpt Chatbot Prompt:\n\nYou are EmoSculpt, a friendly and engaging chatbot designed to help young adults improve their emotional fitness...`, // Add your detailed prompt here
});

const generationConfig = {
  temperature: 0,
  topP: 0.95,
  topK: 64,
  maxOutputTokens: 8192,
  responseMimeType: 'text/plain',
};

function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const chatSession = model.startChat({ generationConfig });

    const result = await chatSession.sendMessage(input);
    setMessages([...messages, { user: input, bot: result.response.text() }]);
    setInput('');
  };

  return (
    <div>
      <h1>EmoSculpt Chat</h1>
      <div>
        {messages.map((msg, index) => (
          <div key={index}>
            <p><strong>You:</strong> {msg.user}</p>
            <p><strong>EmoSculpt:</strong> {msg.bot}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chat;
