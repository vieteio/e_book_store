import React, { useState } from 'react';
import axios from 'axios';

function CreateIngestionJob({ setJobId }) {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [genre, setGenre] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/ingestion-jobs/`, {
        title,
        author,
        genre,
        description
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming token is stored in localStorage
        }
      });
      setJobId(response.data);
    } catch (error) {
      console.error('Error creating ingestion job:', error);
    }
  };

  return (
    <div>
      <h2>Create Ingestion Job</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <input type="text" placeholder="Author" value={author} onChange={(e) => setAuthor(e.target.value)} required />
        <input type="text" placeholder="Genre" value={genre} onChange={(e) => setGenre(e.target.value)} required />
        <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} required />
        <button type="submit">Create Job</button>
      </form>
    </div>
  );
}

export default CreateIngestionJob;
