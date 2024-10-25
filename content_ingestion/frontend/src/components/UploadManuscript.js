import React, { useState } from 'react';
import axios from 'axios';

function UploadManuscript({ jobId }) {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setUploadStatus('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/ingestion-jobs/${jobId}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming token is stored in localStorage
        }
      });
      setUploadStatus('Upload successful');
      console.log(response.data);
    } catch (error) {
      setUploadStatus('Upload failed');
      console.error('Error uploading manuscript:', error);
    }
  };

  return (
    <div>
      <h2>Upload Manuscript</h2>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} accept=".epub,.pdf,.mobi" />
        <button type="submit">Upload</button>
      </form>
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
}

export default UploadManuscript;
