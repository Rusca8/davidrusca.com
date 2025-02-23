
function apply_analysis_to_text(text_to_paint, blocks_to_paint){
    /* paints the analysis highlighting by applying class-ed spans */
    let text = [];
    for(let i=0; i<text_to_paint.length+1; i++){
        // pass for ends
        for(let [key, val] of Object.entries(blocks_to_paint)){
            for(let [s, e] of val){
                if(e == i){
                    text.push('</span>');
                }
            }
        }
        // pass for beginnings
        let afterblocks = [];
        for(let [key, val] of Object.entries(blocks_to_paint)){
            for(let [s, e] of val){
                if(s==i){
                    // check padding
                    let pl = "";
                    if(i > 0 && !" ,.:;\"'?!".includes(text_to_paint[i-1])){
                        pl = " pl-0";
                    }
                    let pr = "";
                    if(!" ,.:;\"'?!".includes(text_to_paint[e]) && text_to_paint[e] != undefined){
                        pr = " pr-0";
                    }
                    if(key == "hid"){
                        afterblocks.push('<span class="eh-' + key + pl + pr + '">');
                    }else{
                        text.push('<span class="eh-' + key + pl + pr + '">');
                    }
                }
            }
        }
        // held beginnings execute
        for(let ab_text of afterblocks){
            text.push(ab_text);
        }
        // the char
        text.push(text_to_paint[i]);
    }
    return text.join("");
}

function swap_quotes(text, temp="❆"){
    return text.replaceAll('"', temp).replaceAll("'", '"').replaceAll(temp, "'");
}

function fix_bad_quotes_dict(dict){
    // gets a (jinja) dict with bad JSON quotes (i.e. ['things', 'things']) and reparses it to proper quotes.
    if(!dict.includes("[")){
        return "";
    }
    let text = JSON.stringify(dict).slice(1, -1);
    text = swap_quotes(text);
    return JSON.parse(text);
}

function render_analyses(){
    /* renders all analyses picking the data from data-blocks attribute */
    console.log("Render analyses...");
    for(let el of document.querySelectorAll("[data-blocks]")){
                                             // resulta que a JSON.parse no li agraden les cometes simples.
        el.innerHTML = apply_analysis_to_text(el.dataset.text, JSON.parse(swap_quotes(el.dataset.blocks)));
    }
}

function render_analysis(el){
    /* renders this element's analysis */
    el.innerHTML = apply_analysis_to_text(el.dataset.text, JSON.parse(swap_quotes(el.dataset.blocks)));
}