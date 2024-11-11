import numpy as np
import scipy.fftpack as fftpack

# Function to load and parse .off files
def load_off_file(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        if first_line.startswith('OFF'):
            first_line = first_line[3:].strip()  # Remove 'OFF' and strip whitespace
            if first_line:
                n_verts, n_faces, n_edges = map(int, first_line.split())
            else:
                n_verts, n_faces, n_edges = map(int, file.readline().strip().split())
        else:
            raise Exception(f'Not a valid OFF file: {file_path}')
        
        # Read the vertices
        verts = []
        for _ in range(n_verts):
            line = file.readline().strip().split()
            if len(line) == 3:
                verts.append(list(map(float, line)))
        
        # Read the faces (not used here)
        faces = []
        for _ in range(n_faces):
            line = file.readline().strip().split()
            if len(line) >= 4:  # Typically, the first number is the face size, followed by the vertex indices
                faces.append(list(map(int, line[1:])))  # Skip the first number (face size), only keep vertex indices
        
        verts = np.array(verts, dtype=np.float32)
        
        return verts, faces

# Function to save modified vertices to a new .off file
def save_obj(vertices, faces, output_file):
    with open(output_file, 'w') as file:
        file.write("OFF\n")
        file.write(f"{len(vertices)} {len(faces)} 0\n")  # Write vertex and face count
        
        # Write the vertices
        for vert in vertices:
            file.write(f"{vert[0]} {vert[1]} {vert[2]}\n")
        
        # Write the faces
        for face in faces:
            file.write(f"{len(face)} " + " ".join(map(str, face)) + "\n")  # Face size followed by vertex indices

# Function to apply DCT and embed watermark
def embed_watermark(vertices, watermark, alpha=0.1):
    # Flatten the vertices
    original_flat = vertices.flatten()
    
    # Apply DCT
    dct_coefficients = fftpack.dct(original_flat, norm='ortho')

    # Embed the watermark by modifying the first few coefficients
    for i in range(len(watermark)):
        dct_coefficients[i] += alpha * watermark[i]  # Modify DCT coefficients with watermark

    # Inverse DCT to get the watermarked vertices
    watermarked_flat = fftpack.idct(dct_coefficients, norm='ortho')
    watermarked_vertices = watermarked_flat.reshape(vertices.shape)
    
    return watermarked_vertices

# Function to extract watermark from DCT coefficients
def extract_watermark(vertices, original_vertices, alpha=0.1, watermark_length=4):
    # Flatten the modified vertices
    modified_flat = vertices.flatten()
    original_flat = original_vertices.flatten()
    
    # Apply DCT
    dct_coefficients = fftpack.dct(modified_flat, norm='ortho')

    # Extract the watermark from the modified DCT coefficients
    extracted_watermark = np.zeros(watermark_length)
    for i in range(watermark_length):
        extracted_watermark[i] = (dct_coefficients[i] - (fftpack.dct(original_flat, norm='ortho')[i])) / alpha  # Retrieve watermark

    # Clamp values to ensure they are within valid ASCII range
    extracted_watermark = np.clip(extracted_watermark, 0, 1)

    return extracted_watermark

# Main execution
if __name__ == "__main__":
    # Load a 3D model
    input_file = 'static/offs/water_ship.off'  # Replace with your .off file path
    output_file = 'output/model.off'  # Replace with your output .off file path
    vertices, faces = load_off_file(input_file)

    # Define watermark
    watermark_text = "kobso"  # Replace with your watermark text
    watermark = np.array([ord(char) / 255.0 for char in watermark_text])  # Normalize ASCII values

    # Embed watermark
    watermarked_vertices = embed_watermark(vertices, watermark)

    # Save the watermarked model
    save_obj(watermarked_vertices, faces, output_file)
    print("Watermark applied and saved to:", output_file)

    # Extract watermark from the watermarked model
    extracted_watermark = extract_watermark(watermarked_vertices, vertices)
    
    # Convert extracted watermark to characters
    extracted_watermark_text = ''.join([chr(int(value * 255)) for value in extracted_watermark])
    
    print("Extracted Watermark:", extracted_watermark_text)
