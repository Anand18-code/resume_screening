import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import ResumeInput from '../components/ResumeInput';
import JobDescriptionInput from '../components/JobDescriptionInput';
import MetricCards from '../components/MetricCards';
import OverviewTab from '../components/OverviewTab';
import SkillAnalysis from '../components/SkillAnalysis';
import InsightsTab from '../components/InsightsTab';
import CandidateProfileTab from '../components/CandidateProfileTab';
import { checkHealth, fetchSampleJDs, screenResumeText, uploadResumeFile } from '../services/api';

export default function Dashboard() {
  const [health, setHealth] = useState(null);
  const [presets, setPresets] = useState({});

  const [inputMode, setInputMode] = useState('pdf'); // 'pdf' or 'text'
  const [selectedFile, setSelectedFile] = useState(null);
  const [pastedText, setPastedText] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [screeningData, setScreeningData] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  // Load initial backend health and sample presets
  useEffect(() => {
    async function init() {
      const h = await checkHealth();
      setHealth(h);
      const p = await fetchSampleJDs();
      setPresets(p);
    }
    init();
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    // Validation
    if (inputMode === 'pdf') {
      if (!selectedFile) {
        setErrorMessage('Please upload a PDF resume file before analyzing.');
        return;
      }
    } else {
      if (!pastedText.trim()) {
        setErrorMessage('Please paste candidate resume text before analyzing.');
        return;
      }
    }

    setIsLoading(true);

    try {
      let result = null;
      if (inputMode === 'pdf' && selectedFile) {
        result = await uploadResumeFile(selectedFile, jobDescription);
      } else {
        result = await screenResumeText({
          resume_text: pastedText,
          job_description: jobDescription,
          filename: 'Pasted Candidate Resume'
        });
      }
      setScreeningData(result);
    } catch (err) {
      console.error('[Screening Error]:', err);
      setErrorMessage(err.message || 'An error occurred during resume screening.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <Header health={health} />

      {/* Error Alert */}
      {errorMessage && (
        <div className="alert-error">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <div>{errorMessage}</div>
        </div>
      )}

      {/* Main Input Form */}
      <form onSubmit={handleAnalyze}>
        <div className="input-grid">
          <ResumeInput
            inputMode={inputMode}
            setInputMode={setInputMode}
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
            pastedText={pastedText}
            setPastedText={setPastedText}
          />

          <JobDescriptionInput
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            presets={presets}
          />
        </div>

        {/* Submit Button */}
        <div className="action-section">
          <button
            type="submit"
            className="primary-btn"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <div className="spinner"></div>
                <span>Analyzing Resume & Matching Fit...</span>
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <span>Analyze Resume & JD Match</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Results Section */}
      {screeningData && (
        <section id="results" style={{ marginTop: '30px' }}>
          {/* KPI Metrics */}
          <MetricCards screeningData={screeningData} />

          {/* Navigation Tabs */}
          <div className="tabs-header">
            <button
              type="button"
              className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              📊 Fit Overview & Alignment
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
              onClick={() => setActiveTab('skills')}
            >
              🧩 Skill Gap Analysis
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'insights' ? 'active' : ''}`}
              onClick={() => setActiveTab('insights')}
            >
              💡 Recruiter Insights & Questions
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              📄 Candidate Profile & Text
            </button>
          </div>

          {/* Active Tab View */}
          <div style={{ marginTop: '16px' }}>
            {activeTab === 'overview' && (
              <OverviewTab
                matchResult={screeningData.match_result}
                hiringDecision={screeningData.hiring_decision}
              />
            )}

            {activeTab === 'skills' && (
              <SkillAnalysis
                matchResult={screeningData.match_result}
                hasJd={Boolean(jobDescription.trim())}
              />
            )}

            {activeTab === 'insights' && (
              <InsightsTab
                explainability={screeningData.explainability}
              />
            )}

            {activeTab === 'profile' && (
              <CandidateProfileTab
                screeningData={screeningData}
              />
            )}
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="app-footer">
        <p>
          AI Resume Screening & Fit Assessment System v2.5 • Powered by FastAPI & Scikit-Learn
        </p>
        <p style={{ marginTop: '4px', fontSize: '0.75rem' }}>
          Assistive Decision Support Tool for Recruiters. Final hiring decisions are subject to human review.
        </p>
      </footer>
    </div>
  );
}
