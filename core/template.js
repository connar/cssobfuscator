(async () => {{
    const {r_map} = {{}}; 
    {stego_init}
    
    const {r_glob} = (typeof globalThis !== 'undefined') ? globalThis : (typeof window !== 'undefined') ? window : self;
    
    const {r_res_fn} = async ({ri_fmap}) => {{
        const {ri_ctn} = {r_glob}.document.createElement({map_div});
        {ri_ctn}.style.cssText = {map_style};
        
        const {ri_lst} = {r_glob}.Object.values({ri_fmap}).flat();
        const {ri_emap} = {{}};
        
        {ri_lst}.forEach({ri_r} => {{
            const {ri_elem} = {r_glob}.document.createElement({map_b}); 
            {ri_elem}.className = {ri_r};
            {ri_ctn}.appendChild({ri_elem}); 
            {ri_emap}[{ri_r}] = {ri_elem};
        }});
        
        {r_glob}.document.body.appendChild({ri_ctn});
        
        // Wait for CSSOM to stabilize
        await new {r_glob}.Promise({ri_r} => {{ {r_glob}.setTimeout({ri_r}, {num_1000}); }});
        
        const {ri_cache} = {{}};
        for (const {ri_cls} of {ri_lst}) {{
            const {ri_elem} = {ri_emap}[{ri_cls}]; 
            const {ri_style} = {r_glob}.getComputedStyle({ri_elem}); 
            const {ri_zindex} = parseInt({ri_style}.zIndex);
            let {ri_val} = "";
            
            if ({ri_zindex} === {num_20}) {{ 
                {ri_val} += {r_glob}.String.fromCharCode(
                    parseInt({ri_style}.paddingTop), 
                    parseInt({ri_style}.paddingRight), 
                    parseInt({ri_style}.paddingBottom), 
                    parseInt({ri_style}.paddingLeft)
                ).substring(0, parseInt({ri_style}.width)); 
            }}
            else if ({ri_zindex} === {num_40}) {{ 
                const {ri_match} = {ri_style}.backgroundImage.match(/from (.*?)deg/); 
                {ri_val} = {r_glob}.String.fromCharCode({ri_match} ? {r_glob}.Math.round({r_glob}.parseFloat({ri_match}[1])) : 0); 
            }}
            else if ({ri_zindex} === {num_10}) {{ 
                {ri_val} = {r_glob}.String.fromCharCode(parseInt({ri_style}.fontSize)); 
            }} 
            else if ({ri_zindex} === {num_30}) {{ 
                {ri_val} = {r_glob}.String.fromCharCode(parseInt({ri_style}.marginTop)); 
            }} 
            else if ({ri_zindex} === {num_35}) {{ 
                {ri_val} = {r_glob}.String.fromCharCode(parseInt({ri_style}.order)); 
            }}
            
            {ri_cache}[{ri_cls}] = {ri_val};
        }}
        
        for (const {ri_key} in {ri_fmap}) {{ 
            {r_map}[{ri_key}] = {ri_fmap}[{ri_key}].map({ri_cls} => {ri_cache}[{ri_cls}]).join(''); 
        }}
        
        {r_glob}.document.body.removeChild({ri_ctn});
    }};

    {stego_logic}

    if (!{r_glob}.document.body) await new {r_glob}.Promise({ri_r} => {{ {r_glob}.onload = {ri_r}; }});
    
    await {r_res_fn}({string_lookup_json});
    
    {stego_call}

    try {{ 
        {obf_user} 
    }} catch({ri_err}) {{ }}
}})();