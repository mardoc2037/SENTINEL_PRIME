import React, { useState } from 'react';
import './App.css';
import logo from './logo.png';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [model, setModel] = useState('adaptive');

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setIsThinking(true);
    setResponse('');

    try {
      const res = await fetch('http://192.168.1.237:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, model })
      });

      if (!res.ok) {
        const errorData = await res.json();
        setResponse(`Error: ${errorData.details || errorData.error || 'Unknown error'}`);
        return;
      }

      const data = await res.json();
      const reply = data.response || 'No response received.';
      setResponse(reply);
      speakText(reply);
    } catch (error) {
      console.error('Error fetching response:', error);
      setResponse('Error fetching response.');
    } finally {
      setIsThinking(false);
    }
  };

  const speakText = async (text) => {
    try {
      const res = await fetch('http://192.168.1.237:5000/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      if (!res.ok) {
        console.error('Audio fetch failed');
        return;
      }

      const audioBlob = await res.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);

      audio.onplay = () => setIsSpeaking(true);
      audio.onended = () => setIsSpeaking(false);

      audio.play();
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img
          src={logo}
          className={`App-logo ${isThinking || isSpeaking ? 'pulse' : ''}`}
          alt="SENTINEL Logo"
        />
        <h1>Welcome to SENTINEL</h1>
        <p>Your AI-powered OSINT assistant is online.</p>

        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSubmit();
            }
          }}
          placeholder="Enter your prompt here"
          style={{ width: '60%', padding: '10px', marginTop: '20px' }}
        />
        <button
          onClick={handleSubmit}
          disabled={isThinking}
          style={{ marginLeft: '10px', padding: '10px' }}
        >
          {isThinking ? 'Thinking...' : 'Submit'}
        </button>

        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          style={{ marginTop: '20px', padding: '10px' }}
        >
          <option value="adaptive">Adaptive (Auto-Select)</option>
          <option value="llama3">LLaMA 3.1</option>
          <option value="phi4">Phi-4 Mini</option>
          <option value="nemotron">NemoTron Mini</option>
          <option value="commandr">Command-R Plus</option>
          <option value="deepseek">DeepSeek V3.1</option>
        </select>

        <div style={{ marginTop: '30px', whiteSpace: 'pre-wrap' }}>
          <strong>Response:</strong>
          <p>{response}</p>
        </div>
      </header>
    </div>
  );
}

export default App;
