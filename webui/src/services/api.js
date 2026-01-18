import axios from 'axios';

const API_BASE = '/api';
const WS_BASE = window.location.protocol === 'https:' ? 'wss://' : 'ws://' + window.location.host + '/ws/chat';

export const fetchMindState = async (sessionId) => {
    try {
        const response = await axios.get(`${API_BASE}/mind/state`, {
            params: { session_id: sessionId }
        });
        return response.data;
    } catch (error) {
        console.error("Failed to fetch mind state:", error);
        return null;
    }
};

export class ChatWebSocket {
    constructor(clientId, onMessage, onStatus) {
        this.clientId = clientId;
        this.onMessage = onMessage;
        this.onStatus = onStatus;
        this.ws = null;
        this.reconnectAttempts = 0;
    }

    connect() {
        this.ws = new WebSocket(`${WS_BASE}/${this.clientId}`);

        this.ws.onopen = () => {
            console.log('Connected to EVA Resonance Bus');
            this.reconnectAttempts = 0;
            if (this.onStatus) this.onStatus('connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (this.onMessage) this.onMessage(data);
            } catch (e) {
                console.error('WS Parse Error:', e);
            }
        };

        this.ws.onclose = () => {
            console.log('Disconnected from EVA Resonance Bus');
            if (this.onStatus) this.onStatus('disconnected');
            this.attemptReconnect();
        };

        this.ws.onerror = (err) => {
            console.error('WS Error:', err);
        };
    }

    sendMessage(text) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ message: text }));
        } else {
            console.warn("WebSocket not open");
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < 5) {
            this.reconnectAttempts++;
            setTimeout(() => this.connect(), 2000 * this.reconnectAttempts);
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}
