import { useState, useEffect } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import VerificationForm from './components/VerificationForm';
import ResultsDisplay from './components/ResultsDisplay';
import Dashboard from './components/Dashboard';
import Footer from './components/Footer';
import { titleApi } from './api';

function App() {
  const [result, setResult] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check if backend is connected
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      await titleApi.healthCheck();
      setIsConnected(true);
    } catch (err) {
      setIsConnected(false);
      console.error('Backend connection failed:', err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />

      {/* Connection Status Banner */}
      {!isConnected && (
        <div className="bg-red-500 text-white py-3 text-center fixed w-full top-16 z-40">
          <p className="text-sm font-semibold">
            ⚠️ Backend not connected. Make sure the API server is running at {import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}
          </p>
        </div>
      )}

      <main className={isConnected ? 'pt-16' : 'pt-32'}>
        <Hero />
        <VerificationForm onResult={setResult} />
        {result && <ResultsDisplay result={result} />}
        <Dashboard />
      </main>

      <Footer />
    </div>
  );
}

export default App;
