import re

html_path = r'C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the generated CSS for barry with proper animation CSS
# First, let's remove the inline SVG for barry if it exists
content = re.sub(r"\.agent\.barry \{ background-image: url\('data:image/svg\+xml;base64,[^\)]+'\); \}", "", content)

# Now, we append the new CSS for the sprite sheet
new_css = """
        /* --- BARRY SPRITE ANIMATION --- */
        .agent.barry {
            background-image: url('assets/barry.png');
            background-size: cover; 
            width: 32px; 
            height: 32px;
            bottom: -5px;
            background-position: left center;
            image-rendering: pixelated;
        }
        
        .agent.barry.state-working {
            /* Assuming the sprite has 3 frames taking up 100% width.
               If background-size is cover, this won't work well for sprites.
               We need to use exact sizes or percentages. 
               The image is 1200x448. There are 3 frames.
               So each frame is 400x448.
               To fit in a 32x32 box, we set background-size to 300% 100% (or auto 100%). */
            background-size: 300% 100%;
            animation: walk-barry 0.6s steps(3) infinite;
        }
        
        @keyframes walk-barry {
            from { background-position: 0% 0; }
            to { background-position: 150% 0; } /* 3 frames. To move from frame 1 to frame 3 + 1, we move 100% * (frames / (frames-1))?
                                                   Wait, steps(3) divides the transition into 3 equal steps.
                                                   If size is 300% 100%, background-position: 100% 0 shows the rightmost edge.
                                                   Actually, standard way is background-size: cover is wrong.
                                                   Let's use exact widths.
                                                 */
        }
"""

# Let's fix the CSS string
new_css = """
        /* --- BARRY SPRITE ANIMATION --- */
        .agent.barry {
            background-image: url('assets/barry.png');
            background-size: 300% 100%; /* 3 frames */
            background-position: 0 0;
            width: 48px; /* Bigger to match aspect ratio of original image ~1:1 */
            height: 48px;
            bottom: 0px;
            image-rendering: pixelated;
            background-repeat: no-repeat;
        }
        
        .agent.barry.state-working {
            animation: walk-barry 0.8s steps(3) infinite;
        }
        
        @keyframes walk-barry {
            from { background-position: 0 0; }
            /* 100% shifts the background so its right edge touches the right edge of the container.
               Since size is 300%, 100% shifts it by exactly 2 frames. 
               Wait, steps(3) will make it jump to 0%, 50%, 100%.
               Let's test this. */
            to { background-position: 150% 0; } /* Actually, proper way with steps is to move by 3 frames, so 3 * 100%? No. */
        }
"""
# If there are 3 frames, the width is 3 * W. 
# Position 0 shows frame 1. Position -W shows frame 2. Position -2W shows frame 3.
# In percentages: 0% shows frame 1. 50% shows frame 2. 100% shows frame 3.
# So steps(3) to 150% would give 0%, 50%, 100% (frame 1, 2, 3).
# Wait, steps(3, end) evaluates at 0, 1/3, 2/3 of the transition if we animate from 0 to 100%?
# If we animate from 0% to 100% background-position:
# steps(3, end) means it will be at 0% (t=0..33%), 33% (t=33..66%), 66% (t=66..100%). That doesn't align with 0%, 50%, 100%.

# The most robust way is to just use explicit keyframes or pixel values, but percentage is easier if size is 300% 100%.
# For 3 frames, steps(3) requires moving exactly 1 sprite width (which is 100% of the image size)
# Actually, the standard way is:
# background-size: 300% 100%; 
# animation: walk 0.6s steps(3) infinite;
# @keyframes walk { 100% { background-position: right; } } -- wait, right is 100%.

# Let's just write the exact keyframes.
new_css = """
        /* --- BARRY SPRITE ANIMATION --- */
        .agent.barry {
            background-image: url('assets/barry.png');
            background-size: 300% 100%; 
            background-position: 0% 0;
            width: 48px;
            height: 48px;
            bottom: 0px;
            image-rendering: pixelated;
        }
        
        .agent.barry.state-working {
            animation: walk-barry 0.6s infinite step-end;
        }
        
        @keyframes walk-barry {
            0% { background-position: 0% 0; }
            33% { background-position: 50% 0; } /* Frame 2 */
            66% { background-position: 100% 0; } /* Frame 3 */
            100% { background-position: 0% 0; }
        }
"""

content = content.replace("/* Avatares Únicos (GBA Pixel Art Style) */", "/* Avatares Únicos (GBA Pixel Art Style) */\n" + new_css)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated CSS in HTML.")
