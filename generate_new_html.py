import re

html_path = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We will inject our new CSS and JS logic, but KEEP the chat panel, dialog box, connection styles intact.
# The safest way is to rebuild the HTML string using the parts we know.

html_start = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMAD Squad Dashboard - Wandering Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        :root {
            --gba-blue: #2255BB;
            --gba-light-blue: #4488FF;
            --gba-text-bg: #F8F8F8;
            --tile-size: 32px;
            --bg-color: #A0D080;
            --floor-color: #D0D0C0;
        }

        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            font-family: 'Press Start 2P', cursive;
            background-color: #1a1a2e;
            display: flex; justify-content: center; align-items: center;
            overflow: hidden; image-rendering: pixelated;
        }

        #wrapper { display: flex; gap: 12px; align-items: stretch; }

        #game-container {
            width: 640px; height: 480px;
            background-color: var(--bg-color);
            position: relative;
            border: 8px solid #000;
            box-shadow: 0 0 30px rgba(0, 230, 118, 0.15);
            overflow: hidden; flex-shrink: 0;
        }

        #office-floor {
            width: 100%; height: 100%;
            background-image: url('assets/office-map.png');
            background-size: cover; background-position: center; background-repeat: no-repeat;
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center center;
        }

        /* --- SQUAD GRID & DESKS --- */
        #squad-grid {
            position: absolute; top: 120px; left: 20px; right: 20px; bottom: 140px;
            display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(2, 1fr);
            gap: 40px 20px; transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center center; z-index: 10;
        }

        .pa {
            position: relative; display: flex; justify-content: center; align-items: center;
            background-image: url('assets/pa-desk.png'); background-size: contain;
            background-repeat: no-repeat; background-position: center bottom;
            width: 100%; height: 100%;
        }

        #boss-room {
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
            width: 150px; height: 100px; z-index: 10;
        }
        #pa-bmad-help {
            background-image: url('assets/boss-desk.png'); width: 100%; height: 100%;
            background-size: contain; background-repeat: no-repeat; background-position: center bottom;
            position: relative;
        }

        /* --- AGENTS LAYER --- */
        #agents-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 15; /* Rendered over floor, behind or over desks via JS Z-index */
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center center;
        }

        .agent {
            position: absolute; width: 48px; height: 48px;
            image-rendering: pixelated; background-color: transparent;
            background-repeat: no-repeat;
            transition: left 0.6s linear, top 0.6s linear;
            margin-left: -24px; margin-top: -36px; /* Center bottom anchor */
        }

        .agent-label {
            position: absolute; top: -15px; background-color: rgba(0, 0, 0, 0.85);
            color: #FFF; padding: 4px 10px; font-size: 7px; border-radius: 4px;
            white-space: nowrap; left: 50%; transform: translateX(-50%);
            border: 1px solid #00E676; box-shadow: 0 4px 0 rgba(0,0,0,0.3); z-index: 20;
        }
        .status-bubble {
            position: absolute; top: -5px; right: -10px; font-size: 18px;
            filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.5));
            animation: float-icon 2s ease-in-out infinite; z-index: 20;
        }
        @keyframes float-icon {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-5px) scale(1.1); }
        }

        /* AURA */
        .agent::before {
            content: ''; position: absolute; bottom: 0px; left: 8px; width: 32px; height: 12px;
            background: rgba(0, 0, 0, 0.2); border-radius: 50%; z-index: -1; transition: all 0.3s;
        }
        .agent.state-working::before {
            background: rgba(0, 230, 118, 0.6); box-shadow: 0 0 15px 5px rgba(0, 230, 118, 0.5);
            animation: pulse-aura-green 1.2s ease-in-out infinite;
        }
        .agent.state-waiting::before {
            background: rgba(255, 214, 0, 0.6); box-shadow: 0 0 15px 5px rgba(255, 214, 0, 0.5);
            animation: pulse-aura-yellow 1.4s ease-in-out infinite;
        }
        @keyframes pulse-aura-green { 0%, 100% { transform: scale(1); opacity: 0.6; } 50% { transform: scale(1.3); opacity: 0.9; } }
        @keyframes pulse-aura-yellow { 0%, 100% { transform: scale(1); opacity: 0.6; } 50% { transform: scale(1.3); opacity: 0.9; } }

        /* WANDERING ANIMATIONS */
        .agent.walking {
            background-size: 300% 400%; /* 3 cols, 4 rows */
            animation: walk-cycle 0.6s infinite step-end;
        }
        .agent.face-down { background-position-y: 0%; }
        .agent.face-left { background-position-y: 33.33%; }
        .agent.face-right { background-position-y: 66.66%; }
        .agent.face-up { background-position-y: 100%; }

        @keyframes walk-cycle {
            0% { background-position-x: 0%; }
            33% { background-position-x: 50%; }
            66% { background-position-x: 100%; }
            100% { background-position-x: 0%; }
        }

        /* SITTING ANIMATIONS */
        .agent.sitting {
            background-size: 300% 100%;
            animation: sit-cycle 0.8s infinite step-end;
            background-position-y: 0%;
        }
        @keyframes sit-cycle {
            0% { background-position-x: 0%; }
            50% { background-position-x: 50%; }
            100% { background-position-x: 0%; }
        }

        /* AGENT ASSETS */
        .agent.barry.walking { background-image: url('assets/barry-walk.png'); }
        .agent.barry.sitting { background-image: url('assets/barry-sit.png'); }
        .agent.mary.walking { background-image: url('assets/mary-walk.png'); }
        .agent.mary.sitting { background-image: url('assets/mary-sit.png'); }
        .agent.john.walking { background-image: url('assets/john-walk.png'); }
        .agent.john.sitting { background-image: url('assets/john-sit.png'); }
        .agent.paige.walking { background-image: url('assets/paige-walk.png'); }
        .agent.paige.sitting { background-image: url('assets/paige-sit.png'); }
        .agent.sally.walking { background-image: url('assets/sally-walk.png'); }
        .agent.sally.sitting { background-image: url('assets/sally-sit.png'); }
        .agent.winston.walking { background-image: url('assets/winston-walk.png'); }
        .agent.winston.sitting { background-image: url('assets/winston-sit.png'); }
        .agent.amelia.walking { background-image: url('assets/amelia-walk.png'); }
        .agent.amelia.sitting { background-image: url('assets/amelia-sit.png'); }
        .agent.quinn.walking { background-image: url('assets/quinn-walk.png'); }
        .agent.quinn.sitting { background-image: url('assets/quinn-sit.png'); }
        .agent.bob.walking { background-image: url('assets/bob-walk.png'); }
        .agent.bob.sitting { background-image: url('assets/bob-sit.png'); }
        .agent.bmad-help.walking { background-image: url('assets/boss-walk.png'); }
        .agent.bmad-help.sitting { background-image: url('assets/boss-sit.png'); }
