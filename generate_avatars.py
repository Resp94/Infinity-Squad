import base64
import re

def generate_svg(pixels, colors):
    svg_header = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 32" shape-rendering="crispEdges">'
    rects = []
    for y, row in enumerate(pixels):
        for x, color_idx in enumerate(row):
            if color_idx is not None:
                color = colors[color_idx]
                rects.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{color}"/>')
    return svg_header + "".join(rects) + '</svg>'

def to_data_uri(svg_content):
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')}"

def get_template():
    return [[None for _ in range(16)] for _ in range(32)]

def draw_chibi(p, skin_color, hair_color, clothes_color, eyes_color, hair_style="short", clothes_style="shirt"):
    for y in range(7, 15):
        for x in range(4, 12):
            p[y][x] = skin_color
    for x in range(4, 12): p[6][x] = hair_color
    if hair_style == "bun":
        for y in range(3, 6):
            for x in range(6, 10): p[y][x] = hair_color
    elif hair_style == "long":
        for y in range(7, 20):
            p[y][3] = p[y][12] = hair_color
    elif hair_style == "ponytail":
        for y in range(7, 15): p[y][12] = hair_color
        p[6][13] = p[7][13] = hair_color
    elif hair_style == "spiky":
        for x in range(4, 12, 2): p[5][x] = hair_color
    p[10][5] = p[10][10] = eyes_color
    p[11][5] = p[11][10] = eyes_color
    if clothes_style == "shirt":
        for y in range(16, 22):
            for x in range(5, 11): p[y][x] = clothes_color
        for y in range(16, 20): p[y][4] = p[y][11] = clothes_color
    elif clothes_style == "dress":
        for y in range(16, 25):
            for x in range(4, 12): p[y][x] = clothes_color
    for y in range(26, 29):
        p[y][6] = p[y][9] = skin_color
    p[29][5] = p[29][6] = p[29][9] = p[29][10] = '#111111'

def make_agent(name):
    p = get_template()
    if name == "mary":
        colors = {'S': '#FFE0BD', 'H': '#FFD700', 'C': '#FF69B4', 'E': '#0066FF'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "bun", "shirt")
    elif name == "john":
        colors = {'S': '#FFE0BD', 'H': '#442211', 'C': '#3366FF', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "short", "shirt")
    elif name == "paige":
        colors = {'S': '#FFE0BD', 'H': '#FF4500', 'C': '#99FF99', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "ponytail", "shirt")
    elif name == "sally":
        colors = {'S': '#FFE0BD', 'H': '#8A2BE2', 'C': '#FF99CC', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "long", "dress")
    elif name == "winston":
        colors = {'S': '#FFE0BD', 'H': '#708090', 'C': '#555555', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "short", "shirt")
    elif name == "amelia":
        colors = {'S': '#FFE0BD', 'H': '#0000FF', 'C': '#4444FF', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "short", "shirt")
    elif name == "quinn":
        colors = {'S': '#FFE0BD', 'H': '#00CC55', 'C': '#FFFFFF', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "short", "shirt")
    elif name == "bob":
        colors = {'S': '#FFE0BD', 'H': '#A52A2A', 'C': '#FF8800', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "spiky", "shirt")
    elif name == "barry":
        colors = {'S': '#FFE0BD', 'H': '#FFD700', 'C': '#EE3333', 'E': '#000000'}
        draw_chibi(p, 'S', 'H', 'C', 'E', "spiky", "shirt")

    return to_data_uri(generate_svg(p, {v: v for v in set(row for r in p for row in r if row is not None)}))

html_path = '_bmad-output/dashboard/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

css_lines = []
agents = ["mary", "john", "paige", "sally", "winston", "amelia", "quinn", "bob", "barry"]
for a in agents:
    css_lines.append(f"        .agent.{a} {{ background-image: url('{make_agent(a)}'); }}")

css_block = "\n".join(css_lines)

new_content = re.sub(
    r"\/\* Avatares Únicos \(SVG Chibi Style\) \*\/\n(        \.agent\.[a-z]+ \{[^\}]+\}\n)+",
    f"/* Avatares Únicos (GBA Pixel Art Style) */\n{css_block}\n",
    content
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("HTML updated with new Avatars.")
