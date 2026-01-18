import React, { useState, useEffect, useCallback } from 'react';
import { fetchMindState, ChatWebSocket } from './services/api';
import ResonanceHUD from './components/ResonanceHUD';
import BioPanel from './components/BioPanel';
import MatrixVis from './components/MatrixVis';
import ChatInterface from './components/ChatInterface';

// Generate a random session ID if not present
const getSessionId = () => {
  let sid = localStorage.getItem('eva_session_id');
  if (!sid) {
    sid = `ses_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('eva_session_id', sid);
  }
  return sid;
};

const App = () => {
  const [mindState, setMindState] = useState(null);
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState('disconnected'); // connected, thinking, disconnected
  const [ws, setWs] = useState(null);
  const sessionId = getSessionId();

  // Load Initial State
  useEffect(() => {
    const loadState = async () => {
      const data = await fetchMindState(sessionId);
      if (data) setMindState(data);
    };
    loadState();
  }, [sessionId]);

  // Connect WebSocket
  useEffect(() => {
    const socket = new ChatWebSocket(
      sessionId,
      (data) => {
        // Message Received
        if (data.type === 'response') {
          setMessages(prev => [...prev, { role: 'assistant', content: data.text }]);
          if (data.state) {
            setMindState(prev => ({ ...prev, ...data.state }));
          }
          setStatus('connected');
        } else if (data.type === 'status') {
          if (data.status === 'thinking') setStatus('thinking');
        }
      },
      (newStatus) => setStatus(newStatus)
    );

    socket.connect();
    setWs(socket);

    return () => socket.disconnect();
  }, [sessionId]);

  const handleSend = useCallback((text) => {
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    ws?.sendMessage(text);
  }, [ws]);

  return (
    <div className="h-screen w-full bg-slate-900 text-white overflow-hidden relative selection:bg-cyan-500/30">
      {/* Background Ambience */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-900 to-black z-0" />
      <div className="absolute top-0 left-0 w-full h-[500px] bg-cyan-500/5 blur-[120px] rounded-full pointer-events-none" />

      {/* Foreground Content */}
      <div className="relative z-10 flex flex-col h-full">

        {/* Top HUD */}
        <ResonanceHUD
          ri={mindState?.resonance_index}
          emotion={mindState?.emotion_label}
          status={status}
          qualia={mindState?.qualia}
        />

        {/* Main Grid */}
        <div className="flex-1 pt-20 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 h-full overflow-hidden">

          {/* Left: Visualization Dashboard (4 cols) */}
          <div className="lg:col-span-4 flex flex-col space-y-6 overflow-y-auto pr-2 scrollbar-none">

            {/* 1. Bio Panel (Hormones + Vitals) */}
            <BioPanel physio={mindState?.physio} />

            {/* 2. Matrix Visualization (9D Radar) */}
            <MatrixVis data={mindState?.eva_matrix} />

            {/* 3. Debug / JSON View (Optional, maybe hidden or bottom) */}
            <div className="p-4 rounded-xl border border-white/5 bg-black/20 text-[10px] font-mono text-gray-500 overflow-hidden h-32">
              <div className="opacity-50 mb-2">RAW STATE SNAPSHOT</div>
              <pre>{JSON.stringify({
                emotion: mindState?.emotion_label,
                ri: mindState?.resonance_index?.toFixed(3)
              }, null, 2)}</pre>
            </div>
          </div>

          {/* Right: Chat Interface (8 cols) */}
          <div className="lg:col-span-8 h-full">
            <ChatInterface
              messages={messages}
              onSend={handleSend}
              status={status}
            />
          </div>

        </div>
      </div>
    </div>
  );
};

export default App;
