import React, { useState } from 'react';

function ChatBox() {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');

    const sendPrompt = async () => {
        const res = await fetch('http://192.168.1.237:5000/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await res.json();
        setResponse(data.response);
    };

    return (
        <div>
            <textarea
                rows="4"
                cols="50"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ask SENTINEL something..."
            />
            <br />
            <button onClick={sendPrompt}>Send</button>
            <pre style={{ marginTop: '20px', color: '#00FF00' }}>
                <strong>Response:</strong>
                {response}
            </pre>
        </div>
    );
}

export default ChatBox;
