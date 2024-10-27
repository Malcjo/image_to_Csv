import maya.cmds as cmds
import csv

def apply_csv_to_mesh(csv_path, plane_size=10, density=50, height_multiplier=10.0, high_res=False):
    # Step 1: Read CSV data
    height_data = []
    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row, if there is one
        
        for row in reader:
            height_data.append([float(value) for value in row])
    
    # Get dimensions from CSV data
    num_rows = len(height_data)
    num_cols = len(height_data[0]) if num_rows > 0 else 0
    
    #if high res is true, keep to the csv resolution
    if high_res:
        # Full Resolution Mode
        plane = cmds.polyPlane(w=plane_size, h=plane_size, sx=num_cols - 1, sy=num_rows - 1)[0]
        vertices = cmds.ls("{}.vtx[*]".format(plane), flatten=True)
        #{}.vrx[*] returns a list of all of the vertices on the plane
        #.format(plane) gets from the plane, then flattens for easy indexing
        
        if len(vertices) != num_rows * num_cols:
            print("Warning: CSV dimensions do not match the plane's subdivisions.")
            return

        # Apply height data at full resolution
        for row in range(num_rows):
            for col in range(num_cols):
                height_value = height_data[row][col] * height_multiplier  # Scale height
                vertex_index = row * num_cols + col
                cmds.move(0, height_value, 0, vertices[vertex_index], relative=True)
    else:
        # Density-Controlled Downsample Mode
        # get step size by dividing by the given density value
        row_step = max(num_rows // density, 1)
        col_step = max(num_cols // density, 1)
        
        # create new downsampled data
        # new lists created, from 0 - num_cols, by col_step
        # new lists created, from 0 - num_row, by row_step
        downsampled_data = [
            [height_data[row][col] for col in range(0, num_cols, col_step)]
            for row in range(0, num_rows, row_step)
        ]
        
        downsampled_rows = len(downsampled_data)
        downsampled_cols = len(downsampled_data[0]) if downsampled_rows > 0 else 0
        
        plane = cmds.polyPlane(w=plane_size, h=plane_size, sx=downsampled_cols - 1, sy=downsampled_rows - 1)[0]
        vertices = cmds.ls("{}.vtx[*]".format(plane), flatten=True)

        if len(vertices) != downsampled_rows * downsampled_cols:
            print("Warning: Downsampled data dimensions do not match the plane's subdivisions.")
            return
        
        # Apply downsampled height data
        for row in range(downsampled_rows):
            for col in range(downsampled_cols):
                height_value = downsampled_data[row][col] * height_multiplier  # Scale height
                vertex_index = row * downsampled_cols + col
                cmds.move(0, height_value, 0, vertices[vertex_index], relative=True)

# Example usage with high resolution
csv_path = r"D:\git\Projects\Python\Image_to_CSV\image_to_Csv\output.csv"
#apply_csv_to_mesh(csv_path, plane_size=200, density=50, height_multiplier=3.0, high_res=True)

# Example usage with downsampled density control
apply_csv_to_mesh(csv_path, plane_size=200, density=200, height_multiplier=3.0, high_res=False)
