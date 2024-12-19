import numpy as np

# Function to calculate Normalized Correlation (NC)
def calculate_nc(original_watermark, extracted_watermark):
    # Ensure both watermarks are of the same length
    # If lengths differ, we truncate or pad them (simple padding with 0 here for simplicity)
    max_len = max(len(original_watermark), len(extracted_watermark))
    
    original = np.array([ord(c) for c in original_watermark.ljust(max_len)])
    extracted = np.array([ord(c) for c in extracted_watermark.ljust(max_len)])
    
    # Calculate the numerator and denominator for NC
    numerator = np.sum(original * extracted)
    denominator = np.sqrt(np.sum(original**2)) * np.sqrt(np.sum(extracted**2))
    
    # Calculate and print the NC
    nc = numerator / denominator
    print(f"NC: {nc}")
    return nc

# Example watermarks (original and extracted)
original_watermark = "hello"
extracted_watermark = "ýxwiå"

# Call the function to calculate NC
x= calculate_nc(original_watermark, extracted_watermark)

original_watermark2 = "this is a watermark for test"
extracted_watermark2= """ ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ"""
y = calculate_nc(original_watermark2,extracted_watermark2)

print(f"final nc is : {(x+y)/2}")