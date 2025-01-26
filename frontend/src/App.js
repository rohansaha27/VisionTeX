import React, { useState } from 'react';
import './App.css';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [pdfData, setPdfData] = useState(null); // PDF data from backend
  const [latexCode, setLatexCode] = useState(''); // LaTeX code from backend
  const [darkMode, setDarkMode] = useState(false);
  const [showOutputPage, setShowOutputPage] = useState(false);
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setUploadedFile(file);
    setFileName(file ? file.name : '');
  };

  const handleSubmit = async () => {
    if (!uploadedFile) {
      alert('Please upload a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);

    setIsLoading(true); // Show loading screen

    try {
      const response = await fetch('http://localhost:5000/process-image', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setPdfData(data.pdfBase64); // Base64 encoded PDF data from backend
        setLatexCode(data.latexCode); // LaTeX code from backend
        setShowOutputPage(true);
      } else {
        alert('Error processing the file. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while connecting to the server.');
    } finally {
      setIsLoading(false); // Hide loading screen
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleBack = () => {
    setShowOutputPage(false);
    setUploadedFile(null);
    setFileName('');
    setPdfData(null);
    setLatexCode('');
  };

  const handleCopyLatex = () => {
    navigator.clipboard.writeText(latexCode).then(() => {
      alert('LaTeX code copied to clipboard!');
    });
  };

  return (
    <div className={`visiontex-container ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <header className="header">
        <button onClick={toggleDarkMode} className="toggle-mode-button">
          {darkMode ? '🌙 Dark Mode' : '☀️ Light Mode'}
        </button>
        <h1>VisionTeX</h1>
      </header>

      {isLoading ? (
        <div className="loading-screen">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      ) : showOutputPage ? (
        <main className="output-page">
          <div className="pdf-viewer">
            <h2>PDF Contents</h2>
            {pdfData ? (
              <>
                <iframe
                  src={`data:application/pdf;base64,${pdfData}`}
                  title="PDF Viewer"
                  style={{ width: '100%', height: '100%' }}
                ></iframe>
                <button
                  onClick={() => {
                    const link = document.createElement('a');
                    link.href = `data:application/pdf;base64,${pdfData}`;
                    link.download = 'output.pdf';
                    link.click();
                  }}
                  className="download-button"
                >
                  Download PDF
                </button>
              </>
            ) : (
              <p>No PDF data available.</p>
            )}
          </div>
          <div className="latex-viewer">
            <h2>LaTeX Output</h2>
            <pre>{latexCode || 'No LaTeX code available.'}</pre>
            {latexCode && (
              <button onClick={handleCopyLatex} className="copy-button">
                Copy LaTeX Code
              </button>
            )}
          </div>
          <button onClick={handleBack} className="back-button">
            Back
          </button>
        </main>
      ) : (
        <main className="main-content">
          <label htmlFor="fileInput" className="upload-box">
            <div className="upload-box-placeholder">
              {fileName || 'Click to upload an image'}
            </div>
            <input
              id="fileInput"
              type="file"
              accept=".jpg, .jpeg, .png"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </label>
          <div className="button-container">
            <button onClick={handleBack} className="back-button">
              Back
            </button>
            <button onClick={handleSubmit} className="submit-button">
              Submit
            </button>
          </div>
        </main>
      )}
    </div>
  );
}

export default App;