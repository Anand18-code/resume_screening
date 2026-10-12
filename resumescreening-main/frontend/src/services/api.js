/**
 * REST API client service for communicating with the FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Checks backend health and model readiness status.
 * @returns {Promise<Object>}
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`Health check returned status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.warn('[API] Health check failed:', error.message);
    return { status: 'offline', category_model_loaded: false };
  }
}

/**
 * Fetches sample job description presets.
 * @returns {Promise<Object>}
 */
export async function fetchSampleJDs() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/sample-jds`);
    if (!response.ok) {
      throw new Error('Failed to fetch sample job descriptions');
    }
    const data = await response.json();
    return data.presets || {};
  } catch (error) {
    console.warn('[API] Failed to fetch sample JDs:', error.message);
    return {};
  }
}

/**
 * Performs resume screening with raw pasted text.
 * @param {Object} payload { resume_text, job_description, filename }
 * @returns {Promise<Object>}
 */
export async function screenResumeText(payload) {
  const response = await fetch(`${API_BASE_URL}/api/screen-resume`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      resume_text: payload.resume_text,
      job_description: payload.job_description || '',
      filename: payload.filename || 'Pasted Resume.txt',
    }),
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `Server returned error (${response.status})`);
  }

  return await response.json();
}

/**
 * Uploads a PDF resume file and screens it against the target JD.
 * @param {File} file PDF file
 * @param {string} jobDescription Target JD text
 * @returns {Promise<Object>}
 */
export async function uploadResumeFile(file, jobDescription = '') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_description', jobDescription);

  const response = await fetch(`${API_BASE_URL}/api/upload-resume`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `Failed to screen uploaded PDF (${response.status})`);
  }

  return await response.json();
}

export { API_BASE_URL };
