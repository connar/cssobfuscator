# cssobfuscator
**What is it**:  
I once needed to make a CTF challenge and obfuscate js of an html page. There are some js obfuscators out there that mainly try to obfuscate via CFF or other methods that make the code completely unreadable (and sussy looking).  

I then had the idea of making a PoC js obfuscator via css elements. Since js can often pull data from css elements, I thought why not hide payloads or executables (i.e. driveby downloads) inside css elements.  

Thus, this PoC obfuscator. So the main idea is to move strings into the CSSOM.  

**CSS storage techniques**:  
Since its a PoC, the techniques to store data in the css are not extensive. The obfuscator uses the following css properties to store data:
- `calc()`: Uses `calc()` and css variables to store ASCII values as pixel offsets.
- `clamp(min, val, max)`: Uses `clamp()` to "lock" a value and basically hide a byte.
- `conic-gradient(from [num]deg, [color], [color])`: Uses `conic-gradient()` to hide a byte at `deg`.
- `order`: Uses `order` to hide a byte.

**Hiding driveby executables in PNG**:  
For driveby download PoC's, the executable is hidden encrypted in a PNG that is pulled dynamically from your server. The obfuscated js handles the extraction of the bytes and their decryption. Specifically:  
- The LSB is used within the Alpha Channel of the PNG.
- A unique key is generated on obfuscation time to xor the bytes (every run different key).
- On runtime, a canvas element (which is never added to the page) is used to load and draw the image. By using getImageData, RGBA values are extracted. The binary is rebuilded by taking the last bit of every 4th byte and then xor decrypting it.


**Requirements**:  
You need:  
- Python 3.10+
- Pillow

To install the requirements, run:  
`pip install -r requirements.txt`

**How to run**:  
If you have an embedded binary (for driveby download for example), you can run the obfuscator as:  
`python main.py clean.js innocent_image.jpg`  
If you don't provide an image, a randomized image will be generated for you.

For normal .js, you run the obfuscator without providing any image.

**Usage Notice**: This is a PoC obfuscator. Althought there are some demo .js files under the `examples` folder, I have not extensively tested the obfuscator to cover all edge cases.  

> *Disclaimer: This project is intended for educational and research purposes only*
