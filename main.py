import sys
import os
from core import CssObfuscator

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.js> [carrier.png]")
        return

    input_file = sys.argv[1]
    carrier = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_file):
        print(f"[-] Error: File {input_file} not found.")
        return

    engine = CssObfuscator()
    print(f"[*] Processing: {input_file}")
    engine.build(input_file, carrier=carrier)

if __name__ == "__main__":
    main()