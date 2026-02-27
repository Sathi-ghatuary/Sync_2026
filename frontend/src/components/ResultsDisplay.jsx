import { CheckCircle2, AlertTriangle, TrendingDown, Shield } from 'lucide-react';

export default function ResultsDisplay({ result }) {
  if (!result) return null;

  const getVerdict = (probability) => {
    if (probability > 0.7) return { status: 'LIKELY APPROVED', color: 'green', icon: CheckCircle2 };
    if (probability > 0.4) return { status: 'NEEDS REVIEW', color: 'yellow', icon: AlertTriangle };
    return { status: 'LIKELY REJECTED', color: 'red', icon: AlertTriangle };
  };

  const verdict = getVerdict(result.verification_probability);
  const VerdictIcon = verdict.icon;

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="section-title mb-8">Verification Results</h2>

        {/* Main Result Card */}
        <div className={`card shadow-2xl mb-8 border-l-4 ${
          verdict.color === 'green' ? 'border-green-500' :
          verdict.color === 'yellow' ? 'border-yellow-500' : 'border-red-500'
        }`}>
          {/* Title */}
          <div className="mb-8">
            <p className="text-sm text-slate-600 mb-2">Verified Title</p>
            <h3 className="text-3xl font-bold text-slate-900 break-words">{result.title}</h3>
          </div>

          {/* Verdict */}
          <div className={`mb-8 p-6 rounded-lg flex items-center gap-4 ${
            verdict.color === 'green' ? 'bg-green-50 border border-green-200' :
            verdict.color === 'yellow' ? 'bg-yellow-50 border border-yellow-200' : 'bg-red-50 border border-red-200'
          }`}>
            <VerdictIcon size={32} className={
              verdict.color === 'green' ? 'text-green-600' :
              verdict.color === 'yellow' ? 'text-yellow-600' : 'text-red-600'
            } />
            <div>
              <p className={`text-sm font-semibold ${
                verdict.color === 'green' ? 'text-green-800' :
                verdict.color === 'yellow' ? 'text-yellow-800' : 'text-red-800'
              }`}>
                {verdict.status}
              </p>
              <p className={`text-xs ${
                verdict.color === 'green' ? 'text-green-700' :
                verdict.color === 'yellow' ? 'text-yellow-700' : 'text-red-700'
              }`}>
                Based on similarity analysis and compliance checks
              </p>
            </div>
          </div>

          {/* Scores */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Similarity Score */}
            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-semibold text-slate-700">Similarity Score</p>
                <TrendingDown size={20} className="text-orange-500" />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-slate-900">
                  {(result.similarity_score * 100).toFixed(1)}%
                </span>
                <span className="text-sm text-slate-600">similarity</span>
              </div>
              <div className="w-full bg-slate-300 rounded-full h-2 mt-3">
                <div
                  className="bg-orange-500 h-2 rounded-full"
                  style={{ width: `${Math.min(result.similarity_score * 100, 100)}%` }}
                />
              </div>
            </div>

            {/* Verification Probability */}
            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-semibold text-slate-700">Approval Probability</p>
                <Shield size={20} className="text-blue-500" />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-slate-900">
                  {(result.verification_probability * 100).toFixed(1)}%
                </span>
                <span className="text-sm text-slate-600">likely approved</span>
              </div>
              <div className="w-full bg-slate-300 rounded-full h-2 mt-3">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${Math.min(result.verification_probability * 100, 100)}%` }}
                />
              </div>
            </div>
          </div>

          {/* Similar Titles */}
          {result.similar_titles && result.similar_titles.length > 0 && (
            <div className="mb-8 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <p className="text-sm font-semibold text-amber-900 mb-3">Similar Existing Titles</p>
              <ul className="space-y-2">
                {result.similar_titles.map((title, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-amber-800">
                    <span className="w-1.5 h-1.5 bg-amber-500 rounded-full" />
                    {title}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Violations */}
          {result.violations && result.violations.length > 0 && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm font-semibold text-red-900 mb-3">Rule Violations ({result.violations.length})</p>
              <ul className="space-y-2">
                {result.violations.slice(0, 5).map((violation, idx) => (
                  <li key={idx} className="text-sm text-red-800">
                    <span className="font-semibold">{violation.rule}:</span> {violation.message}
                  </li>
                ))}
                {result.violations.length > 5 && (
                  <li className="text-sm text-red-700 italic">
                    +{result.violations.length - 5} more violations
                  </li>
                )}
              </ul>
            </div>
          )}

          {/* No Violations */}
          {(!result.violations || result.violations.length === 0) && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800 flex items-center gap-2">
                <CheckCircle2 size={18} />
                No rule violations detected!
              </p>
            </div>
          )}
        </div>

        {/* Recommendations */}
        <div className="card">
          <h4 className="text-lg font-bold text-slate-900 mb-4">Recommendations</h4>
          {result.verification_probability > 0.7 ? (
            <div className="space-y-2 text-slate-700">
              <p>✓ Your title appears to be unique and compliant</p>
              <p>✓ Consider submitting this title for registration</p>
              <p>✓ Review the verification results one more time before submission</p>
            </div>
          ) : result.verification_probability > 0.4 ? (
            <div className="space-y-2 text-slate-700">
              <p>⚠ Consider modifying your title to avoid conflicts</p>
              <p>⚠ Address the flagged rule violations</p>
              <p>⚠ Verify against the similar titles listed above</p>
            </div>
          ) : (
            <div className="space-y-2 text-slate-700">
              <p>✗ This title has significant compliance issues</p>
              <p>✗ Consider choosing a different title</p>
              <p>✗ Review and address all rule violations before resubmitting</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
