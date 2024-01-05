from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import sys
import random

def init():
    global ball_x, ball_y, ball_speed, stick_x, stick_width, score, paused

    ball_x = random.uniform(-0.9, 0.9)
    ball_y = 0.9
    ball_speed = 0.0008
    stick_x = 0.0
    stick_width = 0.3
    score = 0
    paused = False


def reset_ball_position():
    global ball_y
    ball_y = 0.9


def randomize_ball_position():
    global ball_x
    ball_x = random.uniform(-0.9, 0.9)

def draw_diamond(x, y, size):
    half_size = size / 2

    glColor3f(1, 0, 0)

    glBegin(GL_POINTS)

    step = 0.005

    for i in range(0, int(half_size / step) + 1):
        xi = x + i * step
        yi = y + half_size - i * step
        glVertex2f(xi, yi)

    for i in range(0, int(half_size / step) + 1):
        xi = x - i * step
        yi = y + half_size - i * step
        glVertex2f(xi, yi)

    for i in range(0, int(half_size / step) + 1):
        xi = x + i * step
        yi = y - half_size + i * step
        glVertex2f(xi, yi)

    for i in range(0, int(half_size / step) + 1):
        xi = x - i * step
        yi = y - half_size + i * step
        glVertex2f(xi, yi)

    glEnd()

def draw_rectangle_stick(x, width, height):
    half_width = width / 2

    left_x = x - half_width
    right_x = x + half_width
    top_y = -0.9
    bottom_y = top_y - height

    glColor3f(1, 1, 1)

    glBegin(GL_POINTS)

    step = 0.005
    for i in range(0, int(width / step) + 1):
        xi = left_x + i * step
        glVertex2f(xi, top_y)
        glVertex2f(xi, bottom_y)

    for i in range(0, int(height / step) + 1):
        yi = bottom_y + i * step
        glVertex2f(left_x, yi)
        glVertex2f(right_x, yi)

    glEnd()

def special_key_callback(key, x, y):
    global stick_x

    if not paused:
        if key == GLUT_KEY_LEFT and stick_x - stick_width / 2 > -1.0:
            stick_x -= 0.1
        elif key == GLUT_KEY_RIGHT and stick_x + stick_width / 2 < 1.0:
            stick_x += 0.1
        glutPostRedisplay()

pause_button_x = 0.0
pause_button_y = 0.9
pause_button_size = 0.05

def draw_pause_button():
    outline_width = pause_button_size * 2.0
    outline_height = pause_button_size * 2.0

    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(pause_button_x - outline_width / 2, pause_button_y - outline_height / 2)
    glVertex2f(pause_button_x + outline_width / 2, pause_button_y - outline_height / 2)
    glVertex2f(pause_button_x + outline_width / 2, pause_button_y + outline_height / 2)
    glVertex2f(pause_button_x - outline_width / 2, pause_button_y + outline_height / 2)
    glEnd()

    symbol_x = pause_button_x
    symbol_y = pause_button_y

    glColor3f(1.0, 1.0, 0.0)

    glBegin(GL_POINTS)

    if not paused:
        for i in range(0, int(pause_button_size / 0.005) + 1):
            xi = symbol_x - pause_button_size / 4
            yi = symbol_y - pause_button_size / 2 + i * 0.005
            glVertex2f(xi, yi)

        for i in range(0, int(pause_button_size / 0.005) + 1):
            xi = symbol_x + pause_button_size / 4
            yi = symbol_y - pause_button_size / 2 + i * 0.005
            glVertex2f(xi, yi)
    else:
        triangle_size = pause_button_size

        vertices = [
            (symbol_x - triangle_size / 2, symbol_y - triangle_size / 2),
            (symbol_x - triangle_size / 2, symbol_y + triangle_size / 2),
            (symbol_x + triangle_size / 2, symbol_y),
        ]

        num_dots = 30

        for i in range(num_dots + 1):
            t = i / num_dots
            for j in range(3):
                x1, y1 = vertices[j]
                x2, y2 = vertices[(j + 1) % 3]
                xi = x1 + t * (x2 - x1)
                yi = y1 + t * (y2 - y1)
                glVertex2f(xi, yi)

    glEnd()

restart_button_x = -0.9
restart_button_y = 0.9
restart_button_size = 0.05

