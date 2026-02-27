import { BarChart3, FileText, CheckCircle, Clock, XCircle } from 'lucide-react';
import { useEffect, useState } from 'react';
import { titleApi } from '../api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await titleApi.getStats();
      setStats(data);
    } catch (err) {
      setError('Failed to load statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="animate-pulse space-y-4">
            <div className="h-12 bg-slate-200 rounded-lg" />
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {[1, 2, 3, 4, 5].map(i => (
                <div key={i} className="h-32 bg-slate-200 rounded-lg" />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="card bg-red-50 border border-red-200">
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      label: 'Total Titles',
      value: stats?.total_titles || 0,
      icon: FileText,
      color: 'blue',
    },
    {
      label: 'Applications',
      value: stats?.total_applications || 0,
      icon: BarChart3,
      color: 'purple',
    },
    {
      label: 'Pending',
      value: stats?.pending_applications || 0,
      icon: Clock,
      color: 'yellow',
    },
    {
      label: 'Approved',
      value: stats?.approved_applications || 0,
      icon: CheckCircle,
      color: 'green',
    },
    {
      label: 'Rejected',
      value: stats?.rejected_applications || 0,
      icon: XCircle,
      color: 'red',
    },
  ];

  const colorMap = {
    blue: 'bg-blue-50 text-blue-700 border-blue-200',
    purple: 'bg-purple-50 text-purple-700 border-purple-200',
    yellow: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    green: 'bg-green-50 text-green-700 border-green-200',
    red: 'bg-red-50 text-red-700 border-red-200',
  };

  const iconColors = {
    blue: 'text-blue-600',
    purple: 'text-purple-600',
    yellow: 'text-yellow-600',
    green: 'text-green-600',
    red: 'text-red-600',
  };

  return (
    <div id="dashboard" className="min-h-screen bg-gradient-to-b from-white to-slate-50 py-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="section-title">System Dashboard</h2>
        <p className="section-subtitle">Real-time statistics of the verification system</p>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          {statCards.map((stat, idx) => {
            const Icon = stat.icon;
            return (
              <div
                key={idx}
                className={`card border ${colorMap[stat.color]} hover:shadow-lg`}
              >
                <div className="flex items-center justify-between mb-4">
                  <p className="text-sm font-semibold text-slate-600">{stat.label}</p>
                  <Icon size={24} className={iconColors[stat.color]} />
                </div>
                <p className="text-4xl font-bold text-slate-900">{stat.value.toLocaleString()}</p>
              </div>
            );
          })}
        </div>

        {/* Summary Card */}
        <div className="card">
          <h3 className="text-xl font-bold text-slate-900 mb-6">Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-slate-600 mb-2">Database Capacity</p>
              <p className="text-2xl font-bold text-blue-600">
                {((stats?.total_titles / 160000) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-slate-600 mt-2">
                {stats?.total_titles?.toLocaleString()} / 160,000 titles loaded
              </p>
            </div>

            <div className="p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-slate-600 mb-2">Application Status</p>
              <p className="text-2xl font-bold text-purple-600">
                {stats?.total_applications || 0}
              </p>
              <p className="text-xs text-slate-600 mt-2">
                {((stats?.approved_applications / (stats?.total_applications || 1)) * 100).toFixed(0)}% approval rate
              </p>
            </div>

            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-slate-600 mb-2">System Health</p>
              <p className="text-2xl font-bold text-green-600">✓ Operational</p>
              <p className="text-xs text-slate-600 mt-2">All systems running normally</p>
            </div>
          </div>
        </div>

        {/* Info Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <div className="card">
            <h4 className="font-bold text-slate-900 mb-3">How to Use</h4>
            <ol className="space-y-2 text-sm text-slate-700">
              <li><span className="font-semibold">1.</span> Enter your publication title in the verification form</li>
              <li><span className="font-semibold">2.</span> Review the similarity score and violations</li>
              <li><span className="font-semibold">3.</span> Submit your application with email address</li>
              <li><span className="font-semibold">4.</span> Track your application status</li>
            </ol>
          </div>

          <div className="card">
            <h4 className="font-bold text-slate-900 mb-3">Compliance Rules</h4>
            <ul className="space-y-2 text-sm text-slate-700">
              <li>✗ Disallowed words: Police, Crime, Corruption, CBI, CID, Army</li>
              <li>✗ No periodicity additions: daily, weekly, monthly</li>
              <li>✗ Cannot combine existing titles</li>
              <li>✗ Cross-language similarities checked</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
