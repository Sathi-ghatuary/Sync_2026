import { Search, Loader, AlertCircle, CheckCircle, Info } from 'lucide-react';
import { useState } from 'react';
import { titleApi } from '../api';

export default function VerificationForm({ onResult }) {
  const [title, setTitle] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [submitMode, setSubmitMode] = useState('verify'); // 'verify' or 'submit'

  const handleVerify = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Please enter a title');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await titleApi.verify(title);
      onResult(result);
      if (submitMode === 'submit') {
        // Show success message but keep the result displayed
      }
    } catch (err) {
      setError(err.detail || 'Error verifying title');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitApplication = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Please enter a title');
      return;
    }
    if (!email.trim()) {
      setError('Please enter your email');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await titleApi.submitApplication(title, email);
      onResult(result);
      setTitle('');
      setEmail('');
      alert('Application submitted successfully!');
    } catch (err) {
      setError(err.detail || 'Error submitting application');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="verify" className="min-h-screen bg-gradient-to-b from-blue-50 to-white pt-32 pb-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="section-title">Verify Your Publication Title</h2>
          <p className="section-subtitle">
            Check for similarity with existing titles and ensure compliance with guidelines
          </p>
        </div>

        {/* Form Container */}
        <div className="card shadow-2xl">
          {/* Mode Selector */}
          <div className="flex gap-4 mb-8 border-b pb-6">
            <button
              onClick={() => setSubmitMode('verify')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                submitMode === 'verify'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
              }`}
            >
              Quick Verify
            </button>
            <button
              onClick={() => setSubmitMode('submit')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                submitMode === 'submit'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
              }`}
            >
              Submit Application
            </button>
          </div>

          <form onSubmit={submitMode === 'verify' ? handleVerify : handleSubmitApplication}>
            {/* Title Input */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Publication Title
              </label>
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Enter your publication title..."
                  className="input-field pl-12"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Email Input (only for submission) */}
            {submitMode === 'submit' && (
              <div className="mb-6">
                <label className="block text-sm font-semibold text-slate-700 mb-3">
                  Email Address
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your.email@example.com"
                  className="input-field"
                  disabled={loading}
                />
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3 items-start">
                <AlertCircle size={20} className="text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !title.trim()}
              className="btn-primary w-full"
            >
              {loading ? (
                <>
                  <Loader size={20} className="animate-spin" />
                  {submitMode === 'verify' ? 'Verifying...' : 'Submitting...'}
                </>
              ) : (
                <>
                  {submitMode === 'verify' ? 'Verify Title' : 'Submit Application'}
                </>
              )}
            </button>
          </form>

          {/* Info Box */}
          <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg flex gap-3">
            <Info size={20} className="text-blue-600 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-blue-800">
              <p className="font-semibold mb-1">How it works:</p>
              <p>Our system checks your title against existing publications, verifies compliance with guidelines, and provides a verification probability score.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
