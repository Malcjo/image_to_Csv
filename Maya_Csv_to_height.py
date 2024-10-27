import maya.cmds as cmds
import csv

def apply_csv_to_mesh(csv_path, plane_size=10, density=50, height_multiplier=10.0, high_res=False):
    # Step 1: Read CSV data
    height_data = []
    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it exists
        
        for row in reader:
            height_data.append([float(value) for value in row])
    
    # Get dimensions from CSV data
    num_rows = len(height_data)
    num_cols = len(height_data[0]) if num_rows > 0 else 0
    
    if high_res:
        # Full Resolution Mode
        plane = cmds.polyPlane(w=plane_size, h=plane_size, sx=num_cols - 1, sy=num_rows - 1)[0]
        vertices = cmds.ls("{}.vtx[*]".format(plane), flatten=True)
        
        if len(vertices) != num_rows * num_cols:
            print("Warning: CSV dimensions do not match the plane's subdivisions.")
            return

        for row in range(num_rows):
            for col in range(num_cols):
                height_value = height_data[row][col] * height_multiplier
                vertex_index = row * num_cols + col
                cmds.move(0, height_value, 0, vertices[vertex_index], relative=True)
    else:
        # Density-Controlled Downsample Mode
        row_step = max(num_rows // density, 1)
        col_step = max(num_cols // density, 1)
        
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
        
        for row in range(downsampled_rows):
            for col in range(downsampled_cols):
                height_value = downsampled_data[row][col] * height_multiplier
                vertex_index = row * downsampled_cols + col
                cmds.move(0, height_value, 0, vertices[vertex_index], relative=True)

# Function to open a file dialog and select a CSV file
def select_csv_file():
    file_path = cmds.fileDialog2(fileFilter="CSV Files (*.csv)", dialogStyle=2, fm=1)
    if file_path:
        cmds.textField("csvFilePath", edit=True, text=file_path[0])

# Function to generate the plane based on UI inputs
def generate_plane():
    csv_path = cmds.textField("csvFilePath", query=True, text=True)
    plane_size = cmds.floatField("planeSizeField", query=True, value=True)
    density = cmds.intField("densityField", query=True, value=True)
    height_multiplier = cmds.floatField("heightMultiplierField", query=True, value=True)
    high_res = cmds.checkBox("highResCheckbox", query=True, value=True)
    
    if csv_path:
        apply_csv_to_mesh(csv_path, plane_size, density, height_multiplier, high_res)
    else:
        cmds.warning("Please select a CSV file.")

# Function to create the dockable UI
def create_dockable_ui():
    # Check if the workspace control already exists, delete if necessary
    if cmds.workspaceControl("csvToPlaneToolWorkspaceControl", exists=True):
        cmds.deleteUI("csvToPlaneToolWorkspaceControl", control=True)
    
    # Create the dockable workspace control
    workspace_ctrl = cmds.workspaceControl("csvToPlaneToolWorkspaceControl", 
                                           label="CSV to Plane Tool",
                                           widthProperty="fixed", 
                                           initialWidth=400)

    # Set up a formLayout inside the workspace control for better docking compatibility
    form_layout = cmds.formLayout(parent=workspace_ctrl)
    fieldWith = 100

    # File selection
    csv_file_label = cmds.text(label="Select CSV File:", parent=form_layout)
    csv_file_text_field = cmds.textField("csvFilePath", width=300, parent=form_layout)
    browse_button = cmds.button(label="Browse", command=lambda x: select_csv_file(), parent=form_layout)
    
    # Input fields for parameters
    plane_size_label = cmds.text(label="Plane Size:", parent=form_layout)
    plane_size_field = cmds.floatField("planeSizeField",width=fieldWith, value=10, parent=form_layout)
    
    density_label = cmds.text(label="Density:", parent=form_layout)
    density_field = cmds.intField("densityField", width=fieldWith, value=50, parent=form_layout)
    
    height_multiplier_label = cmds.text(label="Height Multiplier:", parent=form_layout)
    height_multiplier_field = cmds.floatField("heightMultiplierField",width=fieldWith, value=10.0, parent=form_layout)
    
    # Checkbox for high resolution
    high_res_checkbox = cmds.checkBox("highResCheckbox", label="Full Resolution", parent=form_layout)
    
    # Generate button
    generate_button = cmds.button(label="Generate Plane", command=lambda x: generate_plane(), parent=form_layout)

    # Attach all elements to the form layout for organized docking
    cmds.formLayout(form_layout, edit=True,
        attachForm=[
            (csv_file_label, 'top', 10), (csv_file_label, 'left', 10),
            (csv_file_text_field, 'top', 10), (csv_file_text_field, 'left', 100),
            (browse_button, 'top', 10), (browse_button, 'right', 10),

            (plane_size_label, 'top', 40), (plane_size_label, 'left', 10),
            (plane_size_field, 'top', 40), (plane_size_field, 'left', 100),

            (density_label, 'top', 70), (density_label, 'left', 10),
            (density_field, 'top', 70), (density_field, 'left', 100),

            (height_multiplier_label, 'top', 100), (height_multiplier_label, 'left', 10),
            (height_multiplier_field, 'top', 100), (height_multiplier_field, 'left', 100),

            (high_res_checkbox, 'top', 130), (high_res_checkbox, 'left', 10),

            (generate_button, 'top', 160), (generate_button, 'left', 10), (generate_button, 'right', 10)
        ]
    )

# Run the dockable UI
create_dockable_ui()
