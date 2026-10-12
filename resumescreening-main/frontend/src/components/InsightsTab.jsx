import React from 'react';

export default function InsightsTab({ explainability }) {
  if (!explainability) return null;

  const reasons = explainability.summary_reasons || [];
  const questions = explainability.interview_questions || [];
  const tips = explainability.improvement_tips || [];

  return (
    <div>
      {/* Decision Factors */}
      <div className="glass-card" style={{ marginBottom: '20px' }}>
        <h4 style={{ fontSize: '1.05rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🔍</span> Explainable AI Decision Factors
        </h4>
        <ul className="insight-list">
          {reasons.map((r, idx) => (
            <li key={idx} className="insight-item">
              <span>{r}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Tailored Screening Questions */}
      <div className="glass-card" style={{ marginBottom: '20px' }}>
        <h4 style={{ fontSize: '1.05rem', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🎯</span> Tailored Technical Screening Interview Questions
        </h4>
        <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '14px' }}>
          Auto-generated for recruiters based on candidate's skill matches and identified gaps:
        </p>
        <ul className="insight-list">
          {questions.map((q, idx) => (
            <li key={idx} className="insight-item">
              <span className="insight-num">{idx + 1}</span>
              <span style={{ fontWeight: '500' }}>{q}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Improvement Tips */}
      <div className="glass-card">
        <h4 style={{ fontSize: '1.05rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🚀</span> Candidate Resume Improvement Recommendations
        </h4>
        <ul className="insight-list">
          {tips.map((t, idx) => (
            <li key={idx} className="insight-item">
              <span style={{ color: '#38bdf8' }}>💡</span>
              <span>{t}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
