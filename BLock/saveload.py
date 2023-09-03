import json


def get_points(dict):
    l = []
    for name in dict:
        if name[0:7] == "socket_":
            socket = [
                name,
                dict[name].connectpoint_id,
                dict[name].my_con_points_ids,
                dict[name].id,
                dict[name].point_type,
                dict[name].value,
            ]
            l.append(socket)
    return l


def save(file_name: list, blocks: list):
    arr = []
    for block in blocks:
        d = block.__dict__
        data = {
            "name": block.bone.name,
            "id": block.bone.id,
            "pos": block.bone.pos,
            "points": get_points(d),
        }
        arr.append(data)

    with open("saves\\" + file_name, "w") as f:
        json.dump(arr, f, indent=4)
        f.write("\n")
