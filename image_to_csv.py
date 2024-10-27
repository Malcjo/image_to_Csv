from PIL import Image
import csv

def image_to_csv(image_path, csv_path):
    img = Image.open(image_path).convert("L")
    width, height = img.size

    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['row', 'col', 'height'])

        for y in range(height):
            row_data = []
            for x in range(width):
                grayscale_value = img.getpixel((x, y))
                height_value = grayscale_value / 255.0
                row_data.append(height_value)

            writer.writerow(row_data)
    print(f"CSV file save at {csv_path}")

image_path = "D:\git\Projects\Python\Image to CSV\image_to_Csv\heightmap.png"
csv_path = "output.csv"
image_to_csv(image_path, csv_path)