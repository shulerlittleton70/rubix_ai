import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pycuber as pc

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Rubik's Cube - Enhanced Lighting")

# Set OpenGL Projection & Camera
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0.0, 0.0, -6)

# Enable OpenGL Features
glEnable(GL_DEPTH_TEST)
glDisable(GL_CULL_FACE)

# **Brighter Background Color**
glClearColor(0.2, 0.2, 0.2, 1)  # Slightly lighter gray

# **Adjust Lighting for Less Darkness**
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)

# **Better Light Positioning**
glLightfv(GL_LIGHT0, GL_POSITION, (3, 3, 3, 1))  # More balanced front light
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1))  # Brighter overall light
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))  # Less deep shadows
glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))  # Shinier reflections

# Enable color material so faces retain color even under lighting
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
glShadeModel(GL_SMOOTH)

# **More Vibrant and Realistic Colors**
FACE_COLORS = {
    'U': (1, 1, 1),      # White (Bright)
    'D': (1, 0.9, 0.2),  # Yellow (Lighter)
    'F': (0.1, 0.8, 0.1),  # Green (Less dark)
    'B': (0.1, 0.2, 0.9),  # Blue (More vibrant)
    'L': (1, 0.5, 0.2),  # Orange (Less harsh)
    'R': (0.9, 0.1, 0.1)  # Red (More natural)
}

# Reduce spacing to remove gaps
SPACING = 1.01

# Define 3D positions for cubelets (3x3)
cube_positions = [(x * SPACING, y * SPACING, z * SPACING)
                  for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)]

# Create a Rubik’s Cube instance
cube = pc.Cube()

# Function to determine if a face is internal (truly hidden)
def is_internal(x, y, z):
    """Returns True if the cubelet is fully inside (center cube)."""
    return x == 0 and y == 0 and z == 0  # Only the very center cube should be hidden

# Function to draw a single cubelet with correct face colors
def draw_cubelet(x, y, z):
    """Draws an individual cubelet with correct face colors and lighting."""
    vertices = [
        [x - 0.5, y - 0.5, z - 0.5], [x + 0.5, y - 0.5, z - 0.5],
        [x + 0.5, y + 0.5, z - 0.5], [x - 0.5, y + 0.5, z - 0.5],
        [x - 0.5, y - 0.5, z + 0.5], [x + 0.5, y - 0.5, z + 0.5],
        [x + 0.5, y + 0.5, z + 0.5], [x - 0.5, y + 0.5, z + 0.5]
    ]

    faces = [
        (0, 1, 2, 3),  # Front
        (4, 5, 6, 7),  # Back
        (0, 1, 5, 4),  # Bottom
        (2, 3, 7, 6),  # Top
        (0, 3, 7, 4),  # Left
        (1, 2, 6, 5)   # Right
    ]

    # **Draw faces first, then draw edges separately**
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        if is_internal(x, y, z):
            glColor3fv((0.1, 0.1, 0.1))  # Softer black for hidden faces
        else:
            glColor3fv(list(FACE_COLORS.values())[i])  # Assign correct face color
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    # **More Natural Black Borders**
    glColor3fv((0.15, 0.15, 0.15))  # Less harsh black
    glLineWidth(2)
    glBegin(GL_LINES)
    for edge in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw full 3x3 cube
def draw_rubiks_cube():
    for pos in cube_positions:
        draw_cubelet(*pos)

# **Mouse Rotation Variables**
dragging = False
last_mouse_x, last_mouse_y = 0, 0

# **Main game loop**
running = True
angle_x, angle_y = 0, 0  # Rotation angles

while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    draw_rubiks_cube()
    glPopMatrix()

    pygame.display.flip()
    glFlush()  # Force OpenGL rendering
    pygame.time.wait(10)

    # **Event Handling**
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            dragging = True
            last_mouse_x, last_mouse_y = event.pos
        elif event.type == MOUSEBUTTONUP:
            dragging = False
        elif event.type == MOUSEMOTION and dragging:
            dx, dy = event.pos[0] - last_mouse_x, event.pos[1] - last_mouse_y
            angle_y += dx * 0.5
            angle_x += dy * 0.5
            last_mouse_x, last_mouse_y = event.pos

pygame.quit()