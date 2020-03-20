from tkinter import Tk, Canvas, Button, filedialog, Spinbox
import math

windowX = 800
windowY = 800

print("yes")

class vec4:
    def __init__(self, X, Y, Z, M):
        self.X = float(X)
        self.Y = float(Y)
        self.Z = float(Z)
        self.M = float(M)

    def x(self):
        return windowX / 2 + (float(self.X) * windowX / 4)

    def y(self):
        return windowY / 2 - (float(self.Y) * windowY / 4)

class mat4:
    def __init__(self, m):
        if len(m) != 4:
            raise Exception("Wrong size of matrix")
            for f in m:
                if len(f) != 4:
                    raise Exception("Wrong size of matrix")

        self.m = m

def multiply(a, b):

    if not isinstance(a, mat4):
        raise Exception("Wrong type matrix")

    m = []

    if isinstance(b, mat4):
        for i in range(4):
            m += [[0, 0, 0, 0]]
            for j in range(4):
                for k in range(4):
                    m[i][j] += a.m[i][k] * b.m[k][j]

        return mat4(m)

    if isinstance(b, vec4):

        x = a.m[0][0] * b.X + a.m[0][1] * b.Y + a.m[0][2] * b.Z + a.m[0][3] * b.M
        y = a.m[1][0] * b.X + a.m[1][1] * b.Y + a.m[1][2] * b.Z + a.m[1][3] * b.M
        z = a.m[2][0] * b.X + a.m[2][1] * b.Y + a.m[2][2] * b.Z + a.m[2][3] * b.M
        m = a.m[3][0] * b.X + a.m[3][1] * b.Y + a.m[3][2] * b.Z + a.m[3][3] * b.M

        return vec4(x, y, z, m)

light = vec4(-1, -1, -1, 0)

class indexedFace:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def drawFace(self):

        if (((v[self.v1].X * v[self.v2].Y) - (v[self.v1].Y * v[self.v2].X)) +
            ((v[self.v2].X * v[self.v3].Y) - (v[self.v2].Y * v[self.v3].X)) +
            ((v[self.v3].X * v[self.v1].Y) - (v[self.v3].Y * v[self.v1].X))) > 0:

            U = vec4(v[self.v2].X - v[self.v1].X, v[self.v2].Y - v[self.v1].Y, v[self.v2].Z - v[self.v1].Z, 0)
            V = vec4(v[self.v3].X - v[self.v1].X, v[self.v3].Y - v[self.v1].Y, v[self.v3].Z - v[self.v1].Z, 0)

            Normal = vec4((U.Y * V.Z) - (U.Z * V.Y), (U.Z * V.X) - (U.X * V.Z), (U.X * V.Y) - (U.Y * V.X), 0)

            n = (Normal.X**2 + Normal.Y**2 + Normal.Z**2)**(1/2)
            l = (light.X**2 + light.Y**2 + light.Z**2)**(1/2)

            c = (Normal.X * light.X) + (Normal.Y * light.Y) + (Normal.Z * light.Z)

            cos = c / (n * l)

            cos = 1 - ((cos + 1) / 2)

            color = hex(int(cos * 16 * 16 * 16))[2:]

            color = (3 - len(color)) * '0' + color
        
            canvas.create_polygon([v[self.v1].x(), v[self.v1].y(), v[self.v2].x(), v[self.v2].y(),
                                   v[self.v3].x(), v[self.v3].y()],fill='#' + color * 3)

    def drawMesh(self):
        
        canvas.create_line(v[self.v1].x(), v[self.v1].y(), v[self.v2].x(), v[self.v2].y())
        canvas.create_line(v[self.v1].x(), v[self.v1].y(), v[self.v3].x(), v[self.v3].y())
        canvas.create_line(v[self.v3].x(), v[self.v3].y(), v[self.v2].x(), v[self.v2].y())


root = Tk()
canvas = Canvas(root, width=windowX + 250, height=windowY)
canvas.pack()

canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

v = []
vo = []
faces = []

def load():

    canvas.delete("all")
    canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

    global v, vo, faces

    v = []

    faces = []

    file = filedialog.askopenfile(mode='r')

    riadok = file.readline()

    while riadok != "":

        data = riadok.split(' ')
        data[-1] = data[-1][:-1]

        if data[0] == 'v':
            v += [vec4(data[1], data[2], data[3], 1)]

        if data[0] == 'f':

            faces += [indexedFace(int(data[1]) - 1, int(data[2]) - 1, int(data[3]) - 1)]

            faces[-1].drawFace()

        riadok = file.readline()

    vo = []

    for f in v:
        vo += [vec4(f.X, f.Y, f.Z, f.M)]

    file.close()

