import torch

class corner_box:
    # Corner instantiation
    def __init__(self, x1: float, x2: float, y1: float, y2: float, class_num: int, probability: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.class_num = class_num
        self.probability = probability
    
    # Allows for conversion to midpoint-type boxes
    def convert_to_midpoint(self):
        x = self.x1 + (self.x2 - self.x1) / 2
        y = self.y1 + (self.y2 - self.y1) / 2
        width = self.x2 - self.x1
        height = self.y2 - self.y1

        return midpoint_box(x, y, width, height, self.class_num, self.probability)

class midpoint_box:
    # midpoint and width instantiation
    def __init__(self, x: float, y: float, width: float, height: float, class_num: int, probability: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.class_num = class_num
        self.probability = probability
    
    # Allows for conversion to corner-type boxes
    def convert_to_corner(self):
        x1 = self.x - (self.width / 2)
        y1 = self.y - (self.height / 2) 

        x2 = self.x + (self.width / 2)
        y2 = self.y + (self.height / 2)

        return corner_box(x1, y1, x2, y2, self.class_num, self.probability)

def intersection_over_union(box1, box2):
    # converts non-corner boxes to corner boxes
    if (isinstance(box1, midpoint_box)):
        box1 = box1.convert_to_corner()
    if (isinstance(box2, midpoint_box)):
        box2 = box2.convert_to_corner()
    
    # corner calculations
    x1 = torch.max(box1.x1, box2.x1)
    y1 = torch.max(box1.y1, box2.y1)

    x2 = torch.min(box1.x2, box2.x2)
    y2 = torch.min(box1.y2, box2.y2)

    # Clamp of 0 helps with edge cases of non-intersection
    intersection = abs((y2 - y1).clamp(0) * (x2 - x1).clamp(0))
    union = (abs((box1.y2 - box1.y1) * (box1.x2 - box1.x1)) + abs((box2.y2 - box2.y1) * (box2.x2 - box2.x1))) - intersection

    return intersection / union