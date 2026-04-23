from PIL import Image

def process_image(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    # Create new image data replacing green with transparent
    # We need a wider tolerance for anti-aliasing artifacts on the edge
    new_data = []
    for item in data:
        # Check if color is close to pure green
        if item[1] > 180 and item[0] < 100 and item[2] < 100:
            new_data.append((255, 255, 255, 0)) # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    
    width, height = img.size
    
    # We want to tightly crop the character, but keep consistent spacing.
    # The image is exactly 3 frames wide and 2 high.
    # So the top row is height // 2
    top_row = img.crop((0, 0, width, height // 2))
    
    top_row.save(output_path, "PNG")
    print(f"Saved {output_path} with size {top_row.size}")

if __name__ == "__main__":
    process_image(r"C:\Users\respl\OneDrive\Aptus Flow\bmad\Male_programmer_walking_202604062120 (2).png", r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\assets\barry.png")
