// SqlForm.js

import React, { useState } from 'react';

const SqlForm = () => {
  const [sqlQuery, setSqlQuery] = useState('');
  const [response, setResponse] = useState(null);

  const handleRunQuery = async () => {
    try {
      const response = await fetch('http://34.229.187.228:8000/api/create_excel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sql_query: sqlQuery }),
      });

      const data = await response.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDownloadExcel = () => {
    if (response && response.file_name) {
      const downloadLink = document.createElement('a');
      downloadLink.href = `http://34.229.187.228/static/${response.file_name}`;
      downloadLink.download = response.file_name;
      downloadLink.click();
    }
  };

  return (
    <div>
      <h2>SQL Query Form</h2>
      <textarea
        value={sqlQuery}
        onChange={(e) => setSqlQuery(e.target.value)}
        placeholder="Enter your SQL query"
        rows={4}
        cols={50}
      />
      <br />
      <button onClick={handleRunQuery}>Run Query</button>

      {response && (
        <div>
          <h3>Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
          <button onClick={handleDownloadExcel}>Download Excel</button>
        </div>
      )}
    </div>
  );
};

export default SqlForm;
