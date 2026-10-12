import React from 'react';
import { API_BASE_URL } from '../services/api';

export default function Header({ health }) {
  const isOnline = health && health.status === 'healthy';
  const modelLoaded = health && health.category_model_loaded;

  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
        </div>
        <div>
          <h1 className="brand-title">AI Resume Screening & JD Fit System</h1>
          <p className="brand-subtitle">Automated NLP Parsing, Competency Gap Analysis & Fit Recommendations</p>
        </div>
      </div>

      <div className="backend-status" title={`API URL: ${API_BASE_URL}`}>
        <span className={`status-dot ${isOnline ? 'online' : 'offline'}`}></span>
        <span>
          {isOnline 
            ? (modelLoaded ? 'FastAPI Backend: Online (NLP Ready)' : 'FastAPI Backend: Online (Heuristics)') 
            : 'FastAPI Backend: Connecting...'}
        </span>
      </div>
    </header>
  );
}
