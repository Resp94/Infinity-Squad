import os
import shutil

src_dir = r"C:\Users\respl\OneDrive\Aptus Flow\bmad"
dest_dir = r"C:\Users\respl\OneDrive\Aptus Flow\bmad\_bmad-output\dashboard\assets"

mapping = {
    "Amelia (1).png": "amelia-sit.png",
    "Amelia-caminhando (1).png": "amelia-walk.png",
    "Barry (1).png": "barry-sit.png",
    "Barry-caminhando (1).png": "barry-walk.png",
    "Bob (1).png": "bob-sit.png",
    "Bob-caminhando (1).png": "bob-walk.png",
    "Boos (1).png": "boss-sit.png",
    "Boos-caminhando (1).png": "boss-walk.png",
    "John (1).png": "john-sit.png",
    "John - caminhando (1).png": "john-walk.png",
    "mary (1).png": "mary-sit.png",
    "Mary - caminhando (1).png": "mary-walk.png",
    "Paige (1).png": "paige-sit.png",
    "Paige - caminhando (1).png": "paige-walk.png",
    "Quin (1).png": "quinn-sit.png",
    "Quin - caminhando (1).png": "quinn-walk.png",
    "Sally (1).png": "sally-sit.png",
    "Sally - caminhando (1).png": "sally-walk.png",
    "Winston (1).png": "winston-sit.png",
    "Winston - caminhando (1).png": "winston-walk.png",
    "PA (1).png": "pa-desk.png",
    "PA - Boos (1).png": "boss-desk.png",
    "Escritorio.png": "office-map.png"
}

os.makedirs(dest_dir, exist_ok=True)

for src_name, dest_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} -> {dest_name}")
    else:
        print(f"Warning: Missing {src_name}")

print("Asset organization complete.")
