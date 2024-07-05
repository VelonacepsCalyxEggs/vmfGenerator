import random

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

def createRoom(worlddata, width, length, height, x, y, z, door_width, door_height, isFrontDoor = False, isBackDoor = False, isLeftDoor = False, isRightDoor = False):
    # ensure width and length are positive
    width = abs(width)
    length = abs(length)

    # Check for errors
    if width <= 0 or length <= 0 or height <= 0:
        raise ValueError("Room dimensions must be positive.")
    if door_width <= 0 or door_height <= 0:
        raise ValueError("Door dimensions must be positive.")
    if door_width > width:
        raise ValueError("Door width cannot exceed room width.")
    if door_height > height:
        raise ValueError("Door height cannot exceed room height.")
    if width <= door_width:
        raise ValueError("Room width must be greater than door width.")
    if length <= door_width:
        raise ValueError("Room length must be greater than door width.")


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

    if not isLeftDoor:
        left_wall = makeSolid(new_id(), 16, length, height, x - 16, y, z)
        worlddata['world'][f'solid_{left_wall['id']}'] = left_wall
    else:
        door_wall_left = makeSolid(new_id(), 16, length / 2 - door_width / 2, door_height, x - 16, y, z)
        door_wall_right = makeSolid(new_id(), 16, length / 2 - door_width / 2, door_height, x - 16, y + length / 2 + door_width / 2, z)
        door_wall_top = makeSolid(new_id(), 16, length, height - door_height, x - 16, y, z + door_height)
        door_floor = makeSolid(new_id(), 16, door_width, 16, x - 16, y + length / 2 - door_width / 2, z - 16)
        worlddata['world'][f'solid_{door_wall_left['id']}'] = door_wall_left
        worlddata['world'][f'solid_{door_wall_right['id']}'] = door_wall_right
        worlddata['world'][f'solid_{door_wall_top['id']}'] = door_wall_top
        worlddata['world'][f'solid_{door_floor['id']}'] = door_floor

    if not isRightDoor:
        right_wall = makeSolid(new_id(), 16, length, height, x + width, y, z)
        worlddata['world'][f'solid_{right_wall['id']}'] = right_wall
    else:
        door_wall_left = makeSolid(new_id(), 16, length / 2 - door_width / 2, door_height, x + width, y, z)
        door_wall_right = makeSolid(new_id(), 16, length / 2 - door_width / 2, door_height, x + width, y + length / 2 + door_width / 2, z)
        door_wall_top = makeSolid(new_id(), 16, length, height - door_height, x + width, y, z + door_height)
        door_floor = makeSolid(new_id(), 16, door_width, 16, x + width, y + length / 2 - door_width / 2, z - 16)
        worlddata['world'][f'solid_{door_wall_left['id']}'] = door_wall_left
        worlddata['world'][f'solid_{door_wall_right['id']}'] = door_wall_right
        worlddata['world'][f'solid_{door_wall_top['id']}'] = door_wall_top
        worlddata['world'][f'solid_{door_floor['id']}'] = door_floor

    if not isFrontDoor:
        front_wall = makeSolid(new_id(), width, 16, height, x, y + length, z)
        worlddata['world'][f'solid_{front_wall['id']}'] = front_wall
    else:
        door_wall_left = makeSolid(new_id(), width / 2 - door_width / 2, 16, door_height, x, y + length, z)
        door_wall_right = makeSolid(new_id(), width / 2 - door_width / 2, 16, door_height, x + width / 2 + door_width / 2, y + length, z)
        door_wall_top = makeSolid(new_id(), width, 16, height - door_height, x, y + length, z + door_height)
        door_floor = makeSolid(new_id(), door_width, 16, 16, x + width / 2 - door_width / 2, y + length, z - 16)
        worlddata['world'][f'solid_{door_wall_left['id']}'] = door_wall_left
        worlddata['world'][f'solid_{door_wall_right['id']}'] = door_wall_right
        worlddata['world'][f'solid_{door_wall_top['id']}'] = door_wall_top
        worlddata['world'][f'solid_{door_floor['id']}'] = door_floor

    if not isBackDoor:
        back_wall = makeSolid(new_id(), width, 16, height, x, y - 16, z)
        worlddata['world'][f'solid_{back_wall['id']}'] = back_wall
    else:
        door_wall_left = makeSolid(new_id(), width / 2 - door_width / 2, 16, door_height, x, y - 16, z)
        door_wall_right = makeSolid(new_id(), width / 2 - door_width / 2, 16, door_height, x + width / 2 + door_width / 2, y - 16, z)
        door_wall_top = makeSolid(new_id(), width, 16, height - door_height, x, y - 16, z + door_height)
        door_floor = makeSolid(new_id(), door_width, 16, 16, x + width / 2 - door_width / 2, y - 16, z - 16)
        worlddata['world'][f'solid_{door_wall_left['id']}'] = door_wall_left
        worlddata['world'][f'solid_{door_wall_right['id']}'] = door_wall_right
        worlddata['world'][f'solid_{door_wall_top['id']}'] = door_wall_top
        worlddata['world'][f'solid_{door_floor['id']}'] = door_floor
    # add the solids to the world data using the new IDs
    # there will be a better way to do it in the future...
    worlddata['world'][f'solid_{floor['id']}'] = floor
    worlddata['world'][f'solid_{ceiling['id']}'] = ceiling


    # Add room coordinates and door data to the dictionary
    roomId = len(room_dict) + 1
    room_dict[roomId] = {
        'coords': {
            'width': width,
            'length': length,
            'height': height,
            'x': x,
            'y': y,
            'z': z,
            'volume': width * length * height
        },
        'doors': {
            'front': isFrontDoor,
            'back': isBackDoor,
            'left': isLeftDoor,
            'right': isRightDoor,
            'door_width': door_width,
            'door_height': door_height
        }
    }

    return worlddata

