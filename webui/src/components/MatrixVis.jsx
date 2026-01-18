import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

const MatrixVis = ({ data }) => {
    if (!data) return <div className="text-white/50 p-4">Orbiting Void...</div>;

    // Transform object to array for Recharts
    // data = { joy: 0.5, trust: 0.2, ... }
    const chartData = Object.keys(data).map(key => ({
        subject: key.charAt(0).toUpperCase() + key.slice(1),
        A: data[key] * 100, // Scale to 0-100
        fullMark: 100
    }));

    return (
        <div className="w-full h-64 relative backdrop-blur-md bg-white/5 rounded-xl border border-white/10 p-4 shadow-lg overflow-hidden">
            <div className="absolute top-2 left-2 text-xs font-mono text-cyan-400 opacity-80">
                EVA MATRIX [9D]
            </div>

            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
                    <PolarGrid stroke="#ffffff20" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#a0aec0', fontSize: 10 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                        name="Psych State"
                        dataKey="A"
                        stroke="#8884d8"
                        strokeWidth={2}
                        fill="#8884d8"
                        fillOpacity={0.4}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default MatrixVis;
