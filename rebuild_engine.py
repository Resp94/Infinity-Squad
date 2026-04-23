import re

html_path = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_updates = """
        /* ── CAMADA DE AGENTES ── */
        #agents-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        }

        .agent {
            position: absolute; width: 64px; height: 64px;
            image-rendering: pixelated; background-color: transparent;
            background-repeat: no-repeat;
            margin-left: -32px; margin-top: -48px;
            /* Transition exactly matches the tile size and time for stepping */
            transition: left 0.4s linear, top 0.4s linear;
        }

        /* Classes de Direção (Eixo Y) */
        .agent.face-down { background-position-y: 0%; }
        .agent.face-left { background-position-y: 33.33%; }
        .agent.face-right { background-position-y: 66.66%; }
        .agent.face-up { background-position-y: 100%; }

        /* Animação de Caminhada (Eixo X - 5 Colunas) */
        .agent.walking {
            background-size: 500% 400%;
            animation: walk-cycle 0.4s infinite step-end;
        }

        @keyframes walk-cycle {
            0% { background-position-x: 0%; }
            25% { background-position-x: 25%; }
            50% { background-position-x: 50%; }
            75% { background-position-x: 75%; }
            100% { background-position-x: 100%; }
        }

        /* Estado Sentado/Trabalhando */
        .agent.sitting {
            background-size: 200% 100%;
            animation: sit-cycle 0.6s infinite step-end;
            background-position-y: 0 !important;
        }
"""
content = re.sub(r"/\* ── CAMADA DE AGENTES ── \*/.*?@keyframes sit-cycle \{.*?\n        \}", css_updates, content, flags=re.DOTALL)