def draw_restart_button():
    outline_width = restart_button_size * 2.0
    outline_height = restart_button_size * 2.0

    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(restart_button_x - outline_width / 2, restart_button_y - outline_height / 2)
    glVertex2f(restart_button_x + outline_width / 2, restart_button_y - outline_height / 2)
    glVertex2f(restart_button_x + outline_width / 2, restart_button_y + outline_height / 2)
    glVertex2f(restart_button_x - outline_width / 2, restart_button_y + outline_height / 2)
    glEnd()

    symbol_x = restart_button_x
    symbol_y = restart_button_y

    glColor3f(0.6, 0.8, 1.0)
    glBegin(GL_POINTS)

    vertices = [
        (symbol_x + restart_button_size / 4, symbol_y - restart_button_size / 2),  # Bottom right vertex
        (symbol_x + restart_button_size / 4, symbol_y + restart_button_size / 2),  # Top right vertex
        (symbol_x - restart_button_size / 2, symbol_y),  # Left vertex
    ]

    num_dots = 30

    for i in range(num_dots + 1):
        t = i / num_dots
        for j in range(3):
            x1, y1 = vertices[j]
            x2, y2 = vertices[(j + 1) % 3]
            xi = x1 + t * (x2 - x1)
            yi = y1 + t * (y2 - y1)
            glVertex2f(xi, yi)

    glEnd()

def restart_game():
    global ball_x, ball_y, score, paused
    init()
    randomize_ball_position()
    paused = False
close_button_x = 0.9
close_button_y = 0.9
close_button_size = 0.025


def draw_close_button():
    outline_width = close_button_size * 2.0
    outline_height = close_button_size * 2.0

    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(close_button_x - outline_width / 2, close_button_y - outline_height / 2)
    glVertex2f(close_button_x + outline_width / 2, close_button_y - outline_height / 2)
    glVertex2f(close_button_x + outline_width / 2, close_button_y + outline_height / 2)
    glVertex2f(close_button_x - outline_width / 2, close_button_y + outline_height / 2)
    glEnd()

    symbol_x = close_button_x
    symbol_y = close_button_y

    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_POINTS)

    step = 0.005

    for i in range(0, int(close_button_size / step) + 1):
        x = symbol_x
        y = symbol_y

        glVertex2f(x - i * step, y - i * step)
        glVertex2f(x + i * step, y + i * step)

        glVertex2f(x - i * step, y + i * step)
        glVertex2f(x + i * step, y - i * step)

    glEnd()


def mouse_click(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        opengl_x = (x / 400) * 2 - 1
        opengl_y = 1 - (y / 600) * 2

        if (
                opengl_x >= pause_button_x - pause_button_size / 2 and
                opengl_x <= pause_button_x + pause_button_size / 2 and
                opengl_y >= pause_button_y - pause_button_size / 2 and
                opengl_y <= pause_button_y + pause_button_size / 2
        ):
            paused = not paused
        if (
                opengl_x >= restart_button_x - restart_button_size / 2 and
                opengl_x <= restart_button_x + restart_button_size / 2 and
                opengl_y >= restart_button_y - restart_button_size / 2 and
                opengl_y <= restart_button_y + restart_button_size / 2
        ):
            restart_game()


        if (
                opengl_x >= close_button_x - close_button_size and
                opengl_x <= close_button_x + close_button_size and
                opengl_y >= close_button_y - close_button_size and
                opengl_y <= close_button_y + close_button_size
        ):
            glutLeaveMainLoop()



def game_loop():
    global ball_y, score, paused

    glClear(GL_COLOR_BUFFER_BIT)

    draw_diamond(ball_x, ball_y, 0.09)

    draw_rectangle_stick(stick_x, stick_width, 0.05)

    draw_pause_button()

    draw_restart_button()

    draw_close_button()


    if not paused:
        ball_y -= ball_speed
        glutPostRedisplay()

    glutSwapBuffers()


    if (
            ball_y < -0.85
            and ball_x >= stick_x - stick_width / 2
            and ball_x <= stick_x + stick_width / 2
    ):
        reset_ball_position()
        randomize_ball_position()
        score += 1
        print(f"Score: {score}")


    if ball_y < -1.0 and not paused:
        print(f"Game Over! Score: {score}")
        paused = not paused

    glutTimerFunc(10, game_loop, 0)


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(400, 600)
    glutCreateWindow(b"Falling Ball")

    init()

    randomize_ball_position()
    glutDisplayFunc(game_loop)
    glutTimerFunc(0, game_loop, 0)
    glutSpecialFunc(special_key_callback)
    glutMouseFunc(mouse_click)

    glutMainLoop()