load = Button(root, text ="Load", command = load)
load.place(x = windowX + 20, y = 20)

def reset():

    global v, vo

    canvas.delete("all")
    canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

    v = []

    for f in vo:
        v += [vec4(f.X, f.Y, f.Z, f.M)]

    for f in faces:
        f.drawFace()

reset = Button(root, text ="Reset", command = reset)
reset.place(x = windowX + 100, y = 20)

lx = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
lx.place(x = windowX + 95, y = 250)
ly = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
ly.place(x = windowX + 140, y = 250)
lz = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
lz.place(x = windowX + 185, y = 250)

def setLight():

    canvas.delete("all")
    canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

    global light
    light = vec4(float(lx.get()), float(ly.get()), float(lz.get()), 0)

    for f in faces:
        f.drawFace()

setLightDir = Button(root, text ="Set light direction", command = setLight)
setLightDir.place(x = windowX + 100, y = 280)

tx = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
tx.place(x = windowX + 95, y = 165)
ty = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
ty.place(x = windowX + 140, y = 165)
tz = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
tz.place(x = windowX + 185, y = 165)

def trasnlate():

    canvas.delete("all")
    canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

    for i in range(len(v)):
        v[i] = multiply(mat4([[1, 0, 0, float(tx.get())],
                      [0, 1, 0, float(ty.get())],
                      [0, 0, 1, float(tz.get())],
                      [0, 0, 0, 1]]), v[i])

    for f in faces:
        f.drawFace()

trasnlate = Button(root, text ="Trasnlate", command = trasnlate)
trasnlate.place(x = windowX + 5, y = 160)

sx = Spinbox(root, from_ = 0, to = 2, increment = 0.1, width = 3)
sx.insert(1, "1")
sx.place(x = windowX + 85, y = 85)
sy = Spinbox(root, from_ = 0, to = 2, increment = 0.1, width = 3)
sy.insert(1, "1")
sy.place(x = windowX + 130, y = 85)
sz = Spinbox(root, from_ = 0, to = 2, increment = 0.1, width = 3)
sz.insert(1, "1")
sz.place(x = windowX + 175, y = 85)

def scale():

    canvas.delete("all")
    canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

    for i in range(len(v)):
        v[i] = multiply(mat4([[float(sx.get()), 0, 0, 0],
                      [0, float(sy.get()), 0, 0],
                      [0, 0, float(sz.get()), 0],
                      [0, 0, 0, 1]]), v[i])

    for f in faces:
        f.drawFace()

scale = Button(root, text ="Scale", command = scale)
scale.place(x = windowX + 20, y = 80)

rx = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
rx.place(x = windowX + 85, y = 125)
ry = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
ry.place(x = windowX + 130, y = 125)
rz = Spinbox(root, from_ = -1, to = 1, increment = 0.1, width = 3)
rz.place(x = windowX + 175, y = 125)

def rotate():

    canvas.delete("all")
    canvas.create_rectangle(windowX, 0, windowX + 250, windowY, outline="#000", fill="#000")

    rotationX = mat4([[1, 0, 0, 0],
                      [0, math.cos(float(rx.get())), -math.sin(float(rx.get())), 0],
                      [0, math.sin(float(rx.get())), math.cos(float(rx.get())), 0],
                      [0, 0, 0, 1]])

    rotationY = mat4([[math.cos(float(ry.get())), 0, math.sin(float(ry.get())), 0],
                      [0, 1, 0, 0],
                      [-math.sin(float(ry.get())), 0, math.cos(float(ry.get())), 0],
                      [0, 0, 0, 1]])

    rotationZ = mat4([[math.cos(float(rz.get())), -math.sin(float(rz.get())), 0, 0],
                      [math.sin(float(rz.get())), math.cos(float(rz.get())), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    rotation = multiply(multiply(rotationX, rotationY), rotationZ)

    for i in range(len(v)):
        v[i] = multiply(rotation, v[i])

    for f in faces:
        f.drawFace()

rotate = Button(root, text ="Rotate", command = rotate)
rotate.place(x = windowX + 10, y = 120)

root.mainloop()
