import numpy as np
import trimesh
import random

# Function to apply translation
def apply_translation(mesh, translation_vector):
    mesh.apply_translation(translation_vector)
    return mesh

# Function to apply scaling
def apply_scaling(mesh, scale_factor):
    mesh.apply_scale(scale_factor)
    return mesh

# Function to apply rotation
def apply_rotation(mesh, rotation_angle, axis):
    rotation_matrix = trimesh.transformations.rotation_matrix(rotation_angle, axis)
    mesh.apply_transform(rotation_matrix)
    return mesh

# Function to apply noise
def apply_noise(mesh, noise_level):
    vertices = mesh.vertices
    noise = np.random.normal(0, noise_level, vertices.shape)
    mesh.vertices += noise
    return mesh

# Function to apply shear
def apply_shear(mesh, shear_factor, axis):
    shear_matrix = np.eye(4)
    shear_matrix[axis, (axis + 1) % 3] = shear_factor
    mesh.apply_transform(shear_matrix)
    return mesh

# Function to apply attack based on the specified type and parameters
def apply_attack(mesh, attack_type, params):
    if attack_type == 'translation':
        return apply_translation(mesh, np.array(params['translation_vector']))
    elif attack_type == 'scaling':
        return apply_scaling(mesh, params['scale_factor'])
    elif attack_type == 'rotation':
        return apply_rotation(mesh, params['rotation_angle'], np.array(params['axis']))
    elif attack_type == 'noise':
        return apply_noise(mesh, params['noise_level'])
    elif attack_type == 'shear':
        return apply_shear(mesh, params['shear_factor'], params['axis'])
    else:
        raise ValueError("Unknown attack type.")

# Function to apply all attacks and save the results with unique names
def apply_all_attacks(input_file, output_directory):
    # Load the 3D model
    mesh = trimesh.load_mesh(input_file)
    
    # Specify attack parameters
    attack_params = {
        'translation': {'translation_vector': [0.1, 0.2, 0.3]},
        'scaling': {'scale_factor': 1.2},
        'rotation': {'rotation_angle': np.pi / 6, 'axis': [0, 0, 1]},  # Rotate by 30 degrees around Z axis
        'noise': {'noise_level': 0.001},
        'shear': {'shear_factor': 0.5, 'axis': 0}  # Shear along X-axis
    }

    # Apply each attack and save the modified model with unique name
    for attack_type, params in attack_params.items():
        # Apply the attack to the mesh
        modified_mesh = apply_attack(mesh, attack_type, params)
        
        # Define output file name based on the attack type
        output_file = f"attacked_{attack_type}.obj"
        
        # Save the modified mesh to output file
        modified_mesh.export(output_file)
        print(f"Saved attacked model with {attack_type} attack to {output_file}")

# Example usage
input_file = 'result.obj'  # Change to the actual file path
output_directory = 'attack'  # Change to your desired output directory

# Apply all attacks and save the results
apply_all_attacks(input_file, output_directory)
