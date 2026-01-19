import yaml
import sys
import os

def represent_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, represent_str)

def main():
    base_dir = sys.argv[1]
    layers_path = os.path.join(base_dir, "keymap_layers.yaml")
    config_path = os.path.join(base_dir, "draw_config.yaml")
    output_path = os.path.join(base_dir, "keymap.yaml")

    # Load Layers
    with open(layers_path, 'r') as f:
        data = yaml.safe_load(f)

    # Load Config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Merge Config into Data (Top level)
    if 'draw_config' in config:
        data['draw_config'] = config['draw_config']
    
    # Post-process keys for styling
    destructive_keys = ['Esc', 'Bksp', 'Del', 'Caps', 'ESCAPE', 'BSPACE', 'DELETE', 'CAPSLOCK']
    
    if 'layers' in data:
        for layer_name, rows in data['layers'].items():
            for row in rows:
                for i, key in enumerate(row):
                    # Key can be a string or a dict
                    label = key
                    meta = {}
                    
                    if isinstance(key, dict):
                        label = key.get('t', '')
                        meta = key
                    elif isinstance(key, str):
                        label = key
                        meta = {'t': key}
                        # If we modify it, we must replace the string with the dict
                    
                    # Apply rules
                    # 1. Destructive
                    if label in destructive_keys:
                        meta['type'] = 'destructive'
                        # Ensure we use the object form
                        row[i] = meta
                    
                    # 2. Layer (if it has a hold 'h' that looks like a layer or is explicit)
                    if isinstance(key, dict) and 'h' in key:
                        hold = key['h']
                        # Simple heuristic: if hold starts with L (L1, L2) or matches Nav/Sym/Func etc
                        if str(hold).startswith('L') or str(hold) in ['Sym', 'Nav', 'Func', 'Num', 'Maus']:
                             meta['type'] = 'layer'
                             row[i] = meta

    # Write output
    with open(output_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=None)

if __name__ == "__main__":
    main()