"""

dialog_match = re.search(r"(\s*/\* ── DIALOG BOX \(GBA Style\) ── \*/.*?)\s*/\* ── SQUAD GRID ── \*/", content, re.DOTALL)
dialog_css = dialog_match.group(1) if dialog_match else ""

chat_match = re.search(r"(\s*/\* ── HEADER ── \*/.*?)</style>", content, re.DOTALL)
chat_panel_css = chat_match.group(1) if chat_match else ""

html_end = """</style>
</head>
<body>
    <div id="wrapper">
        <div id="game-container">
            <div id="conn-indicator"></div>
            <div id="office-floor"></div>
            <div id="header">BMAD SQUAD - ROOM 01</div>
            
            <div id="boss-room">
                <div id="pa-bmad-help" class="pa"></div>
            </div>

            <div id="squad-grid"></div>
            <div id="agents-layer"></div>

            <div id="dialog-box">
                <p id="dialog-text">O squad BMAD está online! Pronto para iniciar o próximo projeto...</p>
                <div id="next-arrow"></div>
            </div>
        </div>

        <div id="chat-panel">
            <div id="chat-header">▶ SQUAD COMMS</div>
            <div id="chat-messages"></div>
            <div id="chat-status">AGUARDANDO ATIVIDADE...</div>
        </div>
    </div>

    <script src="/socket.io/socket.io.js"></script>
    <script>
        const socket = io({ reconnection: true, reconnectionDelay: 1000 });
        const connIndicator = document.getElementById('conn-indicator');
        socket.on('connect', () => connIndicator.className = 'connected');
        socket.on('disconnect', () => connIndicator.className = 'disconnected');

        const agents = [
            { name: "Mary", role: "Analyst", icon: "📊" },
            { name: "John", role: "PM", icon: "📋" },
            { name: "Paige", role: "Writer", icon: "📚" },
            { name: "Sally", role: "Designer", icon: "🎨" },
            { name: "Winston", role: "Architect", icon: "🏗️" },
            { name: "Amelia", role: "Dev", icon: "💻" },
            { name: "Quinn", role: "QA", icon: "🧪" },
            { name: "Bob", role: "SM", icon: "🏃" },
            { name: "Barry", role: "Quick Dev", icon: "🚀" }
        ];
        
        const boss = { name: "BMAD-Help", role: "System", icon: "🤖" };
        const allAgents = [...agents, boss];

        const agentState = {};
        allAgents.forEach(a => agentState[a.name.toLowerCase()] = 'idle');

        const grid = document.getElementById('squad-grid');
        const layer = document.getElementById('agents-layer');
        const floor = document.getElementById('office-floor');
        const dialogText = document.getElementById('dialog-text');
        const chatMsgs = document.getElementById('chat-messages');
        const chatStatus = document.getElementById('chat-status');

        // Render Desks
        agents.forEach(a => {
            const pa = document.createElement('div');
            pa.className = 'pa';
            pa.id = `desk-${a.name.toLowerCase()}`;
            grid.appendChild(pa);
        });

        // Render Avatars
        setTimeout(() => {
            allAgents.forEach(a => {
                const key = a.name.toLowerCase();
                const desk = document.getElementById(`desk-${key}`) || document.getElementById(`pa-${key}`);
                
                const agentEl = document.createElement('div');
                agentEl.className = `agent ${key} walking face-down`;
                agentEl.id = `agent-${key}`;
                
                const label = document.createElement('div');
                label.className = 'agent-label'; label.innerText = `${a.name}`;
                
                const bubble = document.createElement('div');
                bubble.className = 'status-bubble'; bubble.innerText = a.icon;
                
                agentEl.appendChild(label); agentEl.appendChild(bubble);
                layer.appendChild(agentEl);
                
                // Set initial position
                if(desk) {
                    const rect = desk.getBoundingClientRect();
                    const containerRect = document.getElementById('game-container').getBoundingClientRect();
                    const x = rect.left - containerRect.left + (rect.width/2);
                    const y = rect.top - containerRect.top + (rect.height/2);
                    agentEl.dataset.baseX = x;
                    agentEl.dataset.baseY = y;
                    agentEl.style.left = `${x}px`;
                    agentEl.style.top = `${y}px`;
                    agentEl.style.zIndex = Math.floor(y);
                }
            });
            
            // Start Wandering Engine
            setInterval(wanderEngine, 2000);
        }, 500);

        function wanderEngine() {
            allAgents.forEach(a => {
                const key = a.name.toLowerCase();
                const el = document.getElementById(`agent-${key}`);
                if(!el || agentState[key] === 'working' || agentState[key] === 'waiting') return;
                
                // Random wander
                const rx = Math.random() * 500 + 50;
                let ry = Math.random() * 200 + 150; // Keep in middle area
                
                if(key === 'bmad-help') {
                    // Boss stays in boss room
                    ry = Math.random() * 50 + 50;
                }
                
                moveTo(el, rx, ry);
            });
        }

        function moveTo(el, tgtX, tgtY) {
            const curX = parseFloat(el.style.left || 0);
            const curY = parseFloat(el.style.top || 0);
            
            el.classList.remove('face-up', 'face-down', 'face-left', 'face-right');
            if(Math.abs(tgtX - curX) > Math.abs(tgtY - curY)) {
                el.classList.add(tgtX > curX ? 'face-right' : 'face-left');
            } else {
                el.classList.add(tgtY > curY ? 'face-down' : 'face-up');
            }
            
            el.style.left = `${tgtX}px`;
            el.style.top = `${tgtY}px`;
            el.style.zIndex = Math.floor(tgtY) + 20; // Walking agents are above desks
        }

        function setAgentState(agentName, status) {
            const key = agentName.toLowerCase();
            const el = document.getElementById(`agent-${key}`);
            if (!el) return;

            el.classList.remove('state-working', 'state-waiting', 'state-done');
            agentState[key] = (status === 'done') ? 'idle' : status;

            if (status === 'working') {
                el.classList.add('state-working');
                // Return to desk
                const bx = el.dataset.baseX;
                const by = el.dataset.baseY;
                moveTo(el, bx, by);
                // After reaching desk, sit down
                setTimeout(() => {
                    if(agentState[key] === 'working') {
                        el.classList.remove('walking', 'face-up', 'face-down', 'face-left', 'face-right');
                        el.classList.add('sitting');
                        el.style.zIndex = Math.floor(by) - 10; // Behind desk
                        
                        // Force face-down strictly for sitting so we look front
                        el.style.backgroundPositionY = "0%";
                    }
                }, 600);
            } else {
                if(status === 'waiting') el.classList.add('state-waiting');
                el.classList.remove('sitting');
                el.classList.add('walking');
            }
        }

        /* ── UI EXTRAS ── */
        let isTyping = false; let typeQueue = [];
        function typeWriter(text) {
            if (isTyping) { typeQueue.push(text); return; }
            isTyping = true; dialogText.innerText = ''; let i = 0;
            function nextChar() {
                if (i < text.length) { dialogText.innerText += text[i++]; setTimeout(nextChar, 28); }
                else { isTyping = false; if (typeQueue.length > 0) setTimeout(() => typeWriter(typeQueue.shift()), 900); }
            }
            nextChar();
        }

        function now() { const d = new Date(); return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`; }

        function addChatMessage(agentName, status, message) {
            const info = allAgents.find(a => a.name.toLowerCase() === agentName.toLowerCase()) || { icon: '🤖', role: '?' };
            const msg = document.createElement('div'); msg.className = 'chat-msg';
            const bgClass = status === 'working' ? 'working-bg' : status === 'waiting' ? 'waiting-bg' : '';
            msg.innerHTML = `<div class="chat-msg-header"><div class="chat-msg-avatar">${info.icon}</div><span class="chat-msg-name ${status}">${agentName}</span><span class="chat-msg-badge ${status}">${status}</span></div>${message ? `<div class="chat-msg-body ${status} ${bgClass}">${message}</div>` : ''}<div class="chat-msg-time">${now()}</div>`;
            chatMsgs.appendChild(msg); chatMsgs.scrollTo({ top: chatMsgs.scrollHeight, behavior: 'smooth' });
            
            const active = Object.entries(agentState).filter(([, s]) => s === 'working').length;
            const waiting = Object.entries(agentState).filter(([, s]) => s === 'waiting').length;
            chatStatus.textContent = active > 0 ? `${active} AGENTE(S) ATIVO(S) | ${waiting} AGUARDANDO` : waiting > 0 ? `${waiting} AGENTE(S) AGUARDANDO` : 'SQUAD EM PRONTIDÃO';
        }

        let cameraResetTimer = null;
        function resetCamera() {
            if (cameraResetTimer) clearTimeout(cameraResetTimer);
            grid.style.transform = ''; floor.style.transform = ''; layer.style.transform = '';
            document.getElementById('boss-room').style.transform = '';
        }
        function setCameraFocus(agentName) {
            const el = document.getElementById(`agent-${agentName.toLowerCase()}`);
            if (!el) return;
            if (cameraResetTimer) clearTimeout(cameraResetTimer);
            const moveX = (320 - parseFloat(el.style.left || 0)) * 1.5;
            const moveY = (240 - parseFloat(el.style.top || 0)) * 1.5;
            const t = `translate(${moveX}px, ${moveY}px) scale(2.5)`;
            grid.style.transform = t; floor.style.transform = t; layer.style.transform = t;
            document.getElementById('boss-room').style.transform = t;
            cameraResetTimer = setTimeout(resetCamera, 7000);
        }

        socket.on('agent-activity', (data) => {
            const { agent, status, message } = data;
            setAgentState(agent, status);
            if (status === 'working') setCameraFocus(agent); else if (status === 'done') resetCamera();
            if (message) typeWriter(`🟢 ${agent}: "${message}"`);
            addChatMessage(agent, status, message);
        });

        socket.on('status', (data) => {
            typeWriter(`🤖 SYSTEM: ${data.message}`);
            setAgentState('bmad-help', 'working');
            setCameraFocus('bmad-help');
            addChatMessage('BMAD-Help', 'working', data.message);
            setTimeout(() => setAgentState('bmad-help', 'idle'), 4000);
        });
        
        socket.on('state-sync', (states) => {
            const entries = Object.entries(states);
            entries.forEach(([agentName, { status, message }]) => {
                setAgentState(agentName, status);
                addChatMessage(agentName, status, message);
            });
            // Foca câmera no último agente working
            const lastWorking = entries.reverse().find(([, { status }]) => status === 'working');
            if (lastWorking) {
                const [name, { message }] = lastWorking;
                setCameraFocus(name);
                const statusEmoji = '🟢';
                typeWriter(message ? `${statusEmoji} ${name}: "${message}"` : `${statusEmoji} ${name} está trabalhando!`);
            } else {
                const lastAny = entries.find(([, { status }]) => status === 'waiting');
                if (lastAny) {
                    const [name, { message }] = lastAny;
                    typeWriter(message ? `🟡 ${name}: "${message}"` : `🟡 ${name} aguarda sua instrução.`);
                }
            }
        });

    </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_start + dialog_css + chat_panel_css + html_end)

print("Done")
