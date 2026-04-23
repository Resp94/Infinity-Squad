import os
from PIL import Image

assets_dir = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\assets"

def process_all_sprites():
    agents = ["amelia", "barry", "bob", "boss", "john", "mary", "paige", "quinn", "sally", "winston"]
    
    for agent in agents:
        # Walk sheet: originally 4 rows, 5 cols. Convert to 4 rows, 3 cols.
        walk_name = f"{agent}-walk.png"
        walk_path = os.path.join(assets_dir, walk_name)
        if os.path.exists(walk_path):
            img = Image.open(walk_path).convert("RGBA")
            width, height = img.size
            cell_w = width // 5 
            cell_h = height // 4 
            
            frames = []
            for row in range(4):
                # Take only first 3 cols to form standard RPG walking cycle
                for col in range(3):
                    box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
                    frame = img.crop(box)
                    bbox = frame.getbbox()
                    if bbox: frames.append(frame.crop(bbox))
                    else: frames.append(frame)
            
            if frames:
                # Find exactly the maximum dimensions of the cropped characters
                max_w = max(f.width for f in frames)
                max_h = max(f.height for f in frames)
                # Ensure it has padding
                pad = 4
                max_w += pad * 2
                max_h += pad * 2
                
                # New perfectly packed sprite sheet
                new_img = Image.new("RGBA", (max_w * 3, max_h * 4), (255, 255, 255, 0))
                idx = 0
                for row in range(4):
                    for col in range(3):
                        if idx < len(frames):
                            frame = frames[idx]
                            x = col * max_w + pad + (max_w - pad*2 - frame.width) // 2
                            # Bottom align character
                            y = row * max_h + pad + (max_h - pad*2 - frame.height)
                            new_img.paste(frame, (x, y))
                            idx += 1
                new_img.save(walk_path, "PNG")
                print(f"Sliced {walk_name}: packed into {max_w}x{max_h} per frame (3x4 grid)")
                
        # Sit sheet: 1 row, 2 frames. Originally generated as 1200x896 (likely 4x5 grid but only top left matters)
        sit_name = f"{agent}-sit.png"
        sit_path = os.path.join(assets_dir, sit_name)
        if os.path.exists(sit_path):
            img = Image.open(sit_path).convert("RGBA")
            width, height = img.size
            cell_w = width // 5
            cell_h = height // 4
            
            frames = []
            for col in range(2): 
                box = (col * cell_w, 0, (col + 1) * cell_w, cell_h)
                frame = img.crop(box)
                bbox = frame.getbbox()
                if bbox: frames.append(frame.crop(bbox))
                else: frames.append(frame)
                
            if frames:
                max_w = max(f.width for f in frames)
                max_h = max(f.height for f in frames)
                pad = 4
                max_w += pad * 2
                max_h += pad * 2
                new_img = Image.new("RGBA", (max_w * 2, max_h), (255, 255, 255, 0))
                for col in range(2):
                    frame = frames[col]
                    x = col * max_w + pad + (max_w - pad*2 - frame.width) // 2
                    y = pad + (max_h - pad*2 - frame.height)
                    new_img.paste(frame, (x, y))
                new_img.save(sit_path, "PNG")
                print(f"Sliced {sit_name}: packed into {max_w}x{max_h} per frame (2x1 grid)")

if __name__ == "__main__":
    process_all_sprites()
