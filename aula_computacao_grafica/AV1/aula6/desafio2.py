import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

class CohenSutherlandClipper:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.clip_rect = None
        self.lines = []
        self.clipped_lines = []
        self.step_lines = []

        self.rect_defined = False
        self.rect_start = None
        self.rect_end = None

        self.drawing_line = False
        self.line_start = None

        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        self.ax.set_title("Clique e arraste para definir região de recorte e desenhar linhas")
        plt.axis([0, 100, 0, 100])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def compute_out_code(self, x, y, xmin, xmax, ymin, ymax):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code

    def cohen_sutherland_clip(self, x0, y0, x1, y1, xmin, xmax, ymin, ymax):
        out_code0 = self.compute_out_code(x0, y0, xmin, xmax, ymin, ymax)
        out_code1 = self.compute_out_code(x1, y1, xmin, xmax, ymin, ymax)
        accept = False
        intersec_pts = []

        while True:
            if not (out_code0 | out_code1):  # ambos dentro
                accept = True
                break
            elif out_code0 & out_code1:  # totalmente fora
                break
            else:
                x, y = 0, 0
                out_code_out = out_code0 if out_code0 else out_code1

                if out_code_out & TOP:
                    x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                    y = ymax
                elif out_code_out & BOTTOM:
                    x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                    y = ymin
                elif out_code_out & RIGHT:
                    y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                    x = xmax
                elif out_code_out & LEFT:
                    y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                    x = xmin

                intersec_pts.append((x, y))

                if out_code_out == out_code0:
                    x0, y0 = x, y
                    out_code0 = self.compute_out_code(x0, y0, xmin, xmax, ymin, ymax)
                else:
                    x1, y1 = x, y
                    out_code1 = self.compute_out_code(x1, y1, xmin, xmax, ymin, ymax)

        if accept:
            return True, x0, y0, x1, y1, intersec_pts
        else:
            return False, None, None, None, None, intersec_pts

    def draw_all(self):
        self.ax.clear()

        # Região de recorte
        if self.rect_defined:
            xmin, xmax = sorted([self.rect_start[0], self.rect_end[0]])
            ymin, ymax = sorted([self.rect_start[1], self.rect_end[1]])
            rect = Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                             edgecolor='green', fill=False, linewidth=2)
            self.ax.add_patch(rect)

        # Linhas originais
        for x0, y0, x1, y1 in self.lines:
            self.ax.add_line(Line2D([x0, x1], [y0, y1], color='red'))

        # Interseções
        for inters in self.step_lines:
            for (x, y) in inters:
                self.ax.plot(x, y, 'bo')  # ponto azul

        # Linhas recortadas
        for x0, y0, x1, y1 in self.clipped_lines:
            self.ax.add_line(Line2D([x0, x1], [y0, y1], color='white'))

        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_facecolor('black')
        self.ax.set_title("Clique e arraste para definir região e desenhar linhas.")
        self.fig.canvas.draw()

    def on_click(self, event):
        if not self.rect_defined:
            self.rect_start = (event.xdata, event.ydata)
        else:
            self.drawing_line = True
            self.line_start = (event.xdata, event.ydata)

    def on_release(self, event):
        if not self.rect_defined:
            self.rect_end = (event.xdata, event.ydata)
            self.rect_defined = True
            self.draw_all()
        elif self.drawing_line:
            self.drawing_line = False
            x0, y0 = self.line_start
            x1, y1 = event.xdata, event.ydata
            self.lines.append((x0, y0, x1, y1))

            xmin, xmax = sorted([self.rect_start[0], self.rect_end[0]])
            ymin, ymax = sorted([self.rect_start[1], self.rect_end[1]])

            accepted, cx0, cy0, cx1, cy1, inters = self.cohen_sutherland_clip(x0, y0, x1, y1, xmin, xmax, ymin, ymax)
            self.step_lines.append(inters)
            if accepted:
                self.clipped_lines.append((cx0, cy0, cx1, cy1))
            self.draw_all()

    def on_motion(self, event):
        pass  # opcional: mostrar preview da linha

    def on_key(self, event):
        if not self.rect_defined:
            return

        dx, dy = 0, 0
        if event.key == 'left':
            dx = -1
        elif event.key == 'right':
            dx = 1
        elif event.key == 'up':
            dy = 1
        elif event.key == 'down':
            dy = -1

        if dx != 0 or dy != 0:
            x0, y0 = self.rect_start
            x1, y1 = self.rect_end
            self.rect_start = (x0 + dx, y0 + dy)
            self.rect_end = (x1 + dx, y1 + dy)

            # Atualizar recorte
            self.clipped_lines.clear()
            self.step_lines.clear()
            xmin, xmax = sorted([self.rect_start[0], self.rect_end[0]])
            ymin, ymax = sorted([self.rect_start[1], self.rect_end[1]])
            for x0, y0, x1, y1 in self.lines:
                accepted, cx0, cy0, cx1, cy1, inters = self.cohen_sutherland_clip(x0, y0, x1, y1, xmin, xmax, ymin, ymax)
                self.step_lines.append(inters)
                if accepted:
                    self.clipped_lines.append((cx0, cy0, cx1, cy1))

            self.draw_all()

# Executar
CohenSutherlandClipper()
