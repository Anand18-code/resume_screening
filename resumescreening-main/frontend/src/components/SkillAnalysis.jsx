import React from 'react';

export default function SkillAnalysis({ matchResult, hasJd }) {
  if (!matchResult) return null;

  const matchedSkills = matchResult.matched_skills || [];
  const missingSkills = matchResult.missing_skills || [];
  const extraSkills = matchResult.extra_skills || [];

  return (
    <div>
      <h3 style={{ marginBottom: '16px', fontSize: '1.2rem' }}>Detailed Skill Alignment & Gap Analysis</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        {/* Matched Skills */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <h4 style={{ color: '#10b981', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1rem' }}>
            <span>✅</span> Matched Skills ({matchedSkills.length})
          </h4>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: '4px 0 10px' }}>
            Required in JD & verified in candidate resume:
          </p>
          <div className="badge-container">
            {matchedSkills.length > 0 ? (
              matchedSkills.map((skill) => (
                <span key={skill} className="badge badge-matched">
                  {skill}
                </span>
              ))
            ) : (
              <span style={{ color: '#64748b', fontSize: '0.85rem' }}>No direct required skill matches found.</span>
            )}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <h4 style={{ color: '#f43f5e', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1rem' }}>
            <span>⚠️</span> Missing Required Skills ({missingSkills.length})
          </h4>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: '4px 0 10px' }}>
            Required in JD but absent from resume:
          </p>
          <div className="badge-container">
            {missingSkills.length > 0 ? (
              missingSkills.map((skill) => (
                <span key={skill} className="badge badge-missing">
                  {skill}
                </span>
              ))
            ) : (
              <span style={{ color: '#10b981', fontSize: '0.85rem' }}>
                {hasJd ? 'All required skills are present in the resume!' : 'No Job Description provided.'}
              </span>
            )}
          </div>
        </div>

        {/* Extra Skills */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <h4 style={{ color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1rem' }}>
            <span>💡</span> Additional Skills ({extraSkills.length})
          </h4>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: '4px 0 10px' }}>
            Candidate strengths outside JD requirements:
          </p>
          <div className="badge-container">
            {extraSkills.length > 0 ? (
              extraSkills.map((skill) => (
                <span key={skill} className="badge badge-extra">
                  {skill}
                </span>
              ))
            ) : (
              <span style={{ color: '#64748b', fontSize: '0.85rem' }}>No additional technical skills detected.</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
