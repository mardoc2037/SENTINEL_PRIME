import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setIsThinking(true); // switch button to "Thinking..."

    try {
      const res = await fetch('http://192.168.1.237:5000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
      });

      if (!res.ok) {
        throw new Error(`Server responded with status ${res.status}`);
      }

      const data = await res.json();
      setResponse(data.response || data.error || 'No response received.');
    } catch (err) {
      setResponse('Error: ' + err.message);
    } finally {
      setIsThinking(false); // switch button back to "Submit"
    }
  };

  return (
    <div className="App">
      <header className="App-header">
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

        <div style={{ marginTop: '30px', whiteSpace: 'pre-wrap' }}>
          <strong>Response:</strong>
          <p>{response}</p>
        </div>
      </header>
    </div>
  );
}

export default App;
