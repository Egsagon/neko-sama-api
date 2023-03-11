from tqdm import tqdm

def Bar(desc: str, iter: list, **args) -> tqdm:
    
    return tqdm(iter, bar_format = '{desc} [{percentage:3.0f}%] {bar} [{n_fmt}/{total_fmt}]', ascii = ' -', desc = desc, **args)

# EOF