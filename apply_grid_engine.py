import re

html_path = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the chat panel CSS
chat_panel_css_match = re.search(r"(\s*/\* ── HEADER ── \*/.*?)</style>", content, re.DOTALL)
chat_panel_css = chat_panel_css_match.group(1) if chat_panel_css_match else ""

# Extract dialog box CSS
dialog_css_match = re.search(r"(\s*/\* ── DIALOG BOX \(GBA Style\) ── \*/.*?)\s*/\* ──", content, re.DOTALL)
dialog_css = dialog_css_match.group(1) if dialog_css_match else ""
if not dialog_css:
    dialog_css_match = re.search(r"(\s*/\* ── DIALOG BOX \(GBA Style\) ── \*/.*?)#squad-grid", content, re.DOTALL)
    dialog_css = dialog_css_match.group(1) if dialog_css_match else ""

html_start = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMAD Squad Dashboard - Pokemon Grid Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        :root {
            --gba-blue: #2255BB; --gba-light-blue: #4488FF; --gba-text-bg: #F8F8F8;
            --bg-color: #A0D080;
        }
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            font-family: 'Press Start 2P', cursive; background-color: #1a1a2e;
            display: flex; justify-content: center; align-items: center;
            overflow: hidden; image-rendering: pixelated;
        }
        #wrapper { display: flex; gap: 12px; align-items: stretch; }

        #game-container {
            width: 640px; height: 480px; background-color: var(--bg-color);
            position: relative; border: 8px solid #000;
            box-shadow: 0 0 30px rgba(0, 230, 118, 0.15); overflow: hidden; flex-shrink: 0;
        }

        #office-floor {
            width: 100%; height: 100%;
            background-image: url('assets/office-map.png');
            background-size: cover; background-position: center; background-repeat: no-repeat;
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1); transform-origin: center center;
            position: absolute; top: 0; left: 0; z-index: 1;
        }

        /* --- HARDCODED DESKS (PAs) --- */
        #squad-grid {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center center; z-index: 10;
        }

        .pa {
            position: absolute; width: 80px; height: 60px;
            background-image: url('assets/pa-desk.png'); background-size: contain;
            background-repeat: no-repeat; background-position: center bottom;
            transform: translate(-50%, -50%);
        }
        
        /* Map visually to the 9 cubicles in the map */
        #pa-mary { left: 22%; top: 35%; }
        #pa-john { left: 50%; top: 35%; }
        #pa-paige { left: 78%; top: 35%; }
        
        #pa-sally { left: 22%; top: 62%; }
        #pa-winston { left: 50%; top: 62%; }
        #pa-amelia { left: 78%; top: 62%; }
        
        #pa-quinn { left: 22%; top: 88%; }
        #pa-bob { left: 50%; top: 88%; }
        #pa-barry { left: 78%; top: 88%; }

        #boss-room {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1); transform-origin: center center;
            z-index: 5;
        }
        #pa-bmad-help {
            position: absolute; width: 120px; height: 80px;
            background-image: url('assets/boss-desk.png'); background-size: contain;
            background-repeat: no-repeat; background-position: center bottom;
            top: 15%; left: 50%; transform: translate(-50%, -50%); z-index: 10;
        }

        /* --- AGENTS LAYER --- */
        #agents-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 15;
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1); transform-origin: center center;
        }

        .agent {
            position: absolute; width: 48px; height: 48px;
            image-rendering: pixelated; background-color: transparent;
            background-repeat: no-repeat;
            margin-left: -24px; margin-top: -36px;
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
        
        .agent.state-working .status-bubble { content: '💻'; }

        /* WANDERING ANIMATIONS */
        .agent.walking {
            background-size: 300% 400%;
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
            background-size: 200% 100%;
            animation: sit-cycle 0.8s infinite step-end;
            background-position-y: 0%;
        }
        @keyframes sit-cycle {
            0% { background-position-x: 0%; }
            50% { background-position-x: 100%; }
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

html_end = """</style>
</head>
<body>
    <div id="wrapper">
        <div id="game-container">
            <div id="conn-indicator"></div>
            <div id="office-floor"></div>
            <div id="header">BMAD SQUAD - OFFICE</div>
            
            <div id="boss-room">
                <div id="pa-bmad-help" class="pa"></div>
            </div>

            <!-- Hardcoded Desks Layer -->
            <div id="squad-grid">
                <div id="pa-mary" class="pa"></div>
                <div id="pa-john" class="pa"></div>
                <div id="pa-paige" class="pa"></div>
                <div id="pa-sally" class="pa"></div>
                <div id="pa-winston" class="pa"></div>
                <div id="pa-amelia" class="pa"></div>
                <div id="pa-quinn" class="pa"></div>
                <div id="pa-bob" class="pa"></div>
                <div id="pa-barry" class="pa"></div>
            </div>

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
        const agentData = {}; 
        allAgents.forEach(a => {
            agentState[a.name.toLowerCase()] = 'idle';
            agentData[a.name.toLowerCase()] = { x: 0, y: 0, tx: 0, ty: 0 };
        });

        const layer = document.getElementById('agents-layer');
        const dialogText = document.getElementById('dialog-text');
        const chatMsgs = document.getElementById('chat-messages');
        const chatStatus = document.getElementById('chat-status');

        const TILE = 16;

        setTimeout(() => {
            allAgents.forEach(a => {
                const key = a.name.toLowerCase();
                const desk = document.getElementById(`pa-${key}`);
                
                const agentEl = document.createElement('div');
                agentEl.className = `agent ${key} walking face-down`;
                agentEl.id = `agent-${key}`;
                
                const label = document.createElement('div');
                label.className = 'agent-label'; label.innerText = `${a.name}`;
                
                const bubble = document.createElement('div');
                bubble.className = 'status-bubble'; bubble.innerText = a.icon;
                
                agentEl.appendChild(label); agentEl.appendChild(bubble);
                layer.appendChild(agentEl);
                
                if(desk) {
                    const rect = desk.getBoundingClientRect();
                    const containerRect = document.getElementById('game-container').getBoundingClientRect();
                    
                    let x = rect.left - containerRect.left + (rect.width/2);
                    let y = rect.top - containerRect.top + (rect.height/2);
                    
                    x = Math.round(x / TILE) * TILE;
                    y = Math.round(y / TILE) * TILE;
                    
                    agentData[key].baseX = x;
                    agentData[key].baseY = y;
                    
                    agentData[key].x = x;
                    agentData[key].y = y;
                    agentData[key].tx = x;
                    agentData[key].ty = y;
                    
                    renderPos(agentEl, x, y);
                }
            });
            
            setInterval(gameTick, 250);
        }, 500);

        function renderPos(el, x, y) {
            el.style.left = `${x}px`;
            el.style.top = `${y}px`;
            el.style.zIndex = Math.floor(y) + 15;
        }

        function gameTick() {
            allAgents.forEach(a => {
                const key = a.name.toLowerCase();
                const dat = agentData[key];
                const el = document.getElementById(`agent-${key}`);
                if(!el) return;

                const status = agentState[key];
                
                if (status === 'working' && dat.x === dat.baseX && dat.y === dat.baseY) {
                    return;
                }

                if (status !== 'working' && dat.x === dat.tx && dat.y === dat.ty) {
                    if (Math.random() < 0.2) {
                        if(key === 'bmad-help') {
                            dat.tx = Math.round((Math.random() * 200 + 220) / TILE) * TILE;
                            dat.ty = Math.round((Math.random() * 80 + 20) / TILE) * TILE;
                        } else {
                            dat.tx = Math.round((Math.random() * 500 + 50) / TILE) * TILE;
                            dat.ty = Math.round((Math.random() * 200 + 150) / TILE) * TILE;
                        }
                    } else {
                        el.classList.remove('walking');
                        return; 
                    }
                }

                if (status === 'working') {
                    dat.tx = dat.baseX;
                    dat.ty = dat.baseY;
                }

                let dx = 0; let dy = 0;
                
                if (dat.x !== dat.tx) {
                    dx = dat.x < dat.tx ? TILE : -TILE;
                } else if (dat.y !== dat.ty) {
                    dy = dat.y < dat.ty ? TILE : -TILE;
                }

                if (dx !== 0 || dy !== 0) {
                    dat.x += dx;
                    dat.y += dy;
                    
                    el.classList.add('walking');
                    el.classList.remove('face-up', 'face-down', 'face-left', 'face-right', 'sitting');
                    
                    if (dx > 0) el.classList.add('face-right');
                    else if (dx < 0) el.classList.add('face-left');
                    else if (dy > 0) el.classList.add('face-down');
                    else if (dy < 0) el.classList.add('face-up');
                    
                    renderPos(el, dat.x, dat.y);
                }

                if (status === 'working' && dat.x === dat.baseX && dat.y === dat.baseY) {
                    el.classList.remove('walking', 'face-up', 'face-down', 'face-left', 'face-right');
                    el.classList.add('sitting');
                    el.style.zIndex = Math.floor(dat.y) - 5; 
                }
            });
        }

        function setAgentState(agentName, status) {
            const key = agentName.toLowerCase();
            const el = document.getElementById(`agent-${key}`);
            if (!el) return;

            el.classList.remove('state-working', 'state-waiting', 'state-done');
            agentState[key] = (status === 'done') ? 'idle' : status;

            if (status === 'working') {
                el.classList.add('state-working');
                el.querySelector('.status-bubble').innerText = '💻';
            } else {
                if(status === 'waiting') el.classList.add('state-waiting');
                el.classList.remove('sitting');
                el.style.zIndex = Math.floor(agentData[key].y) + 15;
                el.querySelector('.status-bubble').innerText = agents.find(a => a.name.toLowerCase() === key)?.icon || '🤖';
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
            document.getElementById('squad-grid').style.transform = ''; 
            document.getElementById('office-floor').style.transform = ''; 
            document.getElementById('agents-layer').style.transform = '';
            document.getElementById('boss-room').style.transform = '';
        }
        function setCameraFocus(agentName) {
            const dat = agentData[agentName.toLowerCase()];
            if (!dat) return;
            if (cameraResetTimer) clearTimeout(cameraResetTimer);
            const moveX = (320 - dat.x) * 1.5;
            const moveY = (240 - dat.y) * 1.5;
            const t = `translate(${moveX}px, ${moveY}px) scale(2.5)`;
            document.getElementById('squad-grid').style.transform = t; 
            document.getElementById('office-floor').style.transform = t; 
            document.getElementById('agents-layer').style.transform = t;
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
            const lastWorking = entries.reverse().find(([, { status }]) => status === 'working');
            if (lastWorking) {
                const [name, { message }] = lastWorking;
                setCameraFocus(name);
                typeWriter(message ? `🟢 ${name}: "${message}"` : `🟢 ${name} está trabalhando!`);
            }
        });

    </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_start + dialog_css + chat_panel_css + html_end)

print("Grid Engine injected!")
