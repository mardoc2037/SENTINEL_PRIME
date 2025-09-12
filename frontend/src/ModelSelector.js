import React, { useEffect, useState } from 'react';

// Optional: static fallback labels for known models
const friendlyLabels = {
  "phi-3-mini-4k-instruct": "Phi-3 Mini",
  "cogito-v1-preview-llama-70B": "Cogito 70B",
  "llama-3-groq-70B-tool-use": "LLaMA 3 Groq",
  "openchat-3.5-1210": "OpenChat 3.5",
  "codellama-7b-instruct": "CodeLLaMA 7B",
  "mistral-7b-instruct-v0.2": "Mistral v0.2",
  "mistral-nemo-prism-12B": "Mistral Nemo Prism",
  "llama-7b": "LLaMA 7B",
  "phi4-mini:3.8b": "Phi-4 Mini (Ollama)",
  "nemotron-mini:4b": "NemoTron Mini (Ollama)",
  "command-r-plus:104b": "Command-R Plus (Ollama)",
  "llama3.1:405b": "LLaMA 3.1 (Ollama)",
  "deepseek-v3.1:671b": "DeepSeek v3.1 (Ollama)",
  "adaptive": "Adaptive (Auto Select)"
};

function ModelSelector({ onModelChange }) {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('adaptive');

  useEffect(() => {
    fetch('http://192.168.1.237:5000/models')
      .then(res => res.json())
      .then(data => {
        if (data.models && data.models.length > 0) {
          const uniqueModels = [...new Set(data.models)];
          const modelOptions = ['adaptive', ...uniqueModels];
          setModels(modelOptions);
          setSelectedModel('adaptive');
          onModelChange('adaptive');
        }
      })
      .catch(err => {
        console.error('Failed to fetch models:', err);
        setModels(['adaptive']); // fallback
        setSelectedModel('adaptive');
        onModelChange('adaptive');
      });
  }, [onModelChange]);

  const handleChange = (e) => {
    const model = e.target.value;
    setSelectedModel(model);
    onModelChange(model);
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <label htmlFor="model" style={{ marginRight: '10px' }}>
        <strong>Choose Model:</strong>
      </label>
      <select
        id="model"
        value={selectedModel}
        onChange={handleChange}
        style={{
          padding: '10px',
          fontSize: '16px',
          backgroundColor: '#111',
          color: '#0f0',
          border: '1px solid #0f0',
          borderRadius: '5px'
        }}
      >
        {models.map((modelName, index) => (
          <option key={`${modelName}-${index}`} value={modelName}>
            {friendlyLabels[modelName] || modelName}
          </option>
        ))}
      </select>
    </div>
  );
}

export default ModelSelector;
