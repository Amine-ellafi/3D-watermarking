import trimesh

def embed_watermark(input_file, output_file, watermark_text):
    # Load 3D model
    mesh = trimesh.load(input_file)
    
    # Convert the watermark text into bytes or binary representation
    watermark_bin = ''.join(format(ord(char), '08b') for char in watermark_text)
    
    # Modify vertices or properties to embed the watermark
    vertices = mesh.vertices
    for i, bit in enumerate(watermark_bin):
        if i < len(vertices):
            # Example: Modify the x-coordinate of vertices based on the watermark binary
            if bit == '1':
                vertices[i][0] += 0.001  # Add a small value to the x-coordinate
            else:
                vertices[i][0] -= 0.001
    
    # Save the watermarked 3D model
    mesh.export(output_file)
    print(f"Watermark embedded and saved to {output_file}")

def extract_watermark(input_file, reference_file):
    # Load watermarked and reference 3D models
    mesh_watermarked = trimesh.load(input_file)
    mesh_reference = trimesh.load(reference_file)
    
    watermark_bin = ""
    vertices_watermarked = mesh_watermarked.vertices
    vertices_reference = mesh_reference.vertices
    
    for i in range(len(vertices_watermarked)):
        if vertices_watermarked[i][0] > vertices_reference[i][0]:
            watermark_bin += '1'
        else:
            watermark_bin += '0'
    
    # Convert binary string back to text
    watermark_text = ''.join(chr(int(watermark_bin[i:i+8], 2)) for i in range(0, len(watermark_bin), 8))
    w= str(watermark_text)
    print(f"Extracted watermark: {w.strip()}")
    print(f"the len is {len(w.strip())}")
    
    new=""
   
    for i in w :
        if ord(i) == 0:
            new = w.replace(i,"")
    print(f"Extracted watermark2: {new}")
    print(f"the len of new is {len(new)}")
    return new


if __name__=="__main__":
    # Example usage
    inp = "C:/Users/Amine ellafi/OneDrive/Desktop/hybrid/static/objs/water_ship.obj"
    out = "C:/Users/Amine ellafi/OneDrive/Desktop/hybrid/output/first_res.obj"
    embed_watermark(inp, out, '9e6b336d2f2bc1bc68c3c3ae504d649bb7b45c67b9efc05b58db9f3db2200b53')

    # Example usage
    extract_watermark(out, inp)
