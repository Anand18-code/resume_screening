import React from 'react';

export default function OverviewTab({ matchResult, hiringDecision }) {
  if (!matchResult || !hiringDecision) return null;

  const scoreVal = matchResult.composite_score || 0;
  const decision = hiringDecision.decision || 'Review';
  const category = hiringDecision.category || 'Review';
  const reason = hiringDecision.reason || '';

  const candExp = matchResult.candidate_experience > 0 
    ? `${matchResult.candidate_experience} Year(s)` 
    : '0 Years (Fresher)';

  const getScoreColor = (val) => {
    if (val >= 70) return '#10b981';
    if (val >= 45) return '#f59e0b';
    return '#f43f5e';
  };

  return (
    <div>
      {/* Recommendation Banner */}
      <div className={`rec-banner ${category}`}>
        <div className="rec-title">
          Screening Status: {decision}
        </div>
        <div className="rec-reason">
          <strong>Rationale:</strong> {reason}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
        {/* Score Breakdown Card */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1.05rem', marginBottom: '14px' }}>Composite Match Evaluation</h4>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Overall Score</span>
            <span style={{ fontSize: '1.1rem', fontWeight: '800', color: getScoreColor(scoreVal) }}>
              {scoreVal}%
            </span>
          </div>

          <div className="progress-bar-bg">
            <div
              className="progress-bar-fill"
              style={{
                width: `${Math.min(Math.max(scoreVal, 0), 100)}%`,
                backgroundColor: getScoreColor(scoreVal)
              }}
            />
          </div>

          <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '12px' }}>
            Calculated via: 50% Skill Coverage + 30% Contextual Semantics + 20% Experience Qualification.
          </p>
        </div>

        {/* Alignment Criteria Table */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1.05rem', marginBottom: '10px' }}>Requirement Alignment</h4>
          <table className="custom-table">
            <thead>
              <tr>
                <th>Criteria</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Skills Matched</td>
                <td><strong>{matchResult.total_matched_skills} / {matchResult.total_required_skills}</strong> required</td>
              </tr>
              <tr>
                <td>Semantic Relevance</td>
                <td>{matchResult.semantic_score}% contextual overlap</td>
              </tr>
              <tr>
                <td>Candidate Experience</td>
                <td>{candExp}</td>
              </tr>
              <tr>
                <td>Experience Fit</td>
                <td>{matchResult.experience_status}</td>
              </tr>
              <tr>
                <td>Education Level</td>
                <td>{matchResult.candidate_education}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
