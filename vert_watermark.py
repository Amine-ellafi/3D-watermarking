import dct2 as dct 
import try5 as vr 
import off_to_obj as oto
import numpy as np
import hashlib

def hash_text(text):
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Encode the text to bytes and update the hash object
    sha256_hash.update(text.encode('utf-8'))
    
    # Get the hexadecimal representation of the hash
    hashed_text = sha256_hash.hexdigest()
    
    return hashed_text



if __name__ == "__main__":
    # Load a 3D model
    alpha =0.1
    
    input_file = 'static/offs/water_ship.off'  # Replace with your .off file path
    output_file = 'output/new.off'  # Replace with your output .off file path
    vertices, faces = dct.load_off_file(input_file)

    # Define watermark
    watermark_text = "opoera"  # Replace with your watermark text

    watermark = np.array([ord(char) / 255.0 for char in watermark_text])  # Normalize ASCII values

    # Embed watermark
    watermarked_vertices = dct.embed_watermark(vertices, watermark,alpha)

    # Save the watermarked model
    dct.save_obj(watermarked_vertices, faces, output_file)
    print("Watermark applied and saved to:", output_file)

    # Extract watermark from the watermarked model
    extracted_watermark = dct.extract_watermark(watermarked_vertices, vertices,alpha,len(watermark_text))
    
    # Convert extracted watermark to characters
    extracted_watermark_text = ''.join([chr(int(value * 255)) for value in extracted_watermark])
    while (extracted_watermark_text != watermark_text):
        alpha += 0.1
        watermarked_vertices = dct.embed_watermark(vertices, watermark,alpha)
        dct.save_obj(watermarked_vertices, faces, output_file)
        extracted_watermark = dct.extract_watermark(watermarked_vertices, vertices,alpha,len(watermark_text))
    
        # Convert extracted watermark to characters
        extracted_watermark_text = ''.join([chr(int(value * 255)) for value in extracted_watermark])
        print(f"alpha: {alpha} => {extracted_watermark_text}")

    print("Extracted Watermark:", extracted_watermark_text)
    x= round(alpha,2)
    print("alpha the final = ",alpha)

    
    to_pass = "ID"+str(x)
    print(f"to_pass = {to_pass}")
    # Example usage
    text_to_hash = to_pass
    hashed_text = hash_text(text_to_hash)
    print(f"Original text: {text_to_hash}")
    print(f"Hashed text: {hashed_text}")
    
    print("="*100)
    second_input ="output/new.obj"
    final_output="output/last_watermark.obj"
    oto.off_to_obj(output_file,second_input)
    vr.embed_watermark(second_input,final_output,hashed_text)





