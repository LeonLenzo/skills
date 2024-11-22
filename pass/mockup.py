from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd

def generate_pass_image_from_csv(csv_path, output_dir="mockup_passes"):
    """
    Generate image-based mockups of wallet passes for clients based on data from a CSV file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the CSV file
    data = pd.read_csv(csv_path)
    
    for _, row in data.iterrows():
        # Create a blank pass image
        img = Image.new("RGB", (800, 600), color="white")
        draw = ImageDraw.Draw(img)
        
        # Load a font (ensure you have a compatible .ttf file)
        try:
            font = ImageFont.truetype("arial.ttf", size=20)  # Replace with the path to a TTF font if needed
        except:
            font = ImageFont.load_default()
        
        # Add client information
        draw.text((20, 20), f"Name: {row['Name']}", fill="black", font=font)
        draw.text((20, 60), f"DOB: {row.get('DOB', 'N/A')}", fill="black", font=font)
        draw.text((20, 100), f"Email: {row.get('Email', 'N/A')}", fill="black", font=font)
        draw.text((20, 140), f"Phone: {row.get('Mobile', 'N/A')}", fill="black", font=font)
        
        # Add completed units
        course_code = row.get("Course Code", "N/A")
        course_name = row.get("Course Name", "N/A")
        completed_units = f"Completed Units:\n{course_code}: {course_name}"
        draw.text((20, 180), completed_units, fill="black", font=font)
        
        # Save the mockup
        unique_id = row.get("Unique ID", f"{row['Name']}_mockup")
        output_path = os.path.join(output_dir, f"{unique_id}.png")
        img.save(output_path)
        print(f"Mockup saved to {output_path}")

# Example usage
csv_path = "certificates.csv"  # Path to the CSV file
generate_pass_image_from_csv(csv_path)
