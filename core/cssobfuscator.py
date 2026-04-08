import re, random, sys, math, base64, io, json, os
from PIL import Image

sys.set_int_max_str_digits(0)

class CssObfuscator:
    def __init__(self, png_side=128):
        self.png_side = png_side
        self.css_rules = []
        self.used_ids = set()
        self.string_lookup = {} 
        self.symbol_map = {}
        self.payload_key = random.randint(30, 90)
        self.stego_payload = ""
        
        # objects and properties that won't get obfuscated
        self.protected = {
            'window', 'document', 'console', 'navigator', 'clipboard', 'atob', 'btoa', 
            'Uint8Array', 'Blob', 'URL', 'parseInt', 'setTimeout', 'getComputedStyle', 
            'Object', 'String', 'Math', 'Image', 'Promise', 'canvas', '2d', 'onload', 
            'onerror', 'body', 'appendChild', 'removeChild', 'createElement'
        }

    def get_id(self, length=10):
        while True:
            rid = "z" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))
            if rid not in self.used_ids:
                self.used_ids.add(rid)
                return rid

    def generate_math(self, n):
        n = int(n)
        r1, r2 = random.randint(10, 200), random.randint(10, 200)
        diff = r1 + r2 - n
        return f"({hex(r1)} + {r2} - {diff})"

    def generate_png(self, output_path, carrier_path=None):
        if not self.stego_payload: return False
        clean_payload = "".join(self.stego_payload.split())
        data_bytes = (clean_payload + "\0").encode()
        enc = bytearray([(b ^ self.payload_key) for b in data_bytes])
        bits = "".join([format(b, '08b') for b in enc])
        
        if carrier_path and os.path.exists(carrier_path):
            img = Image.open(carrier_path).convert('RGBA')
        else:
            img = Image.new('RGBA', (self.png_side, self.png_side), (128, 128, 128, 255)) 
        
        width, height = img.size
        pixels = img.load()
        bit_idx = 0
        for y in range(height):
            for x in range(width):
                if bit_idx >= len(bits): break
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, (a & 0xFE) | int(bits[bit_idx]))
                bit_idx += 1
        img.save(output_path, "PNG")
        return True

    def obf_str(self, content, r_map_name):
        if not content: return "''"
        local_ids = []
        for char in content:
            cls = self.get_id()
            val = ord(char)
            strategy = random.choice(['CALC', 'CLAMP', 'CONIC', 'ORDER'])
            if strategy == 'CONIC':
                rule = f".{cls}{{background-image:conic-gradient(from {val}deg,#f00,#00f);z-index:40;}}"
            elif strategy == 'CLAMP':
                rule = f".{cls}{{font-size:clamp({val}px,{val}px,{val}px);z-index:10;}}"
            elif strategy == 'CALC':
                h = random.randint(100, 500)
                rule = f".{cls}{{--h:{(h*256)+val};margin-top:calc((var(--h) - ({h}*256))*1px);z-index:30;}}"
            else:
                rule = f".{cls}{{order:{val};z-index:35;}}"
            self.css_rules.append(rule)
            local_ids.append(cls)
        l_id = self.get_id(6)
        self.string_lookup[l_id] = local_ids
        return f"{r_map_name}.{l_id}"

    def process_js(self, js_code, r_map_name, r_payload_name):
        def structural_key_fixer(match):
            prefix, key_name = match.group(1), match.group(3)
            return f"{prefix}__KEY_START__{key_name}__KEY_END__:"

        js_code = re.sub(r'([{,]\s*)([\'"]?)([a-zA-Z0-9_$][\w$-]*)\2\s*:', structural_key_fixer, js_code)

        id_patterns = [r'\b(?:const|let|var)\s+([a-zA-Z_$][\w$]*)', r'function\s*([a-zA-Z_$][\w$]*)*\s*\(([^)]*)\)']
        for pattern in id_patterns:
            for m in re.finditer(pattern, js_code):
                for group in m.groups():
                    if group:
                        for sym in group.split(','):
                            sym = sym.strip().split('=')[0].strip()
                            if sym and sym not in self.symbol_map and (sym not in self.protected or sym == 'data'):
                                if sym not in {r_map_name, r_payload_name}:
                                    self.symbol_map[sym] = self.get_id(8)

        lines = js_code.split('\n')
        processed_lines = []
        in_multicomment = False

        for line in lines:
            if not in_multicomment:
                if line.strip().startswith('/*'):
                    in_multicomment = True
                    if '*/' in line: in_multicomment = False
                    processed_lines.append(line)
                    continue
                if line.strip().startswith('//'):
                    processed_lines.append(line)
                    continue
            else:
                if '*/' in line: in_multicomment = False
                processed_lines.append(line)
                continue

            def stego_handler(match):
                content = match.group(2)
                if len(content) > 500:
                    self.stego_payload = content
                    return r_payload_name
                return self.obf_str(content, r_map_name)

            line = re.sub(r'([\'"])(.*?)\1', stego_handler, line)
            line = re.sub(r'\b(?<!' + r_map_name + r'\.z)(?<!\.)\d+\b(?!\.)', lambda m: self.generate_math(m.group(0)), line)
            line = re.sub(r'(?<!' + r_map_name + r')\.([a-zA-Z_$][\w$]*)', 
                          lambda m: m.group(0) if m.group(1) in self.protected else f"[{self.obf_str(m.group(1), r_map_name)}]", line)
            processed_lines.append(line)

        final_code = '\n'.join(processed_lines)
        for sym, rand_id in self.symbol_map.items():
            final_code = re.sub(r'\b' + re.escape(sym) + r'\b', rand_id, final_code)
        
        def final_key_resolver(match):
            return f"[{self.obf_str(match.group(1), r_map_name)}]"
        return re.sub(r'__KEY_START__(.*?)__KEY_END__', final_key_resolver, final_code)

    def build(self, input_file, carrier=None):
        if not os.path.exists(input_file): return
        
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(os.getcwd(), base_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(input_file, "r") as f: user_js = f.read()

        r_map, r_glob, r_pay_var = self.get_id(7), self.get_id(7), self.get_id(7)
        r_res_fn, r_stego_fn = self.get_id(9), self.get_id(9)
        ri_vars = [self.get_id(8) for _ in range(26)]
        ri_key_var, ri_ctn, ri_lst, ri_emap, ri_cache, ri_cls, ri_elem, ri_style, ri_zindex, ri_val, ri_match, ri_key, ri_img, ri_canv, ri_ctx, ri_data, ri_out, ri_j, ri_bits, ri_b, ri_idx, ri_cc, ri_fmap, ri_res, ri_r, ri_err = ri_vars

        obf_user = self.process_js(user_js, r_map, r_pay_var)
        num = lambda n: self.generate_math(n)

        stego_logic, stego_call = "", ""
        stego_init = f'let {r_pay_var} = "";'
        if self.stego_payload:
            self.generate_png(os.path.join(output_dir, "asset.png"), carrier_path=carrier)
            stego_init = f'let {r_pay_var} = ""; const {ri_key_var} = {num(self.payload_key)};'
            stego_call = f'{r_pay_var} = await {r_stego_fn}();'
            stego_logic = f"""
    const {r_stego_fn} = () => new {r_glob}.Promise({ri_res} => {{
        const {ri_img} = new {r_glob}.Image(); {ri_img}.src = {self.obf_str("./asset.png", r_map)}; {ri_img}.crossOrigin = {self.obf_str("Anonymous", r_map)};
        {ri_img}.onload = () => {{
            const {ri_canv} = {r_glob}.document.createElement({self.obf_str("canvas", r_map)}); const {ri_ctx} = {ri_canv}.getContext({self.obf_str("2d", r_map)});
            {ri_canv}.width = {ri_img}.width; {ri_canv}.height = {ri_img}.height; {ri_ctx}.drawImage({ri_img}, {num(0)}, {num(0)});
            const {ri_data} = {ri_ctx}.getImageData({num(0)}, {num(0)}, {ri_img}.width, {ri_img}.height).data;
            let {ri_out} = "";
            for(let {ri_j}={num(0)}; {ri_j}<{ri_data}.length; {ri_j}+={num(4)}) {{
                let {ri_bits} = "";
                for(let {ri_b}={num(0)}; {ri_b}<{num(8)}; {ri_b}++) {{ 
                    let {ri_idx} = {ri_j} + ({ri_b} * {num(4)}) + {num(3)};
                    if({ri_idx} < {ri_data}.length) {ri_bits} += ({ri_data}[{ri_idx}] & {num(1)}); 
                }}
                let {ri_cc} = parseInt({ri_bits}, {num(2)}) ^ {ri_key_var};
                if({ri_cc} === {num(0)}) break;
                {ri_out} += {r_glob}.String.fromCharCode({ri_cc});
                {ri_j} += {num(28)};
            }}
            {ri_res}({ri_out});
        }};
        {ri_img}.onerror = () => {ri_res}("");
    }});"""

        loader = f"""(async () => {{
    const {r_map} = {{}}; {stego_init}
    const {r_glob} = (typeof globalThis !== 'undefined') ? globalThis : (typeof window !== 'undefined') ? window : self;
    const {r_res_fn} = async ({ri_fmap}) => {{
        const {ri_ctn} = {r_glob}.document.createElement({self.obf_str("div", r_map)});
        {ri_ctn}.style.cssText = {self.obf_str("position:fixed;top:0;left:0;width:1px;height:1px;z-index:-1;opacity:0.01;overflow:hidden;", r_map)};
        const {ri_lst} = {r_glob}.Object.values({ri_fmap}).flat();
        const {ri_emap} = {{}};
        {ri_lst}.forEach({ri_r} => {{
            const {ri_elem} = {r_glob}.document.createElement({self.obf_str("b", r_map)}); {ri_elem}.className = {ri_r};
            {ri_ctn}.appendChild({ri_elem}); {ri_emap}[{ri_r}] = {ri_elem};
        }});
        {r_glob}.document.body.appendChild({ri_ctn});
        await new {r_glob}.Promise({ri_r} => {{ {r_glob}.setTimeout({ri_r}, {num(1000)}); }});
        const {ri_cache} = {{}};
        for (const {ri_cls} of {ri_lst}) {{
            const {ri_elem} = {ri_emap}[{ri_cls}]; const {ri_style} = {r_glob}.getComputedStyle({ri_elem}); const {ri_zindex} = parseInt({ri_style}.zIndex);
            let {ri_val} = "";
            if ({ri_zindex} === {num(20)}) {{ {ri_val} += {r_glob}.String.fromCharCode(parseInt({ri_style}.paddingTop), parseInt({ri_style}.paddingRight), parseInt({ri_style}.paddingBottom), parseInt({ri_style}.paddingLeft)).substring({num(0)}, parseInt({ri_style}.width)); }}
            else if ({ri_zindex} === {num(40)}) {{ const {ri_match} = {ri_style}.backgroundImage.match(/from (.*?)deg/); {ri_val} = {r_glob}.String.fromCharCode({ri_match} ? {r_glob}.Math.round({r_glob}.parseFloat({ri_match}[1])) : {num(0)}); }}
            else if ({ri_zindex} === {num(10)}) {{ {ri_val} = {r_glob}.String.fromCharCode(parseInt({ri_style}.fontSize)); }} 
            else if ({ri_zindex} === {num(30)}) {{ {ri_val} = {r_glob}.String.fromCharCode(parseInt({ri_style}.marginTop)); }} 
            else if ({ri_zindex} === {num(35)}) {{ {ri_val} = {r_glob}.String.fromCharCode(parseInt({ri_style}.order)); }}
            {ri_cache}[{ri_cls}] = {ri_val};
        }}
        for (const {ri_key} in {ri_fmap}) {{ {r_map}[{ri_key}] = {ri_fmap}[{ri_key}].map({ri_cls} => {ri_cache}[{ri_cls}]).join(''); }}
        {r_glob}.document.body.removeChild({ri_ctn});
    }};
    {stego_logic}
    if (!{r_glob}.document.body) await new {r_glob}.Promise({ri_r} => {{ {r_glob}.onload = {ri_r}; }});
    await {r_res_fn}({json.dumps(self.string_lookup)});
    {stego_call}
    try {{ 
{obf_user} 
    }} catch({ri_err}) {{ }}
}})();"""
        
        with open(os.path.join(output_dir, "obfuscated.js"), "w") as f: f.write(loader)
        with open(os.path.join(output_dir, "styles.css"), "w") as f: f.write("b {{ display: block; height: 1px; opacity: 0.01; position: absolute; }}\n" + "\n".join(self.css_rules))
        with open(os.path.join(output_dir, "index.html"), "w") as f: f.write('<!DOCTYPE html><html><head><title>PoC</title><link rel="stylesheet" href="styles.css"></head><body><script src="obfuscated.js"></script></body></html>')
        print(f"[+] Build Complete. Project saved in: ./{base_name}/")