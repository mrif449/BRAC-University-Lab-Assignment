import math
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables
circles = []
paused = False

def draw_circles():
    for circle in circles:
        draw_circle(circle[0], circle[1], circle[2])

def update_circles():
    global circles
    new_circles = []
    for circle in circles:
        x, y, radius = circle
        radius += 0.001  # Increase radius over time
        if (
                -1.0 < (x - radius) < 1.0
                and -1.0 < (y - radius) < 1.0
                and -1.0 < (x + radius) < 1.0
                and -1.0 < (y + radius) < 1.0
        ):
            new_circles.append((x, y, radius))
    circles = new_circles

def draw_circle(x, y, radius):
    num_segments = 500
    glColor3f(1.0, 0.0, 0.0)  # Set border color to red

    glBegin(GL_LINE_LOOP)

    for i in range(num_segments + 1):
        theta = 2.0 * 3.1415926 * i / num_segments
        dx = radius * math.cos(theta)
        dy = radius * math.sin(theta)

        # Use eight-way symmetry to calculate other points
        glVertex2f(x + dx, y + dy)
        glVertex2f(x - dx, y + dy)
        glVertex2f(x + dx, y - dy)
        glVertex2f(x - dx, y - dy)
        glVertex2f(x + dy, y + dx)
        glVertex2f(x - dy, y + dx)
        glVertex2f(x + dy, y - dx)
        glVertex2f(x - dy, y - dx)

    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Draw the circle with no color inside and a red border
    for circle in circles:
        x, y, radius = circle
        draw_circle(x, y, radius)

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def mouse(button, state, x, y):
    global circles
    if not paused and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = (x / glutGet(GLUT_WINDOW_WIDTH)) * 2.0 - 1.0
        y = 1.0 - (y / glutGet(GLUT_WINDOW_HEIGHT)) * 2.0
        circles.append((x, y, 0.01))  # Initial radius = 0.01


def keyboard(key, x, y):
    global paused
    if key == b' ':
        paused = not paused


def idle():
    if not paused:
        update_circles()
        glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"Growing Circles")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
