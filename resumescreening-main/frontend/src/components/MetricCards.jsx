import React from 'react';

export default function MetricCards({ screeningData }) {
  if (!screeningData) return null;

  const { match_result, hiring_decision, predicted_category } = screeningData;
  const scoreVal = match_result?.composite_score || 0;
  const skillScore = match_result?.skill_score || 0;
  const matchedCount = match_result?.total_matched_skills || 0;
  const reqCount = match_result?.total_required_skills || 0;
  const grade = match_result?.grade || 'Assessment';
  
  const decision = hiring_decision?.decision || 'Review';
  const decisionCat = hiring_decision?.category || 'Review';
  const confidence = hiring_decision?.confidence || 80.0;

  const getScoreColor = (val) => {
    if (val >= 70) return '#10b981';
    if (val >= 45) return '#f59e0b';
    return '#f43f5e';
  };

  const getDecisionColor = (cat) => {
    if (cat === 'Hire') return '#10b981';
    if (cat === 'Review') return '#f59e0b';
    return '#f43f5e';
  };

  return (
    <div className="kpi-grid">
      {/* Overall Score */}
      <div className="kpi-card">
        <div className="kpi-label">Overall Match Score</div>
        <div className="kpi-value" style={{ color: getScoreColor(scoreVal) }}>
          {scoreVal}%
        </div>
        <div className="kpi-sub">{grade}</div>
      </div>

      {/* Skill Coverage */}
      <div className="kpi-card">
        <div className="kpi-label">Skill Coverage</div>
        <div className="kpi-value" style={{ color: '#ffffff' }}>
          {skillScore}%
        </div>
        <div className="kpi-sub">
          {matchedCount} of {reqCount} skills matched
        </div>
      </div>

      {/* Recommendation */}
      <div className="kpi-card">
        <div className="kpi-label">Screening Recommendation</div>
        <div className="kpi-value" style={{ color: getDecisionColor(decisionCat), fontSize: '1.25rem' }}>
          {decision}
        </div>
        <div className="kpi-sub">
          Confidence: {confidence.toFixed(1)}%
        </div>
      </div>

      {/* Domain Classifier */}
      <div className="kpi-card">
        <div className="kpi-label">Candidate Domain</div>
        <div className="kpi-value" style={{ fontSize: '1.25rem' }}>
          {predicted_category || 'General Tech'}
        </div>
        <div className="kpi-sub">NLP Domain Classifier</div>
      </div>
    </div>
  );
}
