def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    dictionary = {}
    stack = [dictionary]
    current_dict = dictionary
    key = None
    unique_counter = {}

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == '{':
            if key:
                base_key = key
                count = unique_counter.get(base_key, 0)
                unique_key = f"{base_key}_{count}" if count else base_key
                unique_counter[base_key] = count + 1

                new_dict = {}
                current_dict[unique_key] = new_dict
                stack.append(new_dict)
                current_dict = new_dict
                key = None
        elif stripped_line == '}':
            stack.pop()
            if stack:
                current_dict = stack[-1]
        else:
            parts = stripped_line.split(' ', 1)
            if len(parts) == 2:
                key, value = parts
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                #  check if the key exists and is a list, append to it bruh
                if key in current_dict:
                    if isinstance(current_dict[key], list):
                        current_dict[key].append(value)
                    else:
                        current_dict[key] = [current_dict[key], value]
                else:
                    current_dict[key] = value
            else:
                key = parts[0]

    return dictionary

def makeSolid(id, width, length, height, x = 0, y = 0, z = 0):
    x1, y1, z1 = 0 + x, 0 + y, 0 + z
    x2, y2, z2 = width + x, length + y, height + z
    if width < 0:
        x1, x2 = x2, x1
    if length < 0:
        y1, y2 = y2, y1
    if height < 0:
        z1, z2 = z2, z1
    solid = {
        "id": id,
        "side_1": {
            "id": id + 1,
            "plane": f"({x1} {y2} {z2}) ({x2} {y2} {z2}) ({x2} {y1} {z2})",
            "material": "TOOLS/TOOLSNODRAW",
            "uaxis": "[1 0 0 0] 0.25",
            "vaxis": "[0 1 0 0] 0.25",
            "rotation": "0",
            "lightmapscale": "16",
            "smoothing_groups": "0"
        },
        "side_2": {
            "id": id + 2,
            "plane": f"({x1} {y1} {z1}) ({x2} {y1} {z1}) ({x2} {y2} {z1})",
            "material": "TOOLS/TOOLSNODRAW",
            "uaxis": "[1 0 0 0] 0.25",
            "vaxis": "[0 1 0 0] 0.25",
            "rotation": "0",
            "lightmapscale": "16",
            "smoothing_groups": "0"
        },
        "side_3": {
            "id": id + 3,
            "plane": f"({x1} {y2} {z2}) ({x1} {y1} {z2}) ({x1} {y1} {z1})",
            "material": "TOOLS/TOOLSNODRAW",
            "uaxis": "[1 0 0 0] 0.25",
            "vaxis": "[0 1 0 0] 0.25",
            "rotation": "0",
            "lightmapscale": "16",
            "smoothing_groups": "0"
        },
        "side_4": {
            "id": id + 4,
            "plane": f"({x2} {y2} {z1}) ({x2} {y1} {z1}) ({x2} {y1} {z2})",
            "material": "TOOLS/TOOLSNODRAW",
            "uaxis": "[1 0 0 0] 0.25",
            "vaxis": "[0 1 0 0] 0.25",
            "rotation": "0",
            "lightmapscale": "16",
            "smoothing_groups": "0"
        },
        "side_5": {
            "id": id + 5,
            "plane": f"({x2} {y2} {z2}) ({x1} {y2} {z2}) ({x1} {y2} {z1})",
            "material": "TOOLS/TOOLSNODRAW",
            "uaxis": "[1 0 0 0] 0.25",
            "vaxis": "[0 1 0 0] 0.25",
            "rotation": "0",
            "lightmapscale": "16",
            "smoothing_groups": "0"
        },
        "side_6": {
            "id": id + 6,
            "plane": f"({x2} {y1} {z1}) ({x1} {y1} {z1}) ({x1} {y1} {z2})",
            "material": "TOOLS/TOOLSNODRAW",
            "uaxis": "[1 0 0 0] 0.25",
            "vaxis": "[0 1 0 0] 0.25",
            "rotation": "0",
            "lightmapscale": "16",
            "smoothing_groups": "0"
        },
        "editor": {
            "color": "0 252 237",
            "visgroupshown": "1",
            "visgroupautoshown": "1"
        }
    }
    return solid





def format_dict(d, indent=0):
    lines = []
    for key, value in d.items():
        if isinstance(value, dict):
            # remove unique identifiers from keys
            key = key.split('_')[0] if '_' in key else key
            lines.append('\t' * indent + str(key))
            lines.append('\t' * indent + '{')
            lines.extend(format_dict(value, indent + 1))
            lines.append('\t' * indent + '}')
        elif isinstance(value, list):
            # handle list of items (e.g., vertices)
            lines.append('\t' * indent + key)
            lines.append('\t' * indent + '{')
            for item in value:
                lines.append('\t' * (indent + 1) + f'"v" "{item}"')
            lines.append('\t' * indent + '}')
        else:
            # escape double quotes within the string, huynya btw
            escaped_value = str(value).replace('"', '\\"')
            lines.append('\t' * indent + f'{key} "{escaped_value}"')
    return lines

def write_dict_to_file(dictionary, file_path):
    lines = format_dict(dictionary)
    with open(file_path, 'w') as file:
        file.write('\n'.join(lines))

file_path = 'scripted.vmf'
data = parse_file(file_path)

#id, width, length, height, x, y, z
#solid = makeSolid(3, 128, 128, 128, 0, 0, 0)

def createRoom(worlddata, width, length, height, x, y, z):
    # ensure width and length are positive
    width = abs(width)
    length = abs(length)

    # find the highest existing solid ID
    highest_id = max(
        [int(key.split('_')[1]) for key in worlddata['world'].keys() if 'solid' in key and len(key.split('_')) > 1],
        default=0
    )

    # helper function to generate a new solid IDs
    def new_id():
        nonlocal highest_id
        highest_id += 1
        return highest_id

    # create the floor and ceiling at the specified coordinates
    floor = makeSolid(new_id(), width, length, 16, x, y, z - 16)
    ceiling = makeSolid(new_id(), width, length, 16, x, y, z + height)

    # create the walls with the correct dimensions at the specified coordinates
    left_wall = makeSolid(new_id(), 16, length, height, x - 16, y, z)
    right_wall = makeSolid(new_id(), 16, length, height, x + width, y, z)
    back_wall = makeSolid(new_id(), width, 16, height, x, y - 16, z)
    front_wall = makeSolid(new_id(), width, 16, height, x, y + length, z)

    # add the solids to the world data using the new IDs
    # there will be a better way to do it in the future...
    worlddata['world'][f'solid_{floor}'] = floor
    worlddata['world'][f'solid_{ceiling}'] = ceiling
    worlddata['world'][f'solid_{left_wall}'] = left_wall
    worlddata['world'][f'solid_{right_wall}'] = right_wall
    worlddata['world'][f'solid_{back_wall}'] = back_wall
    worlddata['world'][f'solid_{front_wall}'] = front_wall

    return worlddata

data = createRoom(data, 256, 256, 192, -128, -128, 0)

write_dict_to_file(data, file_path)
print('Finished')