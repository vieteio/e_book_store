import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MonitorProgress({ jobId }) {
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/ingestion-jobs/${jobId}/progress`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming token is stored in localStorage
          }
        });
        setProgress(response.data);
      } catch (error) {
        console.error('Error fetching progress:', error);
      }
    };

    const intervalId = setInterval(fetchProgress, 5000); // Poll every 5 seconds

    return () => clearInterval(intervalId); // Clean up on unmount
  }, [jobId]);

  const getProgressColor = (progress) => {
    if (progress < 30) return 'red';
    if (progress < 70) return 'orange';
    return 'green';
  };

  return (
    <div>
      <h2>Ingestion Progress</h2>
      {progress ? (
        <div>
          <p>Status: {progress.status}</p>
          <div style={{ width: '100%', backgroundColor: '#e0e0e0', borderRadius: '5px' }}>
            <div
              style={{
                width: `${progress.progress}%`,
                backgroundColor: getProgressColor(progress.progress),
                height: '20px',
                borderRadius: '5px',
                transition: 'width 0.5s ease-in-out'
              }}
            />
          </div>
          <p>Progress: {progress.progress}%</p>
          {progress.error && <p style={{ color: 'red' }}>Error: {progress.error}</p>}
          {progress.preview_link && (
            <p>
              Preview Link: <a href={progress.preview_link} target="_blank" rel="noopener noreferrer">View Book</a>
            </p>
          )}
        </div>
      ) : (
        <p>Loading progress...</p>
      )}
    </div>
  );
}

export default MonitorProgress;
