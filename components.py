
class NodeData:
    counter = 0

    def __init__(self, key: int = counter, info: str = "", weight: float = 0.0, pos=None, tag: float = -1):
        self.tag = tag
        if key != NodeData.counter:
            self.key = key
        else:
            self.key = NodeData.counter
            NodeData.counter += 1
        self.info = info
        self.weight = weight
        if pos is not None:
            self.pos = GeoLocation(pos)  # a tuple himself
        else:
            self.pos = None

    def __repr__(self):
        return "#{}".format(self.key)


class EdgeData:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight
        self.info = ""

    def __repr__(self):
        return ""
        #  {} ->{} \n".format(self.src, self.dest)"


class GeoLocation:
    def __init__(self, pos: tuple = (0, 0, 0)):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    def __repr__(self):
        if self.pos is not None:
            return "{},{},{}".format(self.x, self.y, self.z)
        else:
            return "None"
