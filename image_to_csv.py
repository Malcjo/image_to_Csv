from PIL import Image
import csv
#import python imaging library PIL

def image_to_csv(image_path, csv_path):
    img = Image.open(image_path).convert("L") #"L" opens image in grascale mode
    width, height = img.size #width and height of image in pixels

    #'W' writeonly mode
    # with open, allows for exception handling and closes the file after use
    #newline specificed to avoid new lines
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['row', 'col', 'height']) #create row, col, height headers
        #height is the grayuscale
        #loop through x and y with the height and width
        for y in range(height):
            row_data = []
            for x in range(width):
                grayscale_value = img.getpixel((x, y))
                height_value = grayscale_value / 255.0 #normalise to be betwen 0-1
                row_data.append(height_value)

            writer.writerow(row_data)
    print(f"CSV file save at {csv_path}")

image_path = "D:\git\Projects\Python\Image_to_CSV\image_to_Csv\heightmap.png"
csv_path = "output.csv"
image_to_csv(image_path, csv_path)