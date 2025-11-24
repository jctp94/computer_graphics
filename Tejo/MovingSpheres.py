## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

from ast import Not
import os, sys
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, './lib' ) )
sys.path.append( imp_dir )
import pybullet, Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites
import random
import math
import time
from TejoListener import *
import pygame

"""
"""
class MovingSpheres( PUJ_Ogre.BaseApplicationWithVTK ):

  '''
  '''
  m_MovingBodies = {}
  m_StaticBodies = {}
  wx, wy, wz = 0.0, 0.3, -4.5
  base = 2.0
  height = 0.2
  length = 1.0
  field_rotation_deg = -30.0
  bocin_gap = length * 0.09
  mecha_proportion = 0.06
  deep_hole_proportion = 0.0
  tejo_count = 0
  camera_initial_position = [0, 1.7, 5]
  last_tejo_scored = 0
  score = 0
  '''
  '''
  def __init__( self ):
    pygame.mixer.init()
    self.mecha_sound = pygame.mixer.Sound("sonido/mecha_hit.wav")
    self.metal_sound = pygame.mixer.Sound("sonido/metal_hit.mp3")
    self.bocin_sound = pygame.mixer.Sound("sonido/bocin_hit.mp3")
    self.moniona_sound = pygame.mixer.Sound("sonido/moniona_hit.mp3")
    self.wood_sound = pygame.mixer.Sound("sonido/wood_hit.mp3")
    self.paused = False
    super( MovingSpheres, self ).__init__( 'MovingSpheres v0.1', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )
  # end def

  def setup( self ):
    self.m_Listener = TejoListener( self.getRoot( ), self )
    super( MovingSpheres, self ).setup( )  

  '''
  '''
  def _loadScene( self ):

    # Prepare Bullet
    pybullet.connect( pybullet.GUI )
    pybullet.setGravity( 0, -5, 0 )

    # Get root and create scene managerf
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )

    # Configure camera
    self._createCamera(
      top_speed = 3,
      position = self.camera_initial_position,
      look_at = [ 0, 1.70, 0 ],
      background = [ 0.9, 0.75, 0.5 ],
      cam_style = OgreBites.CS_FREELOOK
      )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_DIRECTIONAL )
    light.setDirection( [ 0, -1, 0 ] )

    # A ground
    self._ground( 'ground', [ -1.00, 1.00, -5.00, 4.00 ] )
    ground_bullet = pybullet.createCollisionShape( pybullet.GEOM_PLANE, planeNormal = [ 0, 1, 0 ] )
    ground_body = pybullet.createMultiBody( 0, ground_bullet, -1, [ 0, 0, 0 ] )
    pybullet.changeDynamics( ground_body, -1, restitution = -0.5, lateralFriction = 20 )
    self.m_StaticBodies[ 'ground' ] = ground_body

   
    pit_incline_deg = 15.0

    theta_x = math.radians(pit_incline_deg)  # inclinación
    theta_y = math.radians(-90.0)
    theta_z = math.radians(self.field_rotation_deg)


    qy = pybullet.getQuaternionFromEuler([0, theta_y, 0])
    qz = pybullet.getQuaternionFromEuler([0, 0, theta_z])

    # Multiplicación para aplicar primero Y, después Z
    q = pybullet.multiplyTransforms([0,0,0], qy, [0,0,0], qz)[1]
    qx, qy, qz, qw = q 

    # posición de la caja en el mundo

    wedge_node = self._createManualObject(
        self._box(self.base, self.height,self.length),
        "tejo_wedge",
        "field"
    )

    wedge_node.setPosition(self.wx, self.wy, self.wz)
    wedge_node.setOrientation( Ogre.Quaternion(qx, qy, qz, qw) )

    # collider como BOX + rotación (no wedge)
    wedge_shape = pybullet.createCollisionShape(
        pybullet.GEOM_BOX,
        halfExtents=[self.base * 0.5, self.height * 0.5, self.length * 0.5]
    )


    wedge_body = pybullet.createMultiBody(
        baseMass=0.0,  # estático
        baseCollisionShapeIndex=wedge_shape,
        baseVisualShapeIndex=-1,
        basePosition=[self.wx, self.wy, self.wz],
        baseOrientation=[qx, qy, qz, qw]
    )

    pybullet.changeDynamics(
        wedge_body, -1,
        restitution=0.5,
        lateralFriction=0.6
    )

    cylinder_node = self._createManualObject(
        self._cylinder(0.3, 1.2),
        "tejo_cylinder",
        "backboard_wood"
    )
    cylinder_node.setPosition(0.0, 0.6, self.wz -0.8)

    collision_shape = pybullet.createCollisionShape(
        pybullet.GEOM_CYLINDER,
        radius=1.2,
        height=0.3
    )
    collision_body = pybullet.createMultiBody(
        baseMass=0.0,
        baseCollisionShapeIndex=collision_shape,
        basePosition=[0.0, 0.6, self.wz -0.8],
        baseOrientation=[0, 0, 0, 1]
    )
    self.m_StaticBodies['tejo_cylinder'] = collision_body
    pybullet.changeDynamics(
        collision_body, -1,
        restitution=0.5,
        lateralFriction=0.6
    )

    self.m_StaticBodies['tejo_wedge'] = wedge_body
    

    self.createAllMechas()

    # Finish pybullet configuration
    pybullet.setPhysicsEngineParameter( numSolverIterations = 10 )

  # end def

  def createAllMechas(self):
    angle = math.radians(self.field_rotation_deg)
    mov_y = math.sin(angle) * self.bocin_gap
    mov_z = math.cos(angle) * self.bocin_gap 
    self.initial_position = [self.wx, self.wy + (self.height / 2) - self.deep_hole_proportion, self.wz]
    print("initial_position", self.initial_position)

    print("mov_y", mov_y)
    print("mov_z", mov_z)
    print("self.bocin_gap", self.bocin_gap)
    positions = [
      [self.initial_position[0] , self.initial_position[1] + mov_y, self.initial_position[2] + mov_z],
      [self.initial_position[0] , self.initial_position[1] - mov_y, self.initial_position[2] - mov_z],
      [self.initial_position[0] - self.bocin_gap, self.initial_position[1], self.initial_position[2] ],
      [self.initial_position[0] + self.bocin_gap, self.initial_position[1], self.initial_position[2] ]
    ]
    self.mecha_positions = positions
    for i in range(len(positions)):
      self.createMecha(positions[i], i )

  def togglePause(self):
    self.paused = not self.paused
    print("PAUSA:", self.paused)


  def highlight_mecha(self, mecha_name):

    # Obtener el objeto adjunto (ManualObject)
    man = self.m_SceneMgr.getManualObject(mecha_name)

    man.setMaterialName(0, "black_material")

  def createMecha(self, position, id):

    mecha_node = self._createManualObject(
        self._mecha(base=self.length * self.mecha_proportion, height=self.length * self.mecha_proportion * 0.86, length=self.length * self.mecha_proportion),
        "mecha_" + str(id),
        "red_material"
    )

    mecha_node.setPosition(position[0], position[1], position[2])
    roll_deg  = 0.0      # inclinación que quieres en grados
    pitch_deg = 0

    roll  = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    yaw   = math.radians(self.field_rotation_deg - 90)
    

    mecha_qx, mecha_qy, mecha_qz, mecha_qw = pybullet.getQuaternionFromEuler([roll, pitch, yaw])
    mecha_node.setOrientation(Ogre.Quaternion(mecha_qx, mecha_qy, mecha_qz, mecha_qw))

    pos = mecha_node.getPosition()
    mx = pos.x
    my = pos.y
    mz = pos.z

    ori = mecha_node.getOrientation()
    mecha_qw = ori.w
    mecha_qx = ori.x
    mecha_qy = ori.y
    mecha_qz = ori.z

    
    mecha_shape = pybullet.createCollisionShape(
        pybullet.GEOM_SPHERE,
        radius=self.length * self.mecha_proportion * 0.5
    )

    # La mecha se modela como un cuerpo estático para que la posición
    # renderizada coincida siempre con el collider de Bullet.
    mecha_body = pybullet.createMultiBody(
        baseMass=0.0,
        baseCollisionShapeIndex=mecha_shape,
        baseVisualShapeIndex=-1,
        basePosition=[position[0], position[1], position[2]],
    )

    self.m_StaticBodies['mecha_' + str(id)] = {
        "node": mecha_node,
        "body": mecha_body,
        "available": True
    }

  def getMechaContactPoints(self, body, mecha_name):
    return pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies[mecha_name]['body'])       if self.m_StaticBodies[mecha_name]['available'] else []
  
  def collisionMecha(self, mecha_name):
    print("Colisión con la mecha " + mecha_name)
    self.highlight_mecha(mecha_name)
    self.m_StaticBodies[mecha_name]['available'] = False
    self.printScore()

  def checkBocin(self, tejo_pos):
    x, y, z = tejo_pos  # Posición del tejo
    m0, m1, m2, m3 = self.mecha_positions  # Centro de las mechas
    y_tolerance = 0.10
    condition_x = x >= m2[0] and x <= m3[0]
    condition_y = y >= m1[0] - y_tolerance and y <= m1[1] + y_tolerance
    condition_z = z >= m1[2] and z <= m0[2]
    # Permite un margen de error (radio de bocin) para la mecha 1

    return condition_x  and condition_z and condition_y

  def collisionBocin(self, name, tejo_pos):
    self.last_tejo_scored = int(name[5])
    if self.checkBocin(tejo_pos):
      print("BOCIN!!!!!!!!!!!!")
      return True
    print("No es bocin")
    return False
  
  def calculateScore(self, mecha, bocin):
    score = 0
    if mecha and bocin:
      self.moniona_sound.play()
      score = 9
    elif mecha:
      self.mecha_sound.play()
      score = 3
    elif bocin:
      self.bocin_sound.play()
      score = 6
    return score
  
  def printScore(self):
    print("Puntaje: " + str(self.score))
    
  def frameRenderingQueued(self, evt):
    r = super(PUJ_Ogre.BaseApplicationWithVTK, self).frameRenderingQueued(evt)
    if self.paused:
      return r
    dt = evt.timeSinceLastFrame
    pybullet.setTimeStep(dt)
    pybullet.stepSimulation()

    tejo_to_remove = []
    for name, info in self.m_MovingBodies.items():
        node = info["node"]
        body = info["body"]
        aliveTime = info["aliveTime"]
        # Obtener posición real
        pos, orn = pybullet.getBasePositionAndOrientation(body)
        # print("pos --> ", pos)
        node.setPosition(pos)
        node.setOrientation(Ogre.Quaternion(orn[3], orn[0], orn[1], orn[2]))

        # Detectar colisión con la cancha
        contacts = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['tejo_wedge'])
        contacts_mecha_0 = self.getMechaContactPoints(body, 'mecha_0')
        contacts_mecha_1 = self.getMechaContactPoints(body, 'mecha_1')
        contacts_mecha_2 = self.getMechaContactPoints(body, 'mecha_2')
        contacts_mecha_3 = self.getMechaContactPoints(body, 'mecha_3')
        contacts_ground = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['ground'])
        contacts_field = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['tejo_wedge'])
        contacts_cylinder = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['tejo_cylinder'])

        if len(contacts_cylinder) > 0:
            self.wood_sound.play()

        if len(contacts_ground) > 0:
            self.metal_sound.play()
            pybullet.resetBaseVelocity(body, [0,0,0], [0,0,0])
            pybullet.changeDynamics(body, -1, activationState=pybullet.ACTIVATION_STATE_SLEEP, mass=0.0)
        
        mecha = len(contacts_mecha_0) + len(contacts_mecha_1) + len(contacts_mecha_2) + len(contacts_mecha_3) > 0

        if len(contacts_mecha_0) > 0:
          self.collisionMecha('mecha_0')
        if len(contacts_mecha_1) > 0:
          self.collisionMecha('mecha_1')
        if len(contacts_mecha_2) > 0:
          self.collisionMecha('mecha_2')
        if len(contacts_mecha_3) > 0:
          self.collisionMecha('mecha_3')
        mecha = True if len(contacts_mecha_0) + len(contacts_mecha_1) + len(contacts_mecha_2) + len(contacts_mecha_3) > 0 else False
        
        bocin = False
        if (len(contacts_field) > 0 and int(name[5]) > self.last_tejo_scored ):
          bocin = self.collisionBocin(name, pos)



        score = self.calculateScore(mecha, bocin)
        if score > 0:
          print("Score throw --> ", score)
          self.score += score
          self.printScore()
        
        if len(contacts) > 0:
          pybullet.resetBaseVelocity(body, [0,0,0], [0,0,0])
          pybullet.changeDynamics(body, -1, activationState=pybullet.ACTIVATION_STATE_SLEEP, mass=0.0)
        now = time.time()
        if now - aliveTime > 10:
            print("Tejo eliminado")
            pybullet.removeBody(body)
            node.removeAndDestroyAllChildren()
            self.m_SceneMgr.destroySceneNode(node)
            tejo_to_remove.append(name)

    for name in tejo_to_remove:
        del self.m_MovingBodies[name]
        self.m_SceneMgr.destroyManualObject(name)
        
    return r
    


  def zoomIn(self):
    self.m_CamMan.getCamera().setPosition(0, 1.7, -3)
    self.m_CamMan.getCamera().lookAt(Ogre.Vector3(self.wx, self.wy, self.wz), Ogre.Node.TS_WORLD)

  def zoomOut(self):
    self.m_CamMan.getCamera().setPosition(0, 1.7, 5)
    self.m_CamMan.getCamera().lookAt(Ogre.Vector3(0, 1.7, 0), Ogre.Node.TS_WORLD)

  def lateralView(self):
    self.m_CamMan.getCamera().setPosition(-5, 1.7, 0)
    self.m_CamMan.getCamera().lookAt(Ogre.Vector3(self.wx, self.wy, self.wz), Ogre.Node.TS_WORLD)

  def resetGame(self):
    self.score = 0
    self.printScore()
    tejo_to_remove = []
    for name, info in self.m_MovingBodies.items():
      body = info["body"]
      node = info["node"]
      pybullet.removeBody(body)
      node.removeAndDestroyAllChildren()
      self.m_SceneMgr.destroySceneNode(node)
      tejo_to_remove.append(name)

    for name in tejo_to_remove:
      del self.m_MovingBodies[name]
      self.m_SceneMgr.destroyManualObject(name)

    for i in range(4):
      self.m_StaticBodies['mecha_' + str(i)]['available'] = True
      man = self.m_SceneMgr.getManualObject("mecha_" + str(i))
      man.setMaterialName(0, "red_material")

  def throwTejo(self, duration):
    self.tejo_count+=1
    # 1. Cámara
    cam = self.m_CamMan.getCamera()
    cam_pos = cam._getDerivedPosition()
    cam_orient = cam._getDerivedOrientation()

    # 2. Posición inicial del tejo (un poquito delante de la cámara)
    forward = cam_orient * Ogre.Vector3(0, 0, -1)
    forward.normalise()
    spawn_offset = 0.5
    spawn_pos = cam_pos + forward * spawn_offset

    x_position, y_position, z_position = spawn_pos.x, spawn_pos.y, spawn_pos.z

    # 3. Crear nodo Ogre
    name = f"tejo_{self.tejo_count}"

    tejo_node = self._createManualObject(
        self._cone(0.08, 0.03, 1.3),
        name,
        "tejo_metal"
    )

    tejo_node.setPosition(spawn_pos)

    # 4. Collider PyBullet
    mass = 0.017
    tejo_shape = pybullet.createCollisionShape(
        pybullet.GEOM_SPHERE, radius=0.03 * 0.5
    )

    tejo_body = pybullet.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=tejo_shape,
        baseVisualShapeIndex=-1,
        basePosition=[x_position, y_position, z_position],
        baseOrientation=[cam_orient.x, cam_orient.y, cam_orient.z, cam_orient.w]
    )

    pybullet.changeDynamics(
        tejo_body, -1,
        restitution=0.5,
        lateralFriction=0.6
    )

    # 5. Velocidad según orientación de la cámara
    base_speed = random.uniform(10.0, 12.0)
    power = max(0.3, min(duration, 1.5))
    speed = base_speed * power

    arc = random.uniform(0.1, 0.3)  # arco hacia arriba
    dir_with_arc = Ogre.Vector3(forward.x, forward.y + arc, forward.z)
    dir_with_arc.normalise()

    vx = dir_with_arc.x * speed
    vy = dir_with_arc.y * speed
    vz = dir_with_arc.z * speed

    pybullet.resetBaseVelocity(
        tejo_body,
        linearVelocity=[vx, vy, vz]
    )

    self.m_MovingBodies[name] = {
        "node": tejo_node,
        "body": tejo_body,
        "aliveTime": time.time()
    }

  

# end class

"""
"""
def main( argv ):
  app = MovingSpheres( )
  app.go( )
# end def

if __name__ == '__main__':
  main( sys.argv )
# end def

## eof - MovingSpheres.py
