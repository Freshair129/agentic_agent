import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Activity } from 'lucide-react';

const HormoneBar = ({ label, value, color }) => (
    <div className="mb-2">
        <div className="flex justify-between text-xs text-gray-400 mb-1">
            <span>{label.toUpperCase()}</span>
            <span>{(value * 100).toFixed(0)}%</span>
        </div>
        <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
            <motion.div
                className={`h-full ${color}`}
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(value * 100, 100)}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
            />
        </div>
    </div>
);

const BioPanel = ({ physio }) => {
    const hormones = physio?.hormones || {};
    const vitals = physio?.vitals || {};

    // Color mapping for hormones
    const getHormoneColor = (name) => {
        switch (name) {
            case 'cortisol': return 'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]';
            case 'dopamine': return 'bg-yellow-400 shadow-[0_0_10px_rgba(250,204,21,0.5)]';
            case 'serotonin': return 'bg-blue-400 shadow-[0_0_10px_rgba(96,165,250,0.5)]';
            case 'oxytocin': return 'bg-pink-400 shadow-[0_0_10px_rgba(244,114,182,0.5)]';
            case 'adrenaline': return 'bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.5)]';
            default: return 'bg-gray-400';
        }
    };

    return (
        <div className="w-full backdrop-blur-md bg-white/5 rounded-xl border border-white/10 p-4 shadow-lg text-white">
            <div className="flex justify-between items-center mb-4">
                <div className="text-xs font-mono text-cyan-400 opacity-80">PHYSIO CORE</div>

                {/* Vitals Display */}
                <div className="flex space-x-4">
                    <div className="flex items-center space-x-1">
                        <motion.div
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{
                                duration: 60 / (vitals.bpm || 60),
                                repeat: Infinity
                            }}
                        >
                            <Heart size={14} className="text-red-500 fill-red-500" />
                        </motion.div>
                        <span className="text-xs font-bold">{Math.round(vitals.bpm || 0)} BPM</span>
                    </div>
                    <div className="flex items-center space-x-1 text-blue-400">
                        <Activity size={14} />
                        <span className="text-xs">{Math.round((vitals.hrv || 0) * 100)} HRV</span>
                    </div>
                </div>
            </div>

            <div className="space-y-3">
                {Object.entries(hormones).map(([name, val]) => (
                    <HormoneBar
                        key={name}
                        label={name}
                        value={val}
                        color={getHormoneColor(name)}
                    />
                ))}
            </div>
        </div>
    );
};

export default BioPanel;
