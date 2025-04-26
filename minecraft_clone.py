import pyglet
from vpython import box, vector, scene, rate

# Setup VPython
scene.title = "Minecraft Clone"
scene.width = 800
scene.height = 600
scene.background = vector(0.5, 0.7, 1)  # light blue sky

# Simple world storage
blocks = {}

# Function to create a block
def create_block(x, y, z, color=vector(0.6, 0.4, 0.2)):
    b = box(pos=vector(x, y, z), size=vector(1, 1, 1), color=color)
    blocks[(x, y, z)] = b

# Create a flat ground
for x in range(-5, 6):
    for z in range(-5, 6):
        create_block(x, -1, z, color=vector(0.3, 0.8, 0.3))  # grass color

# Setup Pyglet
window = pyglet.window.Window(800, 600, "Minecraft Clone", resizable=True)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        # Add a block above the center
        pos = (0, 0, 0)
        if pos not in blocks:
            create_block(*pos)
    elif symbol == pyglet.window.key.BACKSPACE:
        # Remove block at center
        pos = (0, 0, 0)
        if pos in blocks:
            blocks[pos].visible = False
            del blocks[pos]

def update(dt):
    rate(60)

pyglet.clock.schedule_interval(update, 1/60.0)

# Run the window
pyglet.app.run()