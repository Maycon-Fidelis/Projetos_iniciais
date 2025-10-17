import pygame

class Polygon:
    def __init__(self, id, name, surface, vertices, zBuffer, color):

        if not isinstance(id, int):
            raise TypeError("id type need to be a int type.")
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(surface, pygame.Surface):
            raise TypeError("Display type need to be a pygame.Surface object.")
        if not (isinstance(vertices, list) and all(isinstance(v, tuple) for v in vertices)):
            raise TypeError("Vertices need to be a list of tuples.")
        if not(isinstance(zBuffer, tuple)):
            raise TypeError("ZBuffer must to be a tuple")
        if not (isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) for c in color)):
            raise TypeError("Color needs to be a tuple with exactly 3 elements (RGB).")


        self._id = id
        self._surface = surface
        self._vertices = vertices
        self._zBuffer = zBuffer
        self._edges = define_edge(self._vertices)
        self._color = color
        self._y_min, self._y_max = define_vertical_limits(self._vertices)

    def draw(self):

        start, end = self._y_min, self._y_max

        for y in range(start, end + 1):
           
            intersection_values = []
            intersection_pair = []

            for (xA, yA), (xB, yB) in self._edges:

                if((yA <= y < yB) or (yB <= y < yA)):
                    x = xA + (((y - yA) * (xB - xA))/(yB - yA))
                    intersection_values.append(round(x))
            
            intersection_values.sort()

            for i in range(0, len(intersection_values) - 1, 2):
                intersection_pair.append((intersection_values[i], intersection_values[i+1]))    

            for x1, x2 in intersection_pair:
                while x1 < x2:
                    
                    if(self._zBuffer[1] <= self._zBuffer[0][x1][y]):
                        self._surface.set_at((x1, y), self._color)
                        self._zBuffer[0][x1][y] = self._zBuffer[1]
                    x1+=1


               
def define_vertical_limits(vertices):
    y_points = []
    for y in vertices:
        y_points.append(y[1])
    
    return min(y_points), max(y_points)

def define_edge(vertices):
        edges = []
        for i in range(len(vertices)):
            if i != len(vertices) - 1:
                edges.append((vertices[i], vertices[i+1]))
            else:
                edges.append((vertices[i], vertices[0]))
        return edges