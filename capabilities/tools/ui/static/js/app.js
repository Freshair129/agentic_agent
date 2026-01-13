// EVA 9.1.0 Living Sandbox
// Frontend Controller

const App = {
    elements: {
        chatHistory: document.getElementById('chat-history'),
        userInput: document.getElementById('user-input'),
        sendBtn: document.getElementById('send-btn'),
        clearBtn: document.getElementById('clear-history'),
        logs: document.getElementById('system-logs'),
        // Dashboard
        riGauge: document.getElementById('ri-gauge'),
        riVal: document.getElementById('ri-val'),
        rimGauge: document.getElementById('rim-gauge'),
        rimVal: document.getElementById('rim-val'),
        coreBars: document.querySelectorAll('.core-bar'),
        tickerGrid: document.getElementById('hormone-ticker'),
        valHR: document.getElementById('val-hr'),
        valRR: document.getElementById('val-rr'),
        barSym: document.getElementById('bar-sym'),
        valANS: document.getElementById('val-ans')
    },

    state: {
        socket: null,
        history: []
    },

    // Previous frame state for Delta calculation
    lastBlood: {},

    // Hardcoded Core 5 IDs
    CORE_IDS: [
        "ESC_H01_ADRENALINE",
        "ESC_H02_CORTISOL",
        "ESC_N02_DOPAMINE",
        "ESC_N03_SEROTONIN",
        "ESC_H04_OXYTOCIN"
    ],

    // Hardcoded Units Map
    HORMONE_UNITS: {
        "ESC_H01_ADRENALINE": "pg/mL",
        "ESC_H02_CORTISOL": "ug/dL",
        "ESC_H03_ALDOSTERONE": "ng/dL",
        "ESC_H04_OXYTOCIN": "pg/mL",
        "ESC_H05_VASOPRESSIN": "pg/mL",
        "ESC_H06_TESTOSTERONE": "ng/dL",
        "ESC_H07_ESTROGEN": "pg/mL",
        "ESC_H08_PROGESTERONE": "ng/mL",
        "ESC_H09_INSULIN": "uIU/mL",
        "ESC_H10_GLUCAGON": "pg/mL",
        "ESC_H11_LEPTIN": "ng/mL",
        "ESC_H12_GHRELIN": "pg/mL",
        "ESC_H13_THYROXINE": "ug/dL",
        "ESC_H14_MELATONIN": "pg/mL",
        "ESC_H15_GROWTH_HORMONE": "ng/mL",
        "ESC_H16_PROLACTIN": "ng/mL",
        "ESC_N01_NORADRENALINE": "pg/mL",
        "ESC_N02_DOPAMINE": "pg/mL",
        "ESC_N03_SEROTONIN": "ng/mL",
        "ESC_N04_ENDORPHIN": "pg/mL",
        "ESC_N05_GABA": "pmol/mL",
        "ESC_N06_ADENOSINE": "umol/L",
        "ESC_N07_HISTAMINE": "ng/mL"
    },

    async init() {
        this.loadHistory();
        await this.checkServer();
        this.initWebSocket();
        this.bindEvents();
        this.log("EVA Bio-Market (30Hz) Online.");
    },

    async checkServer() {
        try {
            const resp = await fetch('/health');
            const data = await resp.json();
            if (data.status === 'online') {
                this.log("Server Handshake: OK.");
            }
        } catch (e) {
            this.log("⚠️ Server Offline. Please run run_sandbox_ui.bat");
            this.appendMessage('system-msg', "CRITICAL: Backend Server not found. Make sure the Python server is running.");
        }
    },

    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.state.socket = new WebSocket(`${protocol}//${window.location.host}/ws`);

        this.state.socket.onopen = () => {
            document.querySelector('.status-indicator').classList.add('online');
            this.log("Subscribed to Physio Stream.");
        };

        this.state.socket.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.type === 'state_update') {
                this.updateDashboard(msg.data);
            }
        };

        this.state.socket.onclose = () => {
            document.querySelector('.status-indicator').classList.remove('online');
            setTimeout(() => this.initWebSocket(), 3000);
        };
    },

    bindEvents() {
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        this.elements.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.elements.clearBtn.addEventListener('click', () => {
            localStorage.removeItem('eva_chat_history');
            this.elements.chatHistory.innerHTML = '';
            this.log("Memory Cleared.");
        });
    },

    async sendMessage() {
        const text = this.elements.userInput.value.trim();
        if (!text) return;

        this.appendMessage('user', text);
        this.elements.userInput.value = '';
        this.saveHistory('user', text);
        this.scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            if (data.error) {
                this.appendMessage('system-msg', `Error: ${data.error}`);
            } else {
                this.appendMessage('eva', data.response, data.meta, data.debug);
                this.saveHistory('eva', data.response);
            }


        } catch (e) {
            this.appendMessage('system-msg', `Connection Failed: ${e}`);
        }
    },

    appendMessage(role, text, meta = null, debug = null) {
        const div = document.createElement('div');
        div.className = `message ${role}`;

        if (role === 'eva') {
            div.innerHTML = typeof marked !== 'undefined' ? marked.parse(text) : text;

            // [NEW] Add Phase 4 debug info if available
            if (meta || debug) {
                const debugDiv = document.createElement('div');
                debugDiv.className = 'message-meta';
                debugDiv.innerHTML = `
                    <div class="meta-row">
                        ${meta?.intent ? `<span class="meta-tag">Intent: ${meta.intent}</span>` : ''}
                        ${meta?.emotion ? `<span class="meta-tag">Emotion: ${meta.emotion}</span>` : ''}
                        ${meta?.confidence ? `<span class="meta-tag">Confidence: ${(meta.confidence * 100).toFixed(0)}%</span>` : ''}
                        ${debug?.perception_delegated !== undefined ?
                        `<span class="meta-tag ${debug.perception_delegated ? 'delegated' : 'refined'}">
                                ${debug.perception_delegated ? '🎯 SLM Delegated' : '🧠 LLM Refined'}
                            </span>` : ''}
                    </div>
                    ${debug?.slm_gut_vector ? `
                        <details class="gut-vector">
                            <summary>SLM Gut Vector</summary>
                            <div class="vector-grid">
                                <div>Valence: ${debug.slm_gut_vector.valence?.toFixed(2) || 'N/A'}</div>
                                <div>Arousal: ${debug.slm_gut_vector.arousal?.toFixed(2) || 'N/A'}</div>
                                <div>Stress: ${debug.slm_gut_vector.stress?.toFixed(2) || 'N/A'}</div>
                                <div>Warmth: ${debug.slm_gut_vector.warmth?.toFixed(2) || 'N/A'}</div>
                            </div>
                        </details>
                    ` : ''}
                `;
                div.appendChild(debugDiv);
            }
        } else {
            div.textContent = text;
        }
        this.elements.chatHistory.appendChild(div);
        this.scrollToBottom();
    },

    scrollToBottom() {
        setTimeout(() => {
            this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
        }, 50);
    },

    updateDashboard(data) {
        if (!data) return;

        // 1. Resonance (If present)
        if (data.Resonance_index !== undefined) {
            // ... legacy payload
        }

        // New Payload Structure from loop is { physio_state: {...}, timestamp: ... }
        // Or { state_snapshot: {...} } from orchestrator

        // Normalize src
        let physio = data.physio_state || (data.state_snapshot ? data.state_snapshot.physio_state : data);
        if (!physio || !physio.blood) return;

        const blood = physio.blood;

        // A. Update Core 5 Bars
        this.elements.coreBars.forEach(row => {
            const hID = row.dataset.id;
            const val = blood[hID] || 0.0;
            const prev = this.lastBlood[hID] || val;
            const delta = val - prev;
            const unit = this.HORMONE_UNITS[hID] || "";

            const barFill = row.querySelector('.bar-fill');
            const valText = row.querySelector('.value');
            const deltaSpan = row.querySelector('.delta');

            // Visualization scaling
            let pct = val;
            if (val > 100) pct = (val / 500) * 100;
            if (val > 1000) pct = (val / 5000) * 100;
            pct = Math.min(100, Math.max(0, pct));

            barFill.style.width = `${pct}%`;
            valText.innerHTML = `${val.toFixed(2)} <small>${unit}</small>`;

            if (deltaSpan) {
                const deltaStr = (delta >= 0 ? "+" : "") + delta.toFixed(3);
                deltaSpan.innerHTML = deltaStr;
                deltaSpan.className = 'delta ' + (delta >= 0 ? 'pos' : 'neg');
            }
        });

        // B. Update Ticker Grid (The Rest)
        this.renderTicker(blood);

        // C. Autonomic & Vitals
        if (physio.autonomic) {
            const ans = physio.autonomic;
            const sym = ans.sympathetic || 0.5;
            this.elements.barSym.style.width = `${sym * 100}%`;

            // Vitals from Backend
            const vitals = physio.vitals || {};
            const bpm = vitals.bpm || (60 + (sym * 40));
            const rpm = vitals.rpm || (12 + (sym * 8));

            this.elements.valHR.innerHTML = `${bpm.toFixed(1)} <small>BPM</small>`;
            this.elements.valRR.innerHTML = `${rpm.toFixed(1)} <small>RPM</small>`;

            const para = ans.parasympathetic || 0.5;
            if (sym > para + 0.2) this.elements.valANS.innerText = "Sympathetic";
            else if (para > sym + 0.2) this.elements.valANS.innerText = "Parasympathetic";
            else this.elements.valANS.innerText = "Balanced";
        }

        // Store this frame as last frame
        this.lastBlood = { ...blood };
    },

    renderTicker(blood) {
        if (!this.tickerCache) this.tickerCache = {};

        Object.keys(blood).forEach(hID => {
            if (this.CORE_IDS.includes(hID)) return; // Skip Core 5

            const val = blood[hID];
            const prev = this.lastBlood[hID] || val;
            const delta = val - prev;
            const unit = this.HORMONE_UNITS[hID] || "";

            // Get or Create Card
            let card = this.tickerCache[hID];
            if (!card) {
                card = document.createElement('div');
                card.className = 'ticker-compact-row'; // Use new compact class
                // Structure: Name | Value Unit | Delta
                card.innerHTML = `
                    <span class="t-name">${this.formatName(hID)}</span>
                    <span class="t-val">-- <span class="t-unit">${unit}</span></span>
                    <span class="t-delta">--</span>
                `;
                this.elements.tickerGrid.appendChild(card);
                this.tickerCache[hID] = card;
            }

            // Update Values
            const elVal = card.querySelector('.t-val');
            const elDelta = card.querySelector('.t-delta');

            // Format: 100 or 100.00 depending on magnitude
            const displayVal = val > 100 ? val.toFixed(0) : val.toFixed(2);
            elVal.innerHTML = `${displayVal} <span class="t-unit">${unit}</span>`;

            // Format delta
            const deltaStr = (delta >= 0 ? "+" : "") + delta.toFixed(3);
            elDelta.innerHTML = `${deltaStr}`;
            elDelta.className = 't-delta ' + (delta >= 0 ? 'pos' : 'neg');
        });
    },

    formatName(hid) {
        const parts = hid.split('_');
        if (parts.length > 2) return parts.slice(2).join(' ');
        return hid;
    },

    log(msg) {
        const div = document.createElement('div');
        div.className = 'log-line';
        const time = new Date().toLocaleTimeString().split(' ')[0];
        div.innerHTML = `<span>[${time}]</span> ${msg}`;
        this.elements.logs.appendChild(div);
        this.elements.logs.scrollTop = this.elements.logs.scrollHeight;
    },

    saveHistory(role, text) {
        this.state.history.push({ role, text });
        if (this.state.history.length > 50) this.state.history.shift();
        localStorage.setItem('eva_chat_history', JSON.stringify(this.state.history));
    },

    loadHistory() {
        const stored = localStorage.getItem('eva_chat_history');
        if (stored) {
            this.state.history = JSON.parse(stored);
            this.state.history.forEach(msg => {
                this.appendMessage(msg.role, msg.text);
            });
        }
        this.scrollToBottom();
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
