import { useEffect, useState } from 'react';
import { GitBranch, AlertTriangle, Clock, ChevronDown, ChevronUp } from 'lucide-react';
import { titleApi } from '../api';

export default function ConflictTimeline({ title }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState({});

  useEffect(() => {
    if (!title || title.trim().length < 2) return;
    setLoading(true);
    titleApi.getConflictTimeline(title)
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [title]);

  if (loading) return (
    <div className="mt-6 p-4 bg-slate-50 rounded-xl border border-slate-200 animate-pulse">
      <div className="h-4 bg-slate-200 rounded w-1/3 mb-3" />
      <div className="h-3 bg-slate-200 rounded w-2/3" />
    </div>
  );

  if (!data || !data.root_title) return null;

  const toggleExpand = (i) => setExpanded(prev => ({ ...prev, [i]: !prev[i] }));

  return (
    <div className="mt-6 bg-white rounded-xl border border-orange-200 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-50 to-red-50 px-5 py-4 border-b border-orange-200">
        <div className="flex items-center gap-2 mb-1">
          <GitBranch size={18} className="text-orange-600" />
          <h3 className="font-bold text-slate-800 text-base">Conflict Ancestry & Timeline</h3>
        </div>
        <p className="text-xs text-slate-500">{data.summary}</p>
      </div>

      {/* Timeline */}
      <div className="p-5">
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-4 top-2 bottom-2 w-0.5 bg-gradient-to-b from-orange-300 via-red-300 to-slate-200" />

          <div className="space-y-6 ml-10">

            {/* ROOT NODE */}
            <div className="relative">
              <div className="absolute -left-10 top-1 w-4 h-4 rounded-full bg-orange-500 border-2 border-white shadow" />
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-orange-700 uppercase tracking-wide">Root Title</span>
                    <p className="font-bold text-slate-800 mt-0.5">{data.root_title}</p>
                  </div>
                  <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full font-semibold">
                    {data.root_similarity}% match
                  </span>
                </div>
              </div>
            </div>

            {/* CONFLICT CHAIN */}
            {data.conflict_chain.map((node, i) => (
              <div key={i} className="relative">
                <div className="absolute -left-10 top-1 w-4 h-4 rounded-full bg-red-400 border-2 border-white shadow" />

                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-xs font-bold text-red-600 uppercase tracking-wide">Similar Registered</span>
                      <p className="font-semibold text-slate-800 mt-0.5">{node.root_title}</p>
                    </div>
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full font-semibold">
                      {node.similarity_to_new}% similar
                    </span>
                  </div>

                  {/* Rejected siblings */}
                  {node.related_rejections.length > 0 && (
                    <div className="mt-3">
                      <button
                        onClick={() => toggleExpand(i)}
                        className="flex items-center gap-1 text-xs text-red-600 font-semibold hover:text-red-800"
                      >
                        <AlertTriangle size={12} />
                        {node.related_rejections.length} previously rejected title(s) in this family
                        {expanded[i] ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                      </button>

                      {expanded[i] && (
                        <div className="mt-2 space-y-2">
                          {node.related_rejections.map((rej, j) => (
                            <div key={j} className="bg-white border border-red-100 rounded p-2">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-slate-700 text-sm">"{rej.title}"</span>
                                <span className="text-xs text-red-500 font-semibold">{rej.similarity_score}%</span>
                              </div>
                              <div className="flex items-center gap-1 mt-1">
                                <Clock size={10} className="text-slate-400" />
                                <span className="text-xs text-slate-400">
                                  {rej.rejected_at ? new Date(rej.rejected_at).toLocaleDateString() : 'Unknown date'}
                                </span>
                              </div>
                              <p className="text-xs text-slate-500 mt-1">{rej.reason}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* NEW TITLE NODE */}
            <div className="relative">
              <div className="absolute -left-10 top-1 w-4 h-4 rounded-full bg-blue-500 border-2 border-white shadow animate-pulse" />
              <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-blue-700 uppercase tracking-wide">Your Submitted Title</span>
                    <p className="font-bold text-slate-800 mt-0.5">"{data.title}"</p>
                  </div>
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-semibold">
                    Now
                  </span>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Family Summary */}
        {data.total_rejected_in_family > 0 && (
          <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg flex items-start gap-2">
            <AlertTriangle size={16} className="text-amber-600 mt-0.5 shrink-0" />
            <p className="text-xs text-amber-800">
              <strong>{data.total_rejected_in_family} title(s)</strong> have been previously rejected
              for being too similar to this conflict family. Your title falls into the same ancestry chain.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}