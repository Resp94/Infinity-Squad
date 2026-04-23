import re

html_path = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

missing_css = """

        .agent-label {
            position: absolute;
            top: -20px;
            background-color: rgba(0, 0, 0, 0.85);
            color: #FFF;
            padding: 4px 10px;
            font-size: 7px;
            border-radius: 4px;
            white-space: nowrap;
            left: 50%;
            transform: translateX(-50%);
            border: 1px solid #00E676;
            box-shadow: 0 4px 0 rgba(0,0,0,0.3);
        }

        .status-bubble {
            position: absolute;
            top: -10px;
            right: -10px;
            font-size: 18px;
            filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.5));
            animation: float-icon 2s ease-in-out infinite;
        }

        @keyframes float-icon {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-5px) scale(1.1); }
        }

        /* ── HEADER ── */
        #header {
            position: absolute;
            top: 5px;
            right: 15px;
            font-size: 8px;
            color: #FFF;
            text-shadow: 2px 2px #000;
        }

        /* ── CHAT PANEL ── */
        #chat-panel {
            width: 260px;
            height: 480px;
            background-color: #0d0d1a;
            border: 4px solid #00E676;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 230, 118, 0.2);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-sizing: border-box;
        }

        #chat-header {
            background-color: #00E676;
            color: #000;
            font-size: 7px;
            padding: 8px 10px;
            text-align: center;
            letter-spacing: 1px;
            flex-shrink: 0;
        }

        #chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 10px 8px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            scrollbar-width: thin;
            scrollbar-color: #00E676 #0d0d1a;
            scroll-behavior: smooth;
        }

        #chat-messages::-webkit-scrollbar {
            width: 4px;
        }

        #chat-messages::-webkit-scrollbar-track {
            background: #0d0d1a;
        }

        #chat-messages::-webkit-scrollbar-thumb {
            background: #00E676;
            border-radius: 2px;
        }

        .chat-msg {
            display: flex;
            flex-direction: column;
            gap: 4px;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(6px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .chat-msg-header {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .chat-msg-avatar {
            width: 16px;
            height: 16px;
            border-radius: 2px;
            font-size: 9px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .chat-msg-name {
            font-size: 7px;
            color: #aaa;
        }

        .chat-msg-name.working {
            color: #00E676;
        }

        .chat-msg-name.waiting {
            color: #FFD600;
        }

        .chat-msg-name.done {
            color: #888;
        }

        .chat-msg-badge {
            font-size: 6px;
            padding: 2px 4px;
            border-radius: 2px;
            margin-left: auto;
        }

        .chat-msg-badge.working {
            background: #00E676;
            color: #000;
        }

        .chat-msg-badge.waiting {
            background: #FFD600;
            color: #000;
        }

        .chat-msg-badge.done {
            background: #444;
            color: #ccc;
        }

        .chat-msg-body {
            font-size: 7px;
            color: #ddd;
            line-height: 1.7;
            background-color: #1a1a2e;
            border-left: 3px solid #333;
            padding: 6px 8px;
            border-radius: 0 4px 4px 0;
            word-break: break-word;
        }

        .chat-msg-body.working {
            border-left-color: #00E676;
        }

        .chat-msg-body.working-bg {
            background-color: #001a0d;
        }

        .chat-msg-body.waiting {
            border-left-color: #FFD600;
        }

        .chat-msg-body.waiting-bg {
            background-color: #1a1700;
        }

        .chat-msg-time {
            font-size: 6px;
            color: #555;
            text-align: right;
        }

        #chat-status {
            background-color: #111;
            color: #555;
            font-size: 6px;
            padding: 6px 10px;
            text-align: center;
            border-top: 2px solid #222;
            flex-shrink: 0;
        }

        /* Connection indicator */
        #conn-indicator {
            position: absolute;
            top: 6px;
            left: 10px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #555;
            z-index: 200;
            transition: background 0.3s;
        }

        #conn-indicator.connected {
            background: #00E676;
            box-shadow: 0 0 6px #00E676;
        }

        #conn-indicator.disconnected {
            background: #FF1744;
            box-shadow: 0 0 6px #FF1744;
            animation: blink-red 1s infinite;
        }

        @keyframes blink-red {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
"""

content = content.replace("</style>", missing_css + "\n</style>")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
