import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  // Preprocess the input
  const preprocessText = (text) => {
  return text
    .toLowerCase()
    // preserves contractions eg. don't, can't
    .replace(/(?!\b\w*'\w*\b)([^\w\s'])/g, ' $1 ') // space around non-word chars (except apostrophes in contractions)
    .replace(/\s+/g, ' ') // clean up extra spaces
    .trim();
};

  const handleSummarize = async () => {
    setLoading(true);
    try {
      const processedText = preprocessText(inputText); // apply preprocessing

      const response = await fetch("http://localhost:8000/api/v1/summarize/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: processedText }),
      });

      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error("Error:", error);
      setSummary("An error occurred.");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h1>Text Summarizer</h1>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        rows="10"
        cols="60"
        placeholder="Enter your text here..."
        style={{ width: '100%', padding: '1rem' }}
      />
      <br />
      <button onClick={handleSummarize} disabled={loading}>
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

