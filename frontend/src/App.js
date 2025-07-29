import React, { useState } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
      setSummary('');  // clear previous summary
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

  const handleSummarize = async () => {
    if (!selectedFile) {
      alert("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/v1/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setSummary(data.summary);
    } catch (err) {
      console.error("Error uploading file:", err);
      setSummary("An error occurred while processing the file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h1>PDF Text Summarizer</h1>

      {/* PDF Upload */}
      <input type="file" accept="application/pdf" onChange={handleFileSelect} />
      <br /><br />

      <button onClick={handleSummarize} disabled={!selectedFile || loading}>
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      <h2>Summary:</h2>
      <div style={{ background: '#f4f4f4', padding: '1rem' }}>
        {summary}
      </div>
    </div>
  );
}

export default App;

