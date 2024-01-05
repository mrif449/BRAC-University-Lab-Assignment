from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height = 800, 600
num_buildings = 32
num_floors_range = (4, 16)
building_width = 64
building_spacing = 8
floor_height = 24
window_color = (1.0, 1.0, 1.0)
street_width = 200
lane_width = 48
sky_color = {
    "Morning": (0.5, 0.8, 1.0),
    "Noon": (0.8, 0.8, 0.8),
    "Afternoon": (0.6, 0.6, 1.0),
    "Evening": (1.0, 0.6, 0.6),
    "Night": (0.2, 0.2, 0.2),
}

time_of_day = ["Morning", "Noon", "Afternoon", "Evening", "Night"]
current_time_index = 0

num_stars_afternoon = 10
num_stars_evening = 30
num_stars_night = 50

stars = []

car_width = 40
car_length = 80
car_height = 20
tire_radius = 8
num_cars_per_lane = 2
cars = []

clouds = []

speed = 3000
paused = False

def keyboard(key, x, y):
    global speed, paused

    if key == b'w':
        speed = max(speed // 2, 300) 
    elif key == b's':
        speed = min(speed * 2, 6000)
    elif key == b' ':
        paused = not paused

def drawCar(x, y, color):
    global current_time_index, time_of_day
    
    r, g, b = color
    
    if time_of_day[current_time_index] == "Evening":
        darkening_factor = 0.5
        r *= darkening_factor
        g *= darkening_factor
        b *= darkening_factor
        
    elif time_of_day[current_time_index] == "Night":
        darkening_factor = 0.25 
        r *= darkening_factor
        g *= darkening_factor
        b *= darkening_factor

    glColor3f(r, g, b)

    glBegin(GL_QUADS)
    glVertex2f(x - car_length / 2, y - car_height / 2)
    glVertex2f(x + car_length / 2, y - car_height / 2)
    glVertex2f(x + car_length / 2, y + car_height / 2)
    glVertex2f(x - car_length / 2, y + car_height / 2)
    glEnd()

    hood_length = 10
    hood_width = 10

    glBegin(GL_QUADS)
    glVertex2f(x + car_length / 2, y + car_height / 2 - hood_width)
    glVertex2f(x + car_length / 2 + hood_length, y + car_height / 2 - hood_width)
    glVertex2f(x + car_length / 2 + hood_length, y - car_height / 2)
    glVertex2f(x + car_length / 2, y - car_height / 2)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x - car_length / 2 - hood_length, y + car_height / 2 - hood_width)
    glVertex2f(x - car_length / 2, y + car_height / 2 - hood_width)
    glVertex2f(x - car_length / 2, y - car_height / 2)
    glVertex2f(x - car_length / 2 - hood_length, y - car_height / 2)
    glEnd()

    window_width = car_length / 4
    window_height = car_height / 4
    window_spacing = car_length / 2

    glColor3f(1.0, 1.0, 0.5)
    glBegin(GL_QUADS)
    glVertex2f(x - window_spacing - window_width / 2, y - window_height / 2)
    glVertex2f(x - window_spacing + window_width / 2, y - window_height / 2)
    glVertex2f(x - window_spacing + window_width / 2, y + window_height / 2)
    glVertex2f(x - window_spacing - window_width / 2, y + window_height / 2)
    glEnd()

    glColor3f(1.0, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex2f(x + window_spacing - window_width / 2, y - window_height / 2)
    glVertex2f(x + window_spacing + window_width / 2, y - window_height / 2)
    glVertex2f(x + window_spacing + window_width / 2, y + window_height / 2)
    glVertex2f(x + window_spacing - window_width / 2, y + window_height / 2)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    x_tire = x + (car_length / 2) * 0.8
    y_tire = y - car_height / 2 - tire_radius * 0.8
    drawCircle(x_tire, y_tire, tire_radius)
    glColor3f(0.5, 0.5, 0.5)
    drawCircle(x_tire, y_tire, tire_radius / 2)
    glColor3f(0.0, 0.0, 0.0)
    x_tire = x - (car_length / 2) * 0.8
    y_tire = y - car_height / 2 - tire_radius * 0.8
    drawCircle(x_tire, y_tire, tire_radius)
    glColor3f(0.5, 0.5, 0.5)
    drawCircle(x_tire, y_tire, tire_radius / 2)

def drawCircle(cx, cy, radius):
    x = radius
    y = 0
    d = 1 - radius

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)

    while y <= x:
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx + x, cy - y)
        glVertex2f(cx - x, cy - y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
        glVertex2f(cx + y, cy - x)
        glVertex2f(cx - y, cy - x)

        y += 1
        if d >= 0:
            x -= 1
            d += 2 * (y - x)
        else:
            d += 2 * y
    glEnd()

def generate_cars():
    global cars
    cars.clear()
    lane_spacing = street_width / 4
    min_car_distance = 16 

    for lane in range(3):
        for _ in range(num_cars_per_lane):
            x = random.uniform(-W_Width / 2, W_Width / 2)
            y = -W_Height / 2 + lane_spacing * (lane + 1)
            color = (random.random(), random.random(), random.random())
            
            while any(
                abs(x - existing_x) < min_car_distance and abs(y - existing_y) < car_height
                for existing_x, existing_y, _ in cars
            ):
                x = random.uniform(-W_Width / 2, W_Width / 2)

            cars.append((x, y, color))

def drawCars():
    for car in cars:
        drawCar(*car)

def generate_cars():
    global cars
    cars.clear()
    lane_spacing = street_width / 4
    for lane in range(3):
        for _ in range(num_cars_per_lane):
            x = random.uniform(-W_Width / 2, W_Width / 2)
            y = -W_Height / 2 + lane_spacing * (lane + 1)
            color = (random.random(), random.random(), random.random())
            cars.append((x, y, color))

def drawCars():
    for car in cars:
        drawCar(*car)

def generate_stars(num_stars):
    stars.clear()
    for _ in range(num_stars):
        x = random.uniform(-W_Width / 2, W_Width / 2)
        y = random.uniform(-W_Height / 2 + street_width, W_Height / 2)
        stars.append((x, y))

def drawBuilding(x, num_floors, time_key):
    if time_key == "Night":
        building_color = (random.uniform(0.0, 1/3), random.uniform(0.1, 0.3), random.uniform(0.1, 0.3))
        
    elif time_key == "Evening":
        building_color = (random.uniform(1/3, 2/3), random.uniform(0.1, 0.3), random.uniform(0.1, 0.3))
    
    else:
        building_color = (random.random(), random.random(), random.random())

    glColor3f(*building_color)
    glBegin(GL_QUADS)
    glVertex2f(x - building_width / 2, -W_Height / 2 + street_width)
    glVertex2f(x + building_width / 2, -W_Height / 2 + street_width)
    glVertex2f(x + building_width / 2, -W_Height / 2 + street_width + num_floors * floor_height)
    glVertex2f(x - building_width / 2, -W_Height / 2 + street_width + num_floors * floor_height)
    glEnd()

    glColor3f(*window_color)
    window_width = building_width / 7
    window_height = floor_height / 3
    window_spacing = building_width / 15
    for floor in range(num_floors):
        for window in range(5):
            glBegin(GL_QUADS)
            wx = x - building_width / 2 + window * (window_width + window_spacing)
            wy = -W_Height / 2 + street_width + floor * floor_height + floor_height / 3
            glVertex2f(wx, wy)
            glVertex2f(wx + window_width, wy)
            glVertex2f(wx + window_width, wy + window_height)
            glVertex2f(wx, wy + window_height)
            glEnd()

def drawStreet():
    glColor3f(0.2, 0.2, 0.2)
    drawFilledRectangle(-W_Width / 2, -W_Height / 2, W_Width / 2, -W_Height / 2 + street_width)
    lane_spacing = street_width / 4
    glColor3f(1.0, 1.0, 1.0)
    adjusted_lane_width = 5

    for lane in range(3):
        lane_y = -W_Height / 2 + lane_spacing * (lane + 1)
        drawFilledRectangle(-W_Width / 2, lane_y - adjusted_lane_width, W_Width / 2, lane_y + adjusted_lane_width)

def drawFilledRectangle(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def drawLine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    x = x1
    y = y1

    glBegin(GL_POINTS)
    while x <= x2:
        glVertex2f(x, y)
        x += 1
        if d < 0:
            d += 2 * dy
        else:
            d += 2 * (dy - dx)
            y += 1
    glEnd()

def drawBackground():
    global current_time_index
    time_key = time_of_day[current_time_index]
    sky_r, sky_g, sky_b = sky_color[time_key]

    glColor3f(sky_r, sky_g, sky_b)
    glBegin(GL_QUADS)
    glVertex2f(-W_Width / 2, -W_Height / 2 + street_width)
    glVertex2f(W_Width / 2, -W_Height / 2 + street_width)
    glVertex2f(W_Width / 2, W_Height / 2)
    glVertex2f(-W_Width / 2, W_Height / 2)
    glEnd()
    
    if time_key == "Night":
        generate_stars(num_stars_night)
        drawMoon()
    else:
        if time_key == "Afternoon":
            generate_stars(num_stars_afternoon)
            drawSun(time_key)
            generate_clouds()
            drawClouds()
        elif time_key == "Evening":
            generate_stars(num_stars_evening)
            drawSun(time_key)
            generate_clouds()
            drawClouds()
        elif time_key == "Morning" or time_key == "Noon":
            drawSun(time_key)
            generate_clouds()
            drawClouds()

    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for star in stars:
        glVertex2f(star[0], star[1])
    glEnd()

def drawMoon():
    moon_size = 32
    moon_position = (-W_Width / 4, W_Height / 4)

    glColor3f(0.75, 0.75, 0.75)
    drawCircle(*moon_position, moon_size)

def drawSun(time_key):
    if time_key == "Morning":
        sun_size = 48
        sun_position = (-W_Width / 4, W_Height / 4)
    elif time_key == "Noon":
        sun_size = 64
        sun_position = (0, W_Height / 4)
    elif time_key == "Afternoon":
        sun_size = 96
        sun_position = (W_Width / 4, W_Height / 8)
    elif time_key == "Evening":
        sun_size = 128
        sun_position = (W_Width / 4, -W_Height / 4)
    else:
        return

    glColor3f(1.0, 1.0, 0.0)
    drawCircle(*sun_position, sun_size)

def generate_clouds():
    global clouds
    clouds.clear()
    num_clouds = random.randint(5, 10)

    for _ in range(num_clouds):
        x = random.uniform(-W_Width / 2, W_Width / 2)
        y = random.uniform(-W_Height / 2 + street_width + floor_height * 3, W_Height / 2)
        size = random.uniform(50, 100)
        clouds.append((x, y, size))

def drawClouds():
    for cloud in clouds:
        drawCloud(*cloud)

def drawCloud(x, y, size, alpha=1.0):
    glColor4f(1.0, 1.0, 1.0, alpha)
    num_segments = 100
    glBegin(GL_POLYGON)
    for i in range(num_segments):
        theta = 2.0 * 3.1415926 * i / num_segments
        cloud_x = x + size * 0.6 * math.cos(theta)
        cloud_y = y + size * 0.4 * math.sin(theta)
        glVertex2f(cloud_x, cloud_y)
    glEnd()

def display():
    global current_time_index
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawBackground()
    for i in range(num_buildings):
        num_floors = random.randint(*num_floors_range)
        x = -W_Width / 2 + i * (building_width + building_spacing)
        drawBuilding(x, num_floors, time_of_day[current_time_index])
    drawStreet()
    drawCars()
    glutSwapBuffers()

def update_time(_):
    global current_time_index, speed, paused

    if not paused:
        current_time_index = (current_time_index + 1) % len(time_of_day)

        if time_of_day[current_time_index] == "Morning":
            stars.clear()
            generate_cars()

    glutPostRedisplay()
    glutTimerFunc(speed, update_time, 0)

def init():
    glClearColor(0.0, 0.0, 0.0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2)

def main():
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    wind = glutCreateWindow(b"Camera is facing south, camera is locked on the cars, cars are moving east.")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(speed, update_time, 0)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    generate_cars()
    main()