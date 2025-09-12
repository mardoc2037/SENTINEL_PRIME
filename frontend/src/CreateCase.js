import React, { useState } from 'react';

function CreateCase() {
  const [formData, setFormData] = useState({
    case_id: '',
    name: '',
    age: '',
    location: '',
    details: ''
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const res = await fetch('http://192.168.1.237:5000/create_case', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await res.json();
      if (!res.ok) {
        setMessage(`Error: ${data.error || 'Failed to create case.'}`);
      } else {
        setMessage(data.message);
        setFormData({
          case_id: '',
          name: '',
          age: '',
          location: '',
          details: ''
        });
      }
    } catch (error) {
      console.error('Error submitting case:', error);
      setMessage('Error submitting case.');
    }
  };

  return (
    <div style={{ padding: '40px', color: '#00FF00', backgroundColor: '#000', fontFamily: 'Courier New' }}>
      <h2>Create New Case</h2>
      <form onSubmit={handleSubmit}>
        <input name="case_id" placeholder="Case ID" value={formData.case_id} onChange={handleChange} required /><br /><br />
        <input name="name" placeholder="Name" value={formData.name} onChange={handleChange} /><br /><br />
        <input name="age" type="number" placeholder="Age" value={formData.age} onChange={handleChange} /><br /><br />
        <input name="location" placeholder="Location" value={formData.location} onChange={handleChange} /><br /><br />
        <textarea name="details" placeholder="Details" value={formData.details} onChange={handleChange} rows="4" /><br /><br />
        <button type="submit">Submit Case</button>
      </form>
      {message && <p style={{ marginTop: '20px' }}>{message}</p>}
    </div>
  );
}

export default CreateCase;