def createCorridor(worlddata, width, length, height, x, y, z, isFrontDoor, isBackDoor, isLeftDoor, isRightDoor):
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

    if not isLeftDoor:
        left_wall = makeSolid(new_id(), 16, length, height, x - 16, y, z)
        worlddata['world'][f'solid_{left_wall['id']}'] = left_wall
        print('Created Left Wall')
    else:
        1

    if not isRightDoor:
        right_wall = makeSolid(new_id(), 16, length, height, x + width, y, z)
        worlddata['world'][f'solid_{right_wall['id']}'] = right_wall
        print('Created Right Wall')
    else:
        1

    if not isFrontDoor:
        front_wall = makeSolid(new_id(), width, 16, height, x, y + length, z)
        worlddata['world'][f'solid_{front_wall['id']}'] = front_wall
        print('Created Front Wall')
    else:
        1

    if not isBackDoor:
        back_wall = makeSolid(new_id(), width, 16, height, x, y - 16, z)
        worlddata['world'][f'solid_{back_wall['id']}'] = back_wall
        print('Created Back Wall')
    else:
        1
    # add the solids to the world data using the new IDs
    # there will be a better way to do it in the future...
    worlddata['world'][f'solid_{floor['id']}'] = floor
    worlddata['world'][f'solid_{ceiling['id']}'] = ceiling
   

    return worlddata

size_list = [32, 64, 96, 128, 192, 256, 384, 512, 1024, 2048]

room_dict = {}
coords = 0
y = 0
corridor_length = 1024
for i in range(0, 5):
    try:
        coords += 2048
        data = createRoom(data, size_list[random.randint(0, len(size_list) - 1)], size_list[random.randint(0, len(size_list) - 1)], size_list[random.randint(0, len(size_list) - 1)],
                           coords, 0, 0,
                             96, 96,
                               True, True, True, True)
    except:
        print('Room failed check.')
        y += 1
print(f'{y} out of {i + 1} rooms, had failed room check.')

for roomId, room in room_dict.items():
    if room['doors']['front']:
       data = createCorridor(data, room['doors']['door_width'] + 32, corridor_length, room['doors']['door_height'] + 32, room['coords']['x'] + room['coords']['width'] / 2 - room['doors']['door_width'] / 2 - 16, room['coords']['y'] + room['coords']['length'] + 16, room['coords']['z'], True, True, False, False)
    if room['doors']['back']:
        data = createCorridor(data, room['doors']['door_width'] + 32, corridor_length, room['doors']['door_height'] + 32, room['coords']['x'] + room['coords']['width'] / 2 - room['doors']['door_width'] / 2 - 16, room['coords']['y'] - corridor_length - 16, room['coords']['z'], True, True, False, False)
    if room['doors']['left']:
        data = createCorridor(data, corridor_length, room['doors']['door_width'] + 32, room['doors']['door_height'] + 32, room['coords']['x'] + room['coords']['width'] + 16 , room['coords']['y'] + room['coords']['length'] / 2 - room['doors']['door_width'] / 2 - 16, room['coords']['z'], False, False, True, True)
    if room['doors']['right']:
        data = createCorridor(data, corridor_length, room['doors']['door_width'] + 32, room['doors']['door_height'] + 32, room['coords']['x'] - corridor_length - 16 , room['coords']['y'] + room['coords']['length'] / 2 - room['doors']['door_width'] / 2 - 16, room['coords']['z'], False, False, True, True)
#data = createCorridor(data, 128, 128, 96, 128, 128, 0, 96, 96, True, False, False, True)

write_dict_to_file(data, file_path)
print('Finished')