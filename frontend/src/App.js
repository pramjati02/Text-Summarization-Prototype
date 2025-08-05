import React, { useState } from 'react';

function App() {
  const [bartFile, setBartFile] = useState(null);
  const [t5File, setT5File] = useState(null);
  const [pegasusFile, setPegasusFile] = useState(null);

  const [bartSummary, setBartSummary] = useState('');
  const [t5Summary, setT5Summary] = useState('');
  const [pegasusSummary, setPegasusSummary] = useState('');

  const [loading, setLoading] = useState({ bart: false, t5: false, pegasus: false });

  const handleFileChange = (setter) => (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      setter(file);
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

  const handleSummarize = async (model, file, setSummary) => {
    if (!file) {
      alert("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(prev => ({ ...prev, [model]: true }));

    let endpoint = "/";
    if (model === "t5") endpoint = "/t5/";
    else if (model === "pegasus") endpoint = "/pegasus/";

    try {
      const response = await fetch(`http://localhost:8000/api/v1/upload${endpoint}`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error(error);
      setSummary("An error occurred.");
    } finally {
      setLoading(prev => ({ ...prev, [model]: false }));
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: 'auto' }}>
      <h1>PDF Summarizer</h1>

      {/* BART */}
      <div style={{ marginBottom: '2rem' }}>
        <h2>BART</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange(setBartFile)} />
        <br /><br />
        <button onClick={() => handleSummarize("bart", bartFile, setBartSummary)} disabled={loading.bart}>
          {loading.bart ? "Summarizing..." : "Summarize with BART"}
        </button>
        <div style={{ marginTop: '1rem', background: '#f4f4f4', padding: '1rem' }}>
          {bartSummary}
        </div>
      </div>

      {/* T5 */}
      <div style={{ marginBottom: '2rem' }}>
        <h2>T5</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange(setT5File)} />
        <br /><br />
        <button onClick={() => handleSummarize("t5", t5File, setT5Summary)} disabled={loading.t5}>
          {loading.t5 ? "Summarizing..." : "Summarize with T5"}
        </button>
        <div style={{ marginTop: '1rem', background: '#f4f4f4', padding: '1rem' }}>
          {t5Summary}
        </div>
      </div>

      {/* PEGASUS */}
      <div style={{ marginBottom: '2rem' }}>
        <h2>PEGASUS</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange(setPegasusFile)} />
        <br /><br />
        <button onClick={() => handleSummarize("pegasus", pegasusFile, setPegasusSummary)} disabled={loading.pegasus}>
          {loading.pegasus ? "Summarizing..." : "Summarize with PEGASUS"}
        </button>
        <div style={{ marginTop: '1rem', background: '#f4f4f4', padding: '1rem' }}>
          {pegasusSummary}
        </div>
      </div>
    </div>
  );
}

export default App;

