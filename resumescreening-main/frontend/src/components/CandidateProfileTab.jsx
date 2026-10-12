import React, { useState } from 'react';

export default function CandidateProfileTab({ screeningData }) {
  const [showRawText, setShowRawText] = useState(false);

  if (!screeningData) return null;

  const { document_name, profile } = screeningData;
  const expVal = profile?.experience_years > 0 
    ? `${profile.experience_years} Year(s)` 
    : '0 Years (Fresher / Entry-Level)';

  return (
    <div>
      <div className="glass-card" style={{ marginBottom: '20px' }}>
        <h4 style={{ fontSize: '1.05rem', marginBottom: '16px' }}>Extracted Candidate Profile Attributes</h4>
        
        <table className="custom-table">
          <thead>
            <tr>
              <th style={{ width: '35%' }}>Attribute</th>
              <th>Extracted Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Document / Source</strong></td>
              <td>{document_name || 'Resume Document'}</td>
            </tr>
            <tr>
              <td><strong>Total Detected Skills</strong></td>
              <td>
                <span className="badge badge-extra" style={{ margin: 0 }}>
                  {profile?.skills?.length || 0} Skills Detected
                </span>
              </td>
            </tr>
            <tr>
              <td><strong>Estimated Experience</strong></td>
              <td>{expVal}</td>
            </tr>
            <tr>
              <td><strong>Highest Detected Education</strong></td>
              <td>{profile?.education || 'B.Tech / Bachelor\'s'}</td>
            </tr>
            <tr>
              <td><strong>Detected Certifications</strong></td>
              <td>{profile?.certification || 'None detected'}</td>
            </tr>
            <tr>
              <td><strong>Estimated Project Count</strong></td>
              <td>{profile?.projects_count || 1} Project(s)</td>
            </tr>
          </tbody>
        </table>
      </div>

      {profile?.clean_text && (
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h4 style={{ fontSize: '1rem' }}>Normalized Resume Text Content</h4>
            <button
              type="button"
              onClick={() => setShowRawText(!showRawText)}
              style={{
                background: 'rgba(255, 255, 255, 0.08)',
                border: '1px solid var(--border-subtle)',
                color: '#94a3b8',
                padding: '6px 12px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '0.8rem'
              }}
            >
              {showRawText ? 'Hide Text' : 'View Extracted Text'}
            </button>
          </div>

          {showRawText && (
            <textarea
              readOnly
              className="custom-textarea"
              style={{ height: '220px', fontFamily: 'monospace', fontSize: '0.85rem' }}
              value={profile.clean_text}
            />
          )}
        </div>
      )}
    </div>
  );
}
