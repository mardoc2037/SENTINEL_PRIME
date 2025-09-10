import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CreateCase = () => {
  const [formData, setFormData] = useState({
    name: '',
    county: '',
    dob: '',
    age: '',
    lastSeenLocation: '',
    description: '',
    status: 'active',
    alerts: '',
    alertContext: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    let updatedForm = { ...formData, [name]: value };

    if (name === 'dob') {
      const birthDate = new Date(value);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const m = today.getMonth() - birthDate.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      updatedForm.age = age;
    }

    setFormData(updatedForm);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://192.168.1.237:5000/api/case', formData);
      const caseId = res.data.case_id || res.data.id;
      alert('✅ Case file created successfully.');
      navigate(`/case/${caseId}`);
    } catch (error) {
      console.error('Error creating case:', error);
      alert('❌ Error creating case: ' + error.message);
    }
  };

  return (
    <div style={{ padding: '40px', color: '#00ff00', backgroundColor: '#000', fontFamily: 'Courier New' }}>
      <h2>Create Case File</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label><br />
          <input name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div>
          <label>County:</label><br />
          <input name="county" value={formData.county} onChange={handleChange} required />
        </div>
        <div>
          <label>Date of Birth:</label><br />
          <input name="dob" type="date" value={formData.dob} onChange={handleChange} required />
        </div>
        <div>
          <label>Age:</label><br />
          <input name="age" type="number" value={formData.age} readOnly />
        </div>
        <div>
          <label>Last Seen Location:</label><br />
          <input name="lastSeenLocation" value={formData.lastSeenLocation} onChange={handleChange} required />
        </div>
        <div>
          <label>Description:</label><br />
          <textarea name="description" value={formData.description} onChange={handleChange} required />
        </div>
        <div>
          <label>Status:</label><br />
          <select name="status" value={formData.status} onChange={handleChange}>
            <option value="active">Active</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>
        <div>
          <label>Special Alerts:</label><br />
          <input name="alerts" value={formData.alerts} onChange={handleChange} placeholder="e.g. Medical Alert, Mental Health Alert" />
        </div>
        <div>
          <label>Alert Context:</label><br />
          <textarea name="alertContext" value={formData.alertContext} onChange={handleChange} placeholder="Details about the alert" />
        </div>
        <button type="submit" style={{ marginTop: '20px', padding: '10px 20px', backgroundColor: '#00ff00', color: '#000', fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>
          Submit Case
        </button>
      </form>
    </div>
  );
};

export default CreateCase;
