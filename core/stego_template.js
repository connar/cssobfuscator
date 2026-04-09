const {r_stego_fn} = () => new {r_glob}.Promise({ri_res} => {{
    const {ri_img} = new {r_glob}.Image(); 
    {ri_img}.src = {map_png_path}; 
    {ri_img}.crossOrigin = {map_anon};
    
    {ri_img}.onload = () => {{
        const {ri_canv} = {r_glob}.document.createElement({map_canvas}); 
        const {ri_ctx} = {ri_canv}.getContext({map_2d});
        
        {ri_canv}.width = {ri_img}.width; 
        {ri_canv}.height = {ri_img}.height; 
        {ri_ctx}.drawImage({ri_img}, 0, 0);
        
        const {ri_data} = {ri_ctx}.getImageData(0, 0, {ri_img}.width, {ri_img}.height).data;
        let {ri_out} = "";
        
        for(let {ri_j}=0; {ri_j}<{ri_data}.length; {ri_j}+={num_4}) {{
            let {ri_bits} = "";
            for(let {ri_b}=0; {ri_b}<{num_8}; {ri_b}++) {{ 
                let {ri_idx} = {ri_j} + ({ri_b} * {num_4}) + {num_3};
                if({ri_idx} < {ri_data}.length) {{
                    {ri_bits} += ({ri_data}[{ri_idx}] & 1); 
                }}
            }}
            let {ri_cc} = parseInt({ri_bits}, 2) ^ {ri_key_var};
            if({ri_cc} === 0) break;
            {ri_out} += {r_glob}.String.fromCharCode({ri_cc});
            {ri_j} += {num_28};
        }}
        {ri_res}({ri_out});
    }};
    {ri_img}.onerror = () => {ri_res}("");
}});