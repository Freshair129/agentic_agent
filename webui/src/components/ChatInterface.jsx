import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ChatInterface = ({ messages, onSend, status }) => {
    const [input, setInput] = useState('');
    const endRef = useRef(null);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim()) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <div className="flex flex-col h-full bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 overflow-hidden shadow-2xl">
            <div className="p-4 border-b border-white/10 bg-black/20">
                <h2 className="text-sm font-bold text-gray-300 flex items-center">
                    <Bot size={16} className="mr-2 text-cyan-400" />
                    SESSION LOG
                </h2>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-white/20">
                <AnimatePresence>
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed ${msg.role === 'user'
                                        ? 'bg-blue-600/80 text-white rounded-tr-sm'
                                        : 'bg-white/10 text-gray-200 rounded-tl-sm border border-white/5'
                                    }`}
                            >
                                {msg.content}
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {status === 'thinking' && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex justify-start"
                    >
                        <div className="px-3 py-2 bg-white/5 rounded-full flex space-x-1">
                            <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce" />
                            <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce delay-75" />
                            <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce delay-150" />
                        </div>
                    </motion.div>
                )}
                <div ref={endRef} />
            </div>

            <form onSubmit={handleSubmit} className="p-4 bg-black/20 border-t border-white/10 flex space-x-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Resonate with EVA..."
                    className="flex-1 bg-black/40 border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-cyan-500/50 transition-colors"
                />
                <button
                    type="submit"
                    className="p-2 bg-cyan-500/20 hover:bg-cyan-500/40 text-cyan-400 rounded-lg transition-colors"
                >
                    <Send size={18} />
                </button>
            </form>
        </div>
    );
};

export default ChatInterface;
