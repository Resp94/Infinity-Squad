import os
from PIL import Image

assets_dir = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\assets"

def fix_all_sprites():
    names_map = {
        "amelia": ("Amelia-caminhando (1).png", "Amelia (1).png"),
        "barry": ("Barry-caminhando (1).png", "Barry (1).png"),
        "bob": ("Bob-caminhando (1).png", "Bob (1).png"),
        "boss": ("Boos-caminhando (1).png", "Boos (1).png"),
        "john": ("John - caminhando (1).png", "John (1).png"),
        "mary": ("Mary - caminhando (1).png", "mary (1).png"),
        "paige": ("Paige - caminhando (1).png", "Paige (1).png"),
        "quinn": ("Quin - caminhando (1).png", "Quin (1).png"),
        "sally": ("Sally - caminhando (1).png", "Sally (1).png"),
        "winston": ("Winston - caminhando (1).png", "Winston (1).png")
    }
    
    for agent, (walk_file, sit_file) in names_map.items():
        # --- 1. Slicing the WALKING Sprites ---
        walk_name = f"{agent}-walk.png"
        walk_path = os.path.join(assets_dir, walk_name)
        
        raw_path = os.path.join(r"C:\Users\respl\OneDrive\Aptus Flow\bmad", walk_file)
        if not os.path.isfile(raw_path):
            print(f"Could not find raw walking file for {agent}")
            continue

        print(f"Processing raw file: {raw_path}")
        img = Image.open(raw_path).convert("RGBA")
        
        # Remove green background (chroma key)
        data = img.getdata()
        new_data = []
        for item in data:
            if item[1] > 180 and item[0] < 100 and item[2] < 100:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item)
        img.putdata(new_data)
        
        # The AI generates exactly 1200x896 images with 5 cols and 4 rows.
        # This means each cell is exactly 240x224.
        cell_w = 240
        cell_h = 224
        
        # We want to extract a 3x4 grid for our CSS (only the first 3 frames of animation)
        # And we want to scale each frame down to a reasonable size for the web, like 48x48 or 64x64.
        target_size = 64
        
        new_walk_img = Image.new("RGBA", (target_size * 3, target_size * 4), (255, 255, 255, 0))
        
        for row in range(4):
            for col in range(3):
                box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
                frame = img.crop(box)
                
                # Resize the frame to 64x64
                frame.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
                
                x_offset = (target_size - frame.width) // 2
                y_offset = (target_size - frame.height) // 2
                
                x = col * target_size + x_offset
                y = row * target_size + y_offset
                
                new_walk_img.paste(frame, (x, y))
                
        new_walk_img.save(walk_path, "PNG")
        print(f"Saved perfect sprite sheet: {walk_name} (192x256)")

        # --- 2. Slicing the SITTING Sprites (originally 1200x896, we only want top 2 frames) ---
        sit_name = f"{agent}-sit.png"
        sit_path = os.path.join(assets_dir, sit_name)
        
        raw_sit_path = os.path.join(r"C:\Users\respl\OneDrive\Aptus Flow\bmad", sit_file)
        if not os.path.isfile(raw_sit_path):
            print(f"Could not find raw sitting file for {agent}")
            continue
            
        sit_img = Image.open(raw_sit_path).convert("RGBA")
        
        data = sit_img.getdata()
        new_data = []
        for item in data:
            if item[1] > 180 and item[0] < 100 and item[2] < 100:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        sit_img.putdata(new_data)
        
        new_sit_img = Image.new("RGBA", (target_size * 2, target_size), (255, 255, 255, 0))
        
        for col in range(2):
            box = (col * cell_w, 0, (col + 1) * cell_w, cell_h)
            frame = sit_img.crop(box)
            frame.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
            
            x_offset = (target_size - frame.width) // 2
            y_offset = (target_size - frame.height) // 2
            
            x = col * target_size + x_offset
            y = y_offset
            
            new_sit_img.paste(frame, (x, y))
            
        new_sit_img.save(sit_path, "PNG")
        print(f"Saved perfect sitting sheet: {sit_name} (128x64)")

if __name__ == "__main__":
    fix_all_sprites()
