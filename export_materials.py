import bpy
import json
import os

def export_materials(file_path):
    """
    Exports selected materials from Blender to a JSON file.
    
    :param file_path: The path where the JSON file will be saved.
    """
    materials = []
    if bpy.context.selected_objects:
        for obj in bpy.context.selected_objects:
            if hasattr(obj, 'data') and obj.data and hasattr(obj.data, 'materials'):
                materials.extend([mat for mat in obj.data.materials if mat])
    
    if not materials:
        print("No materials found on selected objects.")
        return
    
    materials_data = []
    
    for mat in materials:
        mat_info = {
            "name": mat.name,
        }
        
        # Handle node-based materials (Blender 2.8+)
        if mat.use_nodes and mat.node_tree:
            principled = None
            for node in mat.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    principled = node
                    break
            
            if principled:
                mat_info["base_color"] = list(principled.inputs['Base Color'].default_value[:3])
                mat_info["roughness"] = principled.inputs['Roughness'].default_value
                mat_info["metallic"] = principled.inputs['Metallic'].default_value
            else:
                mat_info["base_color"] = [0.8, 0.8, 0.8]
                mat_info["roughness"] = 0.5
                mat_info["metallic"] = 0.0
        else:
            # Fallback for non-node materials
            mat_info["base_color"] = [0.8, 0.8, 0.8]
            mat_info["roughness"] = 0.5
            mat_info["metallic"] = 0.0
        
        materials_data.append(mat_info)
    
    # Writing to JSON file
    try:
        with open(file_path, 'w') as json_file:
            json.dump(materials_data, json_file, indent=4)
            print(f"Materials exported successfully to {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def main():
    # Set up the export path
    try:
        export_dir = bpy.path.abspath("//exports")
    except:
        # Fallback if blend file not saved
        export_dir = os.path.join(os.getcwd(), "exports")
    
    # Ensure the export directory exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Define the output file name
    output_file = os.path.join(export_dir, "exported_materials.json")
    
    export_materials(output_file)

if __name__ == "__main__":
    main()
