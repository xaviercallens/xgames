"""
Cube Runner - A 3D game example using Panda3D.
Demonstrates 3D graphics, lighting, camera control, and basic 3D game mechanics.
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import random
import sys


class CubeRunner(ShowBase):
    """Main 3D game class using Panda3D."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        # Disable the camera trackball controls
        self.disableMouse()
        
        # Set up the environment
        self.setup_environment()
        self.setup_lighting()
        self.setup_player()
        self.setup_obstacles()
        self.setup_ui()
        self.setup_controls()
        
        # Game state
        self.game_speed = 20
        self.score = 0
        self.game_over = False
        
        # Start the game loop
        self.taskMgr.add(self.game_loop, "game_loop")
        
    def setup_environment(self):
        """Set up the 3D environment."""
        # Set background color
        self.setBackgroundColor(0.1, 0.1, 0.8, 1)
        
        # Create ground plane
        self.ground = self.loader.loadModel("environment")
        if not self.ground:
            # Create a simple ground plane if environment model doesn't exist
            cm = CardMaker("ground")
            cm.setFrame(-50, 50, -50, 50)
            self.ground = self.render.attachNewNode(cm.generate())
            self.ground.setP(-90)  # Rotate to be horizontal
            self.ground.setColor(0.2, 0.8, 0.2, 1)  # Green ground
        else:
            self.ground.reparentTo(self.render)
            self.ground.setScale(1, 1, 1)
            self.ground.setPos(0, 0, 0)
        
        # Set up camera position
        self.camera.setPos(0, -20, 5)
        self.camera.lookAt(0, 0, 0)
        
    def setup_lighting(self):
        """Set up lighting for the 3D scene."""
        # Ambient light
        ambient_light = AmbientLight('ambient_light')
        ambient_light.setColor((0.3, 0.3, 0.3, 1))
        ambient_light_np = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_light_np)
        
        # Directional light
        directional_light = DirectionalLight('directional_light')
        directional_light.setDirection((-5, -5, -5))
        directional_light.setColor((0.8, 0.8, 0.8, 1))
        directional_light_np = self.render.attachNewNode(directional_light)
        self.render.setLight(directional_light_np)
        
    def setup_player(self):
        """Set up the player cube."""
        # Create player cube
        self.player = self.loader.loadModel("models/box")
        if not self.player:
            # Create a simple cube if box model doesn't exist
            self.player = self.render.attachNewNode("player")
            # Create a cube geometry
            cube_geom = self.create_cube_geometry()
            cube_node = GeomNode("player_cube")
            cube_node.addGeom(cube_geom)
            self.player.attachNewNode(cube_node)
            
        self.player.reparentTo(self.render)
        self.player.setScale(1, 1, 1)
        self.player.setPos(0, 0, 1)
        self.player.setColor(0, 1, 0, 1)  # Green player
        
        # Player properties
        self.player_speed = 10
        self.player_x = 0
        
    def create_cube_geometry(self):
        """Create a cube geometry programmatically."""
        # Vertex format
        format = GeomVertexFormat.getV3n3()
        vdata = GeomVertexData('cube', format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        
        # Define cube vertices
        vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),  # Bottom face
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)       # Top face
        ]
        
        # Add vertices
        for v in vertices:
            vertex.addData3(v[0], v[1], v[2])
            normal.addData3(0, 0, 1)  # Simple normal
            
        # Create geometry
        geom = Geom(vdata)
        
        # Define faces
        faces = [
            [0, 1, 2, 3],  # Bottom
            [4, 7, 6, 5],  # Top
            [0, 4, 5, 1],  # Front
            [2, 6, 7, 3],  # Back
            [0, 3, 7, 4],  # Left
            [1, 5, 6, 2]   # Right
        ]
        
        for face in faces:
            quad = GeomTriangles(Geom.UHStatic)
            # Two triangles per face
            quad.addVertices(face[0], face[1], face[2])
            quad.addVertices(face[0], face[2], face[3])
            geom.addPrimitive(quad)
            
        return geom
        
    def setup_obstacles(self):
        """Set up obstacle system."""
        self.obstacles = []
        self.obstacle_spawn_time = 0
        self.obstacle_spawn_delay = 2.0  # seconds
        
    def setup_ui(self):
        """Set up user interface."""
        self.score_text = OnscreenText(
            text=f"Score: {self.score}",
            pos=(-0.9, 0.9),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft
        )
        
        self.instructions = OnscreenText(
            text="Use A/D or Arrow Keys to move\nSpace to jump\nESC to quit",
            pos=(0.9, 0.9),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ARight
        )
        
    def setup_controls(self):
        """Set up input controls."""
        self.accept("escape", sys.exit)
        self.accept("a", self.move_left)
        self.accept("d", self.move_right)
        self.accept("arrow_left", self.move_left)
        self.accept("arrow_right", self.move_right)
        self.accept("space", self.jump)
        
        # Continuous key handling
        self.keys = {"left": False, "right": False}
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        self.accept("arrow_left", self.set_key, ["left", True])
        self.accept("arrow_left-up", self.set_key, ["left", False])
        self.accept("arrow_right", self.set_key, ["right", True])
        self.accept("arrow_right-up", self.set_key, ["right", False])
        
    def set_key(self, key, value):
        """Set key state for continuous input."""
        self.keys[key] = value
        
    def move_left(self):
        """Move player left."""
        if not self.game_over:
            self.player_x = max(-10, self.player_x - 2)
            
    def move_right(self):
        """Move player right."""
        if not self.game_over:
            self.player_x = min(10, self.player_x + 2)
            
    def jump(self):
        """Make player jump."""
        if not self.game_over:
            # Simple jump animation
            jump_up = self.player.posInterval(0.3, Point3(self.player_x, 0, 3))
            jump_down = self.player.posInterval(0.3, Point3(self.player_x, 0, 1))
            jump_sequence = Sequence(jump_up, jump_down)
            jump_sequence.start()
            
    def spawn_obstacle(self):
        """Spawn a new obstacle."""
        obstacle = self.loader.loadModel("models/box")
        if not obstacle:
            # Create obstacle cube
            obstacle = self.render.attachNewNode("obstacle")
            cube_geom = self.create_cube_geometry()
            cube_node = GeomNode("obstacle_cube")
            cube_node.addGeom(cube_geom)
            obstacle.attachNewNode(cube_node)
            
        obstacle.reparentTo(self.render)
        obstacle.setScale(1, 1, 2)  # Taller obstacle
        obstacle.setColor(1, 0, 0, 1)  # Red obstacle
        
        # Random position
        x_pos = random.uniform(-8, 8)
        obstacle.setPos(x_pos, 30, 1)
        
        self.obstacles.append(obstacle)
        
    def update_obstacles(self, dt):
        """Update obstacle positions."""
        for obstacle in self.obstacles[:]:  # Copy list to avoid modification issues
            current_pos = obstacle.getPos()
            new_y = current_pos.getY() - self.game_speed * dt
            obstacle.setPos(current_pos.getX(), new_y, current_pos.getZ())
            
            # Remove obstacles that are behind the camera
            if new_y < -25:
                obstacle.removeNode()
                self.obstacles.remove(obstacle)
                self.score += 10
                
    def check_collisions(self):
        """Check for collisions between player and obstacles."""
        player_pos = self.player.getPos()
        
        for obstacle in self.obstacles:
            obstacle_pos = obstacle.getPos()
            
            # Simple collision detection
            distance = ((player_pos.getX() - obstacle_pos.getX()) ** 2 + 
                       (player_pos.getY() - obstacle_pos.getY()) ** 2 + 
                       (player_pos.getZ() - obstacle_pos.getZ()) ** 2) ** 0.5
                       
            if distance < 2:  # Collision threshold
                self.game_over = True
                self.show_game_over()
                
    def show_game_over(self):
        """Display game over screen."""
        self.game_over_text = OnscreenText(
            text=f"GAME OVER!\nFinal Score: {self.score}\nPress R to Restart",
            pos=(0, 0),
            scale=0.1,
            fg=(1, 0, 0, 1),
            align=TextNode.ACenter
        )
        self.accept("r", self.restart_game)
        
    def restart_game(self):
        """Restart the game."""
        # Clean up
        for obstacle in self.obstacles:
            obstacle.removeNode()
        self.obstacles.clear()
        
        if hasattr(self, 'game_over_text'):
            self.game_over_text.destroy()
            
        # Reset game state
        self.score = 0
        self.game_over = False
        self.player.setPos(0, 0, 1)
        self.player_x = 0
        
        # Update UI
        self.score_text.setText(f"Score: {self.score}")
        
    def game_loop(self, task):
        """Main game loop."""
        dt = globalClock.getDt()
        
        if not self.game_over:
            # Handle continuous input
            if self.keys["left"]:
                self.player_x = max(-10, self.player_x - self.player_speed * dt)
            if self.keys["right"]:
                self.player_x = min(10, self.player_x + self.player_speed * dt)
                
            # Update player position
            current_pos = self.player.getPos()
            self.player.setPos(self.player_x, current_pos.getY(), current_pos.getZ())
            
            # Spawn obstacles
            self.obstacle_spawn_time += dt
            if self.obstacle_spawn_time >= self.obstacle_spawn_delay:
                self.spawn_obstacle()
                self.obstacle_spawn_time = 0
                
            # Update obstacles
            self.update_obstacles(dt)
            
            # Check collisions
            self.check_collisions()
            
            # Update score display
            self.score_text.setText(f"Score: {self.score}")
            
            # Increase game speed gradually
            self.game_speed += dt * 0.5
            
        return task.cont


if __name__ == "__main__":
    game = CubeRunner()
    game.run()
