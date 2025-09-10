import React, { useState } from 'react';

const ModelSelector = ({ onModelChange }) => {
  const [selectedModel, setSelectedModel] = useState('llama3'); // default fallback

  const models = [
    { label: 'Adaptive (Auto)', value: 'llama3' },
    { label: 'Mistral', value: 'mistral' },
    { label: 'LLaMA 3', value: 'llama3' },
    { label: 'Phi-3', value: 'phi3' },
    { label: 'OpenChat', value: 'openchat' },
    { label: 'Cogito 70B', value: 'cogito:70b' },
    { label: 'Command-R+', value: 'command-r-plus:104b' },
    { label: 'NemoTron Mini', value: 'nemotron-mini:4b' },
    { label: 'LLaMA 3 Groq Tool Use', value: 'llama3-groq-tool-use:70b' },
  ];

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedModel(value);
    onModelChange(value);
  };

  return (
    <div className="model-selector">
      <label htmlFor="model">Model:</label>
      <select id="model" value={selectedModel} onChange={handleChange}>
        {models.map((model) => (
          <option key={model.value} value={model.value}>
            {model.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelector;
