import os
from PIL import Image

assets_dir = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\assets"

def remove_green_bg(img):
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        # Check if color is close to pure green (chroma key)
        if item[1] > 180 and item[0] < 100 and item[2] < 100:
            new_data.append((255, 255, 255, 0)) # Transparent
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img

def process_all():
    avatars = ["Amelia.png", "Bob.png", "John.png", "mary.png", "paige.png", "Quin.png", "Sally.png", "Winston.png"]
    
    for avatar in avatars:
        path = os.path.join(assets_dir, avatar)
        if os.path.exists(path):
            img = Image.open(path)
            # Remove bg
            img = remove_green_bg(img)
            # If the image is large (like 2 rows), crop top half
            width, height = img.size
            if height > 500: # Assuming 2-row images are around 768-1024h
                img = img.crop((0, 0, width, height // 2))
            
            img.save(path, "PNG")
            print(f"Processed avatar: {avatar}")
            
    # Process PA (Desk)
    pa_path = os.path.join(assets_dir, "PA.png")
    if os.path.exists(pa_path):
        img = Image.open(pa_path)
        img = remove_green_bg(img)
        img.save(pa_path, "PNG")
        print("Processed PA.png")

if __name__ == "__main__":
    process_all()
