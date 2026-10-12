import React from 'react';

export default function JobDescriptionInput({
  jobDescription,
  setJobDescription,
  presets,
}) {
  const presetKeys = Object.keys(presets || {});

  return (
    <div className="glass-card">
      <div className="card-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
        <h3>2. Target Job Description</h3>
      </div>
      <p className="card-description">Paste required skills, years of experience, and role qualifications.</p>

      {presetKeys.length > 0 && (
        <div className="preset-bar">
          <span className="preset-label">Templates:</span>
          {presetKeys.map((key) => (
            <button
              key={key}
              type="button"
              className="preset-chip"
              onClick={() => setJobDescription(presets[key])}
            >
              {key}
            </button>
          ))}
        </div>
      )}

      <textarea
        className="custom-textarea"
        placeholder="Paste target job requirements, qualifications, and required skills here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />
    </div>
  );
}
