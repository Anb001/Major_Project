import os
import re
import pandas as pd

# Define the folder containing the images
image_folder = "Dataset"

# Get all PNG image files
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

# Create a list to store metadata
metadata = []

# Process each image file
for filename in image_files:
    # Extract modulation type (QPSK, 8QAM, or 16QAM)
    modulation = "Unknown"
    if "QPSK" in filename:
        modulation = "QPSK"
    elif "8QAM" in filename:
        modulation = "8QAM"
    elif "16QAM" in filename:
        modulation = "16QAM"

    # Extract OSNR, ROF, and Skew values using regex
    osnr_match = re.search(r'OSNR(\d+)', filename)
    rof_match = re.search(r'ROF(\d+_?\d*)', filename)  # Match both `ROF1_0` and `ROF1`
    skew_match = re.search(r'Skew(neg?\d+|\d+)', filename)  # Now captures positive Skew values too

    # Convert extracted values safely
    osnr_dB = int(osnr_match.group(1)) if osnr_match else None
    rof = None
    skew_ps = None

    if rof_match:
        rof_str = rof_match.group(1).replace('_', '.')  # Convert `_` to `.`
        if "." not in rof_str:  # If no decimal, assume `.0` (e.g., `ROF1` → `1.0`)
            rof_str += ".0"
        rof = float(rof_str)

    if skew_match:
        skew_str = skew_match.group(1).replace('neg', '-')  # Convert `neg` to `-`
        skew_ps = int(skew_str)

    # Debugging: Print filenames that result in NaN values
    if osnr_dB is None or rof is None or skew_ps is None:
        print(f"⚠️ Skipped: {filename} (OSNR={osnr_dB}, ROF={rof}, Skew={skew_ps})")

    # Append only valid data (skip invalid entries)
    if osnr_dB is not None and rof is not None and skew_ps is not None:
        metadata.append([filename, modulation, osnr_dB, rof, skew_ps])

# Create a DataFrame
df = pd.DataFrame(metadata, columns=["Filename", "Modulation", "OSNR_dB", "ROF", "Skew_ps"])

# Define the output CSV file path
csv_file = "eye_diagrams_metadata.csv"

# Save metadata to CSV file
df.to_csv(csv_file, index=False)

print(f"✅ CSV file created successfully: {csv_file}")
print(f"Total valid datasets: {len(df)}")
