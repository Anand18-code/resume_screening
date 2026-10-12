import React, { useRef, useState } from 'react';

export default function ResumeInput({
  inputMode,
  setInputMode,
  selectedFile,
  setSelectedFile,
  pastedText,
  setPastedText,
}) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
        setSelectedFile(file);
      } else {
        alert('Please select a valid PDF file (.pdf).');
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
        setSelectedFile(file);
      } else {
        alert('Please drop a valid PDF file (.pdf).');
      }
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  return (
    <div className="glass-card">
      <div className="card-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg>
        <h3>1. Candidate Resume</h3>
      </div>
      <p className="card-description">Upload a PDF resume or paste raw resume text for automated parsing.</p>

      {/* Mode Switcher */}
      <div className="mode-toggle">
        <button
          type="button"
          className={`mode-btn ${inputMode === 'pdf' ? 'active' : ''}`}
          onClick={() => setInputMode('pdf')}
        >
          📄 Upload PDF
        </button>
        <button
          type="button"
          className={`mode-btn ${inputMode === 'text' ? 'active' : ''}`}
          onClick={() => setInputMode('text')}
        >
          ✏️ Paste Text
        </button>
      </div>

      {inputMode === 'pdf' ? (
        <div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />

          {!selectedFile ? (
            <div
              className={`dropzone ${isDragging ? 'drag-active' : ''}`}
              onClick={() => fileInputRef.current && fileInputRef.current.click()}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <svg className="dropzone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <div className="dropzone-text">Click or drag & drop PDF resume here</div>
              <div className="dropzone-subtext">Supports standard PDF resumes with readable text</div>
            </div>
          ) : (
            <div className="file-preview">
              <div className="file-info">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
                <div>
                  <div className="file-name">{selectedFile.name}</div>
                  <div className="file-size">{formatFileSize(selectedFile.size)}</div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setSelectedFile(null)}
                style={{
                  background: 'rgba(244, 63, 94, 0.2)',
                  border: '1px solid rgba(244, 63, 94, 0.4)',
                  color: '#f43f5e',
                  borderRadius: '6px',
                  padding: '6px 10px',
                  cursor: 'pointer',
                  fontWeight: '600',
                  fontSize: '0.8rem'
                }}
              >
                Change
              </button>
            </div>
          )}
        </div>
      ) : (
        <textarea
          className="custom-textarea"
          placeholder="Paste raw candidate resume text, skills, experience, and educational background..."
          value={pastedText}
          onChange={(e) => setPastedText(e.target.value)}
        />
      )}
    </div>
  );
}
