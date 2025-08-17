import {useState} from 'react';

const fastApiURL = process.env.REACT_APP_FAST_API_URL;
console.log("URL: ", fastApiURL)

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
      const response = await fetch(`${fastApiURL}/api/v1/upload${endpoint}`, {
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

  const cardStyle = {
    background: '#ffffff',
    borderRadius: '10px',
    padding: '1.5rem',
    boxShadow: '0px 4px 12px rgba(0,0,0,0.08)',
    marginBottom: '2rem',
  };

  const buttonStyle = {
    background: '#4a90e2',
    color: '#fff',
    padding: '0.6rem 1.2rem',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '1rem',
    transition: 'background 0.3s ease',
  };

  const buttonHoverStyle = { background: '#357ABD' };

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: 'auto', background: '#f7f9fc', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem', color: '#333' }}>PDF Summarizer</h1>

      {/* BART */}
      <div style={cardStyle}>
        <h2 style={{ color: '#4a90e2' }}>BART</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange(setBartFile)} />
        <br /><br />
        <button
          onMouseOver={e => e.currentTarget.style.background = buttonHoverStyle.background}
          onMouseOut={e => e.currentTarget.style.background = buttonStyle.background}
          onClick={() => handleSummarize("bart", bartFile, setBartSummary)}
          disabled={loading.bart}
          style={buttonStyle}
        >
          {loading.bart ? "Summarizing..." : "Summarize with BART"}
        </button>
        <div style={{ marginTop: '1rem', background: '#eef3fa', padding: '1rem', borderRadius: '6px' }}>
          {bartSummary}
        </div>
      </div>

      {/* T5 */}
      <div style={cardStyle}>
        <h2 style={{ color: '#7b68ee' }}>T5</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange(setT5File)} />
        <br /><br />
        <button
          onMouseOver={e => e.currentTarget.style.background = '#5a4fcf'}
          onMouseOut={e => e.currentTarget.style.background = '#7b68ee'}
          onClick={() => handleSummarize("t5", t5File, setT5Summary)}
          disabled={loading.t5}
          style={{ ...buttonStyle, background: '#7b68ee' }}
        >
          {loading.t5 ? "Summarizing..." : "Summarize with T5"}
        </button>
        <div style={{ marginTop: '1rem', background: '#f0ecff', padding: '1rem', borderRadius: '6px' }}>
          {t5Summary}
        </div>
      </div>

      {/* PEGASUS */}
      <div style={cardStyle}>
        <h2 style={{ color: '#e67e22' }}>PEGASUS</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange(setPegasusFile)} />
        <br /><br />
        <button
          onMouseOver={e => e.currentTarget.style.background = '#cf6712'}
          onMouseOut={e => e.currentTarget.style.background = '#e67e22'}
          onClick={() => handleSummarize("pegasus", pegasusFile, setPegasusSummary)}
          disabled={loading.pegasus}
          style={{ ...buttonStyle, background: '#e67e22' }}
        >
          {loading.pegasus ? "Summarizing..." : "Summarize with PEGASUS"}
        </button>
        <div style={{ marginTop: '1rem', background: '#fff3e6', padding: '1rem', borderRadius: '6px' }}>
          {pegasusSummary}
        </div>
      </div>
    </div>
  );
}

export default App;


