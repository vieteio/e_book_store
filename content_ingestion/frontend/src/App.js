import React, { useState } from 'react';
import CreateIngestionJob from './components/CreateIngestionJob';
import UploadManuscript from './components/UploadManuscript';
import MonitorProgress from './components/MonitorProgress';

function App() {
  const [jobId, setJobId] = useState(null);

  return (
    <div className="App">
      <h1>Content Ingestion Process</h1>
      {!jobId && <CreateIngestionJob setJobId={setJobId} />}
      {jobId && <UploadManuscript jobId={jobId} />}
      {jobId && <MonitorProgress jobId={jobId} />}
    </div>
  );
}

export default App;
