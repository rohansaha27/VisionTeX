import React, { useState } from 'react';
import { Worker, Viewer } from '@react-pdf-viewer/core'; // Import PDF Viewer
import '@react-pdf-viewer/core/lib/styles/index.css'; // Viewer styles
import './App.css';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [output, setOutput] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [showOutputPage, setShowOutputPage] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setUploadedFile(file);
    setFileName(file ? file.name : '');
  };

  const handleSubmit = () => {
    if (!uploadedFile) {
      alert('Please upload a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);

    // Simulating asynchronous behavior using promises
    new Promise((resolve) => {
      setTimeout(() => {
        // Mocked backend response
        const mockResponse = {
          latexCode: 'Mock LaTeX Code: \\int_{0}^{\\infty} e^{-x^2} dx',
        };
        resolve(mockResponse);
      }, 1000);
    })
      .then((response) => {
        setOutput(response.latexCode);
        setShowOutputPage(true);
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while connecting to the server.');
      });
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleBack = () => {
    setShowOutputPage(false);
    setUploadedFile(null);
    setFileName('');
    setOutput('');
  };

  return (
    <div className={`visiontex-container ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <header className="header">
        <button onClick={toggleDarkMode} className="toggle-mode-button">
          {darkMode ? '🌙 Dark Mode' : '☀️ Light Mode'}
        </button>
        <h1>VisionTeX</h1>
      </header>

      {showOutputPage ? (
        <main className="output-page">
          <div className="pdf-viewer">
            <h2>PDF Contents</h2>
            {uploadedFile ? (
              <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js">
              <Viewer fileUrl={URL.createObjectURL(uploadedFile)} />
            </Worker>
            ) : (
              <p>No PDF uploaded</p>
            )}
          </div>
          <div className="latex-viewer">
            <h2>LaTeX Output</h2>
            <pre>{output}</pre>
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
              accept=".pdf"
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