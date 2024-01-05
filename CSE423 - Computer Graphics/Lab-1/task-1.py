from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_KEY_LEFT, GLUT_KEY_RIGHT


import random


def draw_rain():
    global left_arrow_pressed, right_arrow_pressed

    glLineWidth(1.0)
    glBegin(GL_LINES)
    num_lines = 500
    spacing = 20.0  # Adjust the spacing as needed
    for i in range(num_lines):
        x = i * spacing / num_lines - 10.0  # Distribute evenly between -10 and 10
        y = random.uniform(-1, 4)

        # Apply bending based on arrow key input
        if left_arrow_pressed:
            angle = 1
        elif right_arrow_pressed:
            angle = -1
        else:
            angle = 0.0

        top_point_y = y  # Keep the top point y-coordinate unchanged
        bottom_point_y = y - 0.3  # Adjust the y-coordinate of the bottom point

        glVertex3f(x, top_point_y, 0.0)
        glVertex3f(x + angle, bottom_point_y, 0.0)  # Adjusted bottom point
    glEnd()

def drawRoof():
    if lines_white:
        glColor3f(1.0, 1.0, 1.0)  # White lines
    else:
        glColor3f(0.0, 0.0, 0.0)  # Black lines
    glLineWidth(5.0)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-4.0, -1.0, 0.0)
    glVertex3f(4.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()

def drawStructure():
    if lines_white:
        glColor3f(1.0, 1.0, 1.0)  # White lines
    else:
        glColor3f(0.0, 0.0, 0.0)  # Black lines
    glBegin(GL_LINES)
    glVertex3f(-3.5, -1.0, 0.0)  # Shifted left
    glVertex3f(-3.5, -4.0, 0.0)  # Shifted left

    glVertex3f(3.5, -1.0, 0.0)   # Shifted right
    glVertex3f(3.5, -4.0, 0.0)   # Shifted right

    glVertex3f(-3.5, -4.0, 0.0)  # Bottom point of left vertical line
    glVertex3f(3.5, -4.0, 0.0)
    glEnd()

def drawDoor():
    if lines_white:
        glColor3f(1.0, 1.0, 1.0)  # White lines
    else:
        glColor3f(0.0, 0.0, 0.0)  # Black lines
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex3f(-1.1, -2.0, 0.0)  # Shifted left
    glVertex3f(-1.1, -4.0, 0.0)  # Shifted left

    glVertex3f(-2.3, -2.0, 0.0)   # Shifted right
    glVertex3f(-2.3, -4.0, 0.0)   # Shifted right

    # Top point of left vertical line
    glVertex3f(-2.3, -2.0, 0.0)
    glVertex3f(-1.1, -2.0, 0.0)

    glEnd()

    #add a door knob
    glPointSize(5.0)  # Set point size
    glBegin(GL_POINTS)
    glVertex3f(-1.3, -3, 0.0) 

    glEnd()

def drawWindow():
    if lines_white:
        glColor3f(1.0, 1.0, 1.0)  # White lines
    else:
        glColor3f(0.0, 0.0, 0.0)  # Black lines
    glPushMatrix()
    glTranslatef(2.5, -2.0, 0.0)  # Adjusted translation

    glScalef(0.5, 0.5, 1.0)  # Scale down by half

    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glEnd()

    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)

    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()

    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10)
    glColor3f(1.0, 1.0, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Enable fill mode

    drawRoof()

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Restore line mode

    drawStructure()
    drawDoor()
    drawWindow()
    draw_rain()  # Draw rain

    glutSwapBuffers()

background_white = False
lines_white = True
left_arrow_pressed = False
right_arrow_pressed = False

def keyboard_callback(key, x, y):
    global background_white, lines_white, left_arrow_pressed, right_arrow_pressed

    if key == b'L' or key == b'l':
        background_white = True
        lines_white = False
    if key == b'D' or key == b'd':
        background_white = False
        lines_white = True
    if key == GLUT_KEY_LEFT:
        left_arrow_pressed = True
        right_arrow_pressed = False
    if key == GLUT_KEY_RIGHT:
        left_arrow_pressed = False
        right_arrow_pressed = True

    if background_white:
        glClearColor(1.0, 1.0, 1.0, 1.0)
    else:
        glClearColor(0.0, 0.0, 0.0, 0.0)

    glutPostRedisplay()



# Function to handle window resizing
    

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Triangle")
    glutDisplayFunc(display)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glShadeModel(GL_FLAT)  # Set shading model to flat
    glutKeyboardFunc(keyboard_callback)
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
