import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Brain } from 'lucide-react';

const ResonanceHUD = ({ ri, emotion, status, qualia }) => {
    // Determine color based on RI strength
    const riColor = ri > 0.8 ? 'text-amber-400' : ri > 0.5 ? 'text-cyan-400' : 'text-gray-400';
    const glow = ri > 0.8 ? 'drop-shadow-[0_0_8px_rgba(251,191,36,0.8)]' : 'drop-shadow-[0_0_5px_rgba(34,211,238,0.5)]';

    const isThinking = status === 'thinking';

    return (
        <div className="flex justify-between items-center bg-black/40 backdrop-blur-lg border-b border-white/10 p-4 px-6 fixed top-0 w-full z-50">
            <div className="flex items-center space-x-4">
                <div className="flex flex-col">
                    <span className="text-[10px] text-gray-500 font-mono tracking-widest">RESONANCE IDX</span>
                    <div className={`text-2xl font-bold font-mono ${riColor} ${glow} flex items-center`}>
                        <Zap size={18} className="mr-2" />
                        {(ri || 0).toFixed(2)}
                    </div>
                </div>

                <div className="h-8 w-[1px] bg-white/10 mx-2"></div>

                <div className="flex flex-col">
                    <span className="text-[10px] text-gray-500 font-mono tracking-widest">STATE</span>
                    <span className="text-sm font-medium text-white">{emotion || "Neutral"}</span>
                </div>
            </div>

            <div className="flex items-center space-x-4">
                {qualia?.tone && (
                    <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-purple-300">
                        Tone: {qualia.tone}
                    </div>
                )}

                <motion.div
                    animate={{ opacity: isThinking ? [0.5, 1, 0.5] : 1 }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                    className={`flex items-center space-x-2 px-3 py-1 rounded border ${isThinking ? 'border-green-500/50 text-green-400' : 'border-gray-700 text-gray-500'}`}
                >
                    <Brain size={14} />
                    <span className="text-xs font-bold">{isThinking ? "PROCESSING" : "READY"}</span>
                </motion.div>
            </div>
        </div>
    );
};

export default ResonanceHUD;
