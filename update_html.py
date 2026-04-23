import re
import os

html_path = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_css = """        /* Avatares Únicos (GBA Pixel Art Style) */

        /* ── MESA (PA) ── */
        .pa {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 4px;
            background-image: url('assets/PA.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center bottom;
            z-index: 1;
        }

        /* ── AGENTE BASE ── */
        .agent {
            position: absolute;
            background-size: 300% 100%; 
            background-position: 0% 0;
            width: 48px;
            height: 48px;
            bottom: 0px;
            image-rendering: pixelated;
            background-color: transparent;
            z-index: 10;
        }

        .agent-label {
            top: -15px; /* Adjust label for 48px height */
            z-index: 20;
        }
        
        .status-bubble {
            top: -5px; /* Adjust bubble for 48px height */
            z-index: 20;
        }

        /* ANIMATION FOR ALL SPRITES */
        .agent.state-working {
            animation: walk-sprite 0.6s infinite step-end;
        }
        
        @keyframes walk-sprite {
            0% { background-position: 0% 0; }
            33% { background-position: 50% 0; } /* Frame 2 */
            66% { background-position: 100% 0; } /* Frame 3 */
            100% { background-position: 0% 0; }
        }

        /* INDIVIDUAL BACKGROUNDS */
        .agent.barry { background-image: url('assets/barry.png'); }
        .agent.mary { background-image: url('assets/mary.png'); }
        .agent.john { background-image: url('assets/John.png'); }
        .agent.paige { background-image: url('assets/paige.png'); }
        .agent.sally { background-image: url('assets/Sally.png'); }
        .agent.winston { background-image: url('assets/Winston.png'); }
        .agent.amelia { background-image: url('assets/Amelia.png'); }
        .agent.quinn { background-image: url('assets/Quin.png'); }
        .agent.bob { background-image: url('assets/Bob.png'); }
"""

# Find where "Avatares Únicos" starts and replace until "</style>"
pattern = re.compile(r"/\* Avatares Únicos \(GBA Pixel Art Style\) \*/.*?(?=</style>)", re.DOTALL)
content = re.sub(pattern, new_css, content)

# Update the floor background
# We look for #office-floor css
floor_pattern = re.compile(r"#office-floor \{.*?\}", re.DOTALL)
new_floor_css = """#office-floor {
            width: 100%;
            height: 100%;
            background-image: url('assets/Futuristic_office_room_202604062222.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center center;
        }"""
content = re.sub(floor_pattern, new_floor_css, content)


with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML and CSS successfully updated!")
