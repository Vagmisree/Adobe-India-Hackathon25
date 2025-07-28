import os
import sys
import json
from utils import extract_outline_from_pdf

INPUT_DIR = '/app/input'
OUTPUT_DIR = '/app/output'

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename[:-4] + '.json')
            try:
                result = extract_outline_from_pdf(pdf_path)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"Processed: {filename} -> {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
