from PIL import Image

def process_image(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    # Create new image data replacing green with transparent
    # The green is close to (0, 255, 0). We can use a tolerance.
    new_data = []
    for item in data:
        # Check if color is close to pure green
        if item[1] > 200 and item[0] < 50 and item[2] < 50:
            new_data.append((255, 255, 255, 0)) # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    
    width, height = img.size
    
    # We want exactly 3 frames in a row. The image has 3 columns and 2 rows.
    # The total width is 'width', meaning each frame is roughly width // 3
    # We just crop the top row (0 to height // 2)
    top_row = img.crop((0, 0, width, height // 2))
    
    top_row.save(output_path, "PNG")
    print(f"Saved {output_path} with size {top_row.size}")

if __name__ == "__main__":
    process_image(r"C:\Users\respl\OneDrive\Aptus Flow\bmad\Male_programmer_walking_202604062120 (2).png", r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\assets\barry.png")
