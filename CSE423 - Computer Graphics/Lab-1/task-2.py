from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

# Initialize global variables
points = []
frozen = False
speed = 0.01
blinking = False
blink_interval = 0.8
original_colors = []

# Initialize window dimensions
window_width = 800
window_height = 600

# Initialize colors
colors = [
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Cyan
]

def draw_point(x, y, color):
    glColor3f(color[0], color[1], color[2])
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for point in points:
        draw_point(*point)
    glutSwapBuffers()

def random_direction():
    return random.choice([-1, 1]), random.choice([-1, 1])

def mouse_click(button, state, x, y):
    global points, blinking, original_colors, frozen
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not frozen:
        points.append([(x / window_width) * 2 - 1, -(y / window_height) * 2 + 1, random.choice(colors)])
        original_colors.append(points[-1][2])
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not frozen:
        blinking = not blinking
        if blinking:
            glutTimerFunc(int(blink_interval * 500), blink_points, 0)

def blink_points(value):
    global points, blinking, original_colors
    if blinking and not frozen:
        for i, point in enumerate(points):
            if point[2] == (0, 0, 0):  # If color is black, revert to original color
                point[2] = original_colors[i]
            else:  # Otherwise, set color to black
                original_colors[i] = point[2]  # Store original color
                point[2] = (0, 0, 0)

        glutPostRedisplay()
        glutTimerFunc(int(blink_interval * 500), blink_points, 0)

def keyboard(key, x, y):
    global speed, frozen
    if key == b'\x1b':
        sys.exit(0)
    elif key == b' ':
        frozen = not frozen
    elif key == b'\x1b[A' and not frozen:  # Up arrow key
        speed += 0.02
    elif key == b'\x1b[B' and not frozen:  # Down arrow key
        speed = max(speed - 0.001, 0.2) 

def update_points(value):
    global points
    if not frozen:
        new_points = []
        for point in points:
            x, y, color = point
            x += random.uniform(-1, 1) * speed
            y += random.uniform(-1, 1) * speed
            if abs(x) > 1 or abs(y) > 1:
                x, y = -x, -y  # Move to the opposite direction
            new_points.append([x, y, color])
        points = new_points

    glutPostRedisplay()
    glutTimerFunc(16, update_points, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b'OpenGL Box')
    glutDisplayFunc(draw)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(0, update_points, 0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1, 1, -1, 1)
    glutMainLoop()

if __name__ == "__main__":
    main()