# 2. Update Script
new_script = """
    <script src="/socket.io/socket.io.js"></script>
    <script>
        const socket = io({
            reconnection: true,
            reconnectionAttempts: Infinity,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            transports: ['websocket', 'polling']
        });
        
        // --- ENGINE CONFIG ---
        const TILE_SIZE = 40; // 800x600 -> 20x15 grid
        const GRID_COLS = 20;
        const GRID_ROWS = 15;
        const collisionGrid = Array(GRID_ROWS).fill().map(() => Array(GRID_COLS).fill(0));

        // Bordas
        for(let x=0; x<GRID_COLS; x++) { collisionGrid[0][x] = 1; collisionGrid[GRID_ROWS-1][x] = 1; }
        for(let y=0; y<GRID_ROWS; y++) { collisionGrid[y][0] = 1; collisionGrid[y][GRID_COLS-1] = 1; }
        
        // Mesas / Obstáculos (Mapeamento aproximado do Escritorio.png)
        // 9 baias
        const desks = [
            { id: 'mary', r: 4, c: 3 },
            { id: 'john', r: 4, c: 9 },
            { id: 'paige', r: 4, c: 15 },
            { id: 'sally', r: 9, c: 3 },
            { id: 'winston', r: 9, c: 9 },
            { id: 'amelia', r: 9, c: 15 },
            { id: 'quinn', r: 13, c: 3 },
            { id: 'bob', r: 13, c: 9 },
            { id: 'barry', r: 13, c: 15 }
        ];

        // Bloqueia as posições das mesas no grid para ngm atravessar (exceto o dono sentando)
        desks.forEach(d => { collisionGrid[d.r][d.c] = 1; collisionGrid[d.r-1][d.c] = 1; }); // Mesa ocupa 2 tiles verticais na arte

        const agentsData = [
            { id: 'mary', name: "Mary", role: "Analyst", sit: 'mary (1).png', walk: 'Mary - caminhando (1).png', desk: desks[0] },
            { id: 'john', name: "John", role: "PM", sit: 'John (1).png', walk: 'John - caminhando (1).png', desk: desks[1] },
            { id: 'paige', name: "Paige", role: "Writer", sit: 'Paige (1).png', walk: 'Paige - caminhando (1).png', desk: desks[2] },
            { id: 'sally', name: "Sally", role: "Designer", sit: 'Sally (1).png', walk: 'Sally - caminhando (1).png', desk: desks[3] },
            { id: 'winston', name: "Winston", role: "Architect", sit: 'Winston (1).png', walk: 'Winston - caminhando (1).png', desk: desks[4] },
            { id: 'amelia', name: "Amelia", role: "Dev", sit: 'mary (1).png', walk: 'Mary - caminhando (1).png', desk: desks[5] },
            { id: 'quinn', name: "Quinn", role: "QA", sit: 'Quin (1).png', walk: 'Quin - caminhando (1).png', desk: desks[6] },
            { id: 'bob', name: "Bob", role: "SM", sit: 'Bob (1).png', walk: 'Bob-caminhando (1).png', desk: desks[7] },
            { id: 'barry', name: "Barry", role: "Quick Dev", sit: 'Boos (1).png', walk: 'Boos-caminhando (1).png', desk: desks[8] }
        ];

        const agentElements = {};

        // --- PATHFINDING A* ---
        function findPath(start, end) {
            const openList = [{r: start.r, c: start.c, g: 0, h: Math.abs(start.r-end.r)+Math.abs(start.c-end.c), p: null}];
            const closedList = new Set();
            
            while(openList.length > 0) {
                let current = openList.sort((a,b) => (a.g+a.h) - (b.g+b.h))[0];
                if(current.r === end.r && current.c === end.c) {
                    const path = [];
                    while(current.p) { path.push({r: current.r, c: current.c}); current = current.p; }
                    return path.reverse();
                }
                openList.splice(openList.indexOf(current), 1);
                closedList.add(`${current.r},${current.c}`);
                
                // ORTHOGONAL ONLY (Top-Down RPG)
                [[0,1],[0,-1],[1,0],[-1,0]].forEach(([dr, dc]) => {
                    const nr = current.r + dr, nc = current.c + dc;
                    if(nr>=0 && nr<GRID_ROWS && nc>=0 && nc<GRID_COLS && collisionGrid[nr][nc] === 0 && !closedList.has(`${nr},${nc}`)) {
                        const g = current.g + 1;
                        const existing = openList.find(o => o.r === nr && o.c === nc);
                        if(!existing || g < existing.g) {
                            if(existing) openList.splice(openList.indexOf(existing), 1);
                            openList.push({r: nr, c: nc, g, h: Math.abs(nr-end.r)+Math.abs(nc-end.c), p: current});
                        }
                    }
                });
            }
            return null; // Sem caminho
        }

        // --- RENDERING ---
        function renderScene() {
            const objectsLayer = document.getElementById('objects-layer');
            const agentsLayer = document.getElementById('agents-layer');
            
            agentsData.forEach(a => {
                // Instanciar Mesas
                const desk = document.createElement('div');
                desk.className = 'pa-desk';
                desk.style.left = (a.desk.c * TILE_SIZE + TILE_SIZE/2) + 'px';
                desk.style.top = ((a.desk.r-1) * TILE_SIZE + TILE_SIZE/2) + 'px'; // Ajuste visual da mesa
                objectsLayer.appendChild(desk);

                // Instanciar Agentes num tile livre aleatório
                let startR, startC;
                do {
                    startR = Math.floor(Math.random()*(GRID_ROWS-2))+1;
                    startC = Math.floor(Math.random()*(GRID_COLS-2))+1;
                } while(collisionGrid[startR][startC] === 1);

                const el = document.createElement('div');
                el.className = 'agent walking face-down';
                el.style.backgroundImage = `url('assets/${a.walk}')`;
                el.innerHTML = `<div class="agent-label">${a.name}</div><div class="status-bubble">💤</div>`;
                agentsLayer.appendChild(el);
                
                agentElements[a.id] = { 
                    el, data: a, status: 'idle', 
                    gridPos: {r: startR, c: startC},
                    path: [] 
                };
                updateElementPos(a.id);
            });
        }

        function updateElementPos(id) {
            const a = agentElements[id];
            // PIXEL PERFECT MOVEMENT
            a.el.style.left = (a.gridPos.c * TILE_SIZE + TILE_SIZE/2) + 'px';
            a.el.style.top = (a.gridPos.r * TILE_SIZE + TILE_SIZE/2) + 'px';
            // Y-SORTING (Depth)
            if(a.status === 'working' && a.gridPos.r === a.data.desk.r && a.gridPos.c === a.data.desk.c) {
                a.el.style.zIndex = a.gridPos.r - 1; // Senta atrás da mesa
            } else {
                a.el.style.zIndex = a.gridPos.r + 10; // Fica na frente das mesas acima dele
            }
        }

        // --- GAME LOOP ---
        function gameTick() {
            Object.keys(agentElements).forEach(id => {
                const a = agentElements[id];
                
                // WORKING: Precisa ir para a mesa
                if(a.status === 'working' && (a.gridPos.r !== a.data.desk.r || a.gridPos.c !== a.data.desk.c)) {
                    if(a.path.length === 0) {
                        // Desbloqueia a própria mesa temporariamente para calcular a rota final
                        collisionGrid[a.data.desk.r][a.data.desk.c] = 0;
                        let newPath = findPath(a.gridPos, a.data.desk);
                        if(newPath) a.path = newPath;
                        collisionGrid[a.data.desk.r][a.data.desk.c] = 1;
                    }
                }

                // IDLE: Passear aleatoriamente
                if(a.status === 'idle' && a.path.length === 0 && Math.random() > 0.8) {
                    const targets = [[0,1],[0,-1],[1,0],[-1,0]].map(([dr, dc]) => ({r: a.gridPos.r+dr, c: a.gridPos.c+dc}))
                        .filter(t => t.r>=0 && t.r<GRID_ROWS && t.c>=0 && t.c<GRID_COLS && collisionGrid[t.r][t.c] === 0);
                    
                    // Checa se o tile alvo não está ocupado por outro agente
                    const validTargets = targets.filter(t => !Object.values(agentElements).some(other => other.gridPos.r === t.r && other.gridPos.c === t.c));
                    
                    if(validTargets.length > 0) {
                        a.path = [validTargets[Math.floor(Math.random()*validTargets.length)]];
                    }
                }

                // MOVER
                if(a.path.length > 0) {
                    const next = a.path.shift();
                    
                    // Verifica se o próximo tile não foi ocupado subitamente por outro agente vagando
                    const occupiedByOther = Object.values(agentElements).find(other => other.id !== a.id && other.gridPos.r === next.r && other.gridPos.c === next.c);
                    if(occupiedByOther) {
                        // Bateu em alguém! Para o movimento e espera o próximo tick.
                        a.path.unshift(next);
                        a.el.classList.remove('walking');
                        return;
                    }

                    // Direção
                    a.el.classList.remove('face-up', 'face-down', 'face-left', 'face-right', 'sitting');
                    if(next.c > a.gridPos.c) a.el.classList.add('face-right');
                    else if(next.c < a.gridPos.c) a.el.classList.add('face-left');
                    else if(next.r > a.gridPos.r) a.el.classList.add('face-down');
                    else if(next.r < a.gridPos.r) a.el.classList.add('face-up');

                    a.gridPos = next;
                    updateElementPos(id);
                    a.el.classList.add('walking'); // Garante que está animando as pernas

                    // Chegou na mesa?
                    if(a.status === 'working' && a.gridPos.r === a.data.desk.r && a.gridPos.c === a.data.desk.c) {
                        a.el.classList.remove('walking', 'face-up', 'face-left', 'face-right');
                        a.el.classList.add('sitting', 'face-down'); // Senta virado pra frente
                        a.el.style.backgroundImage = `url('assets/${a.data.sit}')`;
                        updateElementPos(id); // Força Y-Sort
                    }
                } else {
                    // Parado
                    if (a.status === 'idle') {
                        a.el.classList.remove('walking'); // Para as perninhas se não tem rota
                    }
                }
            });
        }

        // --- TYPEWRITER & CHAT (Mantendo a UI) ---
        const dialogText = document.getElementById('dialog-text');
        const chatMsgs = document.getElementById('chat-messages');
        let isTyping = false;
        let typeQueue = [];

        function typeWriter(text) {
            if (isTyping) { typeQueue.push(text); return; }
            isTyping = true; dialogText.innerText = ''; let i = 0;
            function nextChar() {
                if (i < text.length) { dialogText.innerText += text[i++]; setTimeout(nextChar, 25); }
                else { isTyping = false; if (typeQueue.length > 0) setTimeout(() => typeWriter(typeQueue.shift()), 800); }
            }
            nextChar();
        }

        // --- EVENTS ---
        socket.on('agent-activity', (data) => {
            const id = data.agent.toLowerCase();
            const a = agentElements[id];
            if(!a) return;

            if(data.status === 'working') {
                a.status = 'working';
                a.el.querySelector('.status-bubble').innerText = '💻';
                a.el.style.backgroundImage = `url('assets/${a.data.walk}')`; // Prepara pra andar
                a.path = []; // Recalcula
            } else {
                a.status = 'idle';
                a.el.classList.remove('sitting');
                a.el.classList.add('walking', 'face-down');
                a.el.style.backgroundImage = `url('assets/${a.data.walk}')`;
                a.el.querySelector('.status-bubble').innerText = '💤';
                // Move um tile pra baixo pra sair da mesa
                if(collisionGrid[a.gridPos.r+1][a.gridPos.c] === 0) {
                    a.path = [{r: a.gridPos.r+1, c: a.gridPos.c}];
                }
            }
            
            const msg = document.createElement('div');
            msg.className = `chat-msg ${data.status}`;
            msg.innerHTML = `<span class="chat-msg-name">${data.agent}</span>${data.message || (data.status === 'working' ? 'Indo para a mesa...' : 'Ocioso.')}`;
            chatMsgs.appendChild(msg);
            chatMsgs.scrollTo(0, 9999);
            
            typeWriter(`${data.agent}: "${data.message || (data.status === 'working' ? 'Estou focado!' : 'Terminei!')}"`);
        });

        renderScene();
        // O intervalo deve bater com o transition-duration do CSS (0.4s)
        setInterval(gameTick, 400);
    </script>
"""
content = re.sub(r"<script src=\"/socket\.io/socket\.io\.js\"></script>.*?</script>", new_script, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
