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
  '''
  '''
  def __init__( self ):
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
    pybullet.connect( pybullet.DIRECT )
    pybullet.setGravity( 0, -9.8, 0 )

    # Get root and create scene managerf
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )

    # Configure camera
    self._createCamera(
      top_speed = 3,
      position = [ 0.00, 1.70, 5.0 ],
      look_at = [ 0, 1.70, 0 ],
      background = [ 0.9, 0.75, 0.5 ],
      cam_style = OgreBites.CS_FREELOOK
      )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_DIRECTIONAL )
    light.setDirection( [ 0, -1, 0 ] )

    # A ground
    self._ground( 'ground', [ -4.00, 4.00, -4.00, 4.00 ] )
    ground_bullet = pybullet.createCollisionShape( pybullet.GEOM_PLANE, planeNormal = [ 0, 1, 0 ] )
    ground_body = pybullet.createMultiBody( 0, ground_bullet, -1, [ 0, 0, 0 ] )
    pybullet.changeDynamics( ground_body, -1, restitution = -0.5, lateralFriction = 20 )
    self.m_StaticBodies[ 'ground' ] = ground_body

    # Load billiards
    # red_ball = self._createManualObject(
    #   self._sphere( 0.057, 50, 50 ), 'red_ball', 'red_material'
    #   )
    # red_ball.setPosition( 60, 0, 0 )
    # red_ball_bullet = pybullet.createCollisionShape( pybullet.GEOM_SPHERE, radius = 0.057 )
    # red_ball_body = pybullet.createMultiBody( 0.017, red_ball_bullet, -1, [ 2, 1, 0 ] )
    # pybullet.changeDynamics( red_ball_body, -1, restitution = 0.5, lateralFriction = 0.3 )
    # self.m_MovingBodies[ 'red_ball' ] = ( red_ball, red_ball_body )
   
    pit_incline_deg = 15.0

    theta_x = math.radians(pit_incline_deg)  # inclinación
    theta_y = math.radians(-90.0)
    theta_z = math.radians(self.field_rotation_deg)

    # qx, qy, qz, qw = pybullet.getQuaternionFromEuler([0, theta_y, theta_z])

    qy = pybullet.getQuaternionFromEuler([0, theta_y, 0])
    qz = pybullet.getQuaternionFromEuler([0, 0, theta_z])

    # Multiplicación para aplicar primero Y, después Z
    q = pybullet.multiplyTransforms([0,0,0], qy, [0,0,0], qz)[1]
    qx, qy, qz, qw = q 

    # posición de la caja en el mundo

    wedge_node = self._createManualObject(
        self._box(self.base, self.height,self.length),
        "tejo_wedge",
        "debug_material"
    )

    wedge_node.setPosition(self.wx, self.wy, self.wz)
    wedge_node.setOrientation( Ogre.Quaternion(qx, qy, qz, qw) )
    wedge_node.setVisible(True)

    # collider como BOX + rotación (no wedge)
    wedge_shape = pybullet.createCollisionShape(
        pybullet.GEOM_BOX,
        halfExtents=[self.base * 0.5, self.height * 0.5, self.length * 0.5]
    )

    # theta = math.radians(-pit_incline_deg)
    # qx = math.sin(theta / 2.0)
    # qw = math.cos(theta / 2.0)

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

    self.m_StaticBodies['tejo_wedge'] = wedge_body
    

    self.createAllMechas()

    # de createCollisionShape
    # box_node = self._createManualObject(
    #     self._box(base, height,length),
    #     "tejo_wedge",
    #     "debug_material"
    # )

    # box_node.setPosition(wx, wy, wz)
    # box_node.setOrientation( Ogre.Quaternion(qrx, qry, qrz, qrw) )
    # box_node.setVisible(True)

    # Finish pybullet configuration
    pybullet.setPhysicsEngineParameter( numSolverIterations = 10 )
  # end def

  def createAllMechas(self):
    angle = math.radians(self.field_rotation_deg)
    mov_y = math.sin(angle) * self.bocin_gap
    mov_z = math.cos(angle) * self.bocin_gap 
    initial_position = [self.wx, self.wy + (self.height / 2) - self.deep_hole_proportion, self.wz]
    
    positions = [
      [initial_position[0] , initial_position[1] + mov_y, initial_position[2] + mov_z],
      [initial_position[0] , initial_position[1] - mov_y, initial_position[2] - mov_z],
      [initial_position[0] - self.bocin_gap, initial_position[1], initial_position[2] ],
      [initial_position[0] + self.bocin_gap, initial_position[1], initial_position[2] ]
    ]
    for i in range(len(positions)):
      self.createMecha(positions[i], i )

  def highlight_mecha(self, mecha_name):

    # Obtener el objeto adjunto (ManualObject)
    man = self.m_SceneMgr.getManualObject(mecha_name)

    man.setMaterialName(0, "black_material")

  def createMecha(self, position, id):
    pit_incline_deg = 15.0

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
  '''
  '''
  def frameRenderingQueued(self, evt):
    r = super(PUJ_Ogre.BaseApplicationWithVTK, self).frameRenderingQueued(evt)

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
        node.setPosition(pos)
        node.setOrientation(Ogre.Quaternion(orn[3], orn[0], orn[1], orn[2]))

        # Detectar colisión con la cancha
        contacts = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['tejo_wedge'])
        contacts_mecha_0 = self.getMechaContactPoints(body, 'mecha_0')
        contacts_mecha_1 = self.getMechaContactPoints(body, 'mecha_1')
        contacts_mecha_2 = self.getMechaContactPoints(body, 'mecha_2')
        contacts_mecha_3 = self.getMechaContactPoints(body, 'mecha_3')
        contacts_ground = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['ground'])

        if len(contacts_ground) > 0:
            print("Colisión con el suelo")
            pybullet.resetBaseVelocity(body, [0,0,0], [0,0,0])
            pybullet.changeDynamics(body, -1, activationState=pybullet.ACTIVATION_STATE_SLEEP, mass=0.0)
        collision_count = 0
        if len(contacts_mecha_0) > 0:
            collision_count += 1
            print("Colisión con la mecha 0")
            self.highlight_mecha('mecha_0')
            self.m_StaticBodies['mecha_0']['available'] = False
        if len(contacts_mecha_1) > 0:
            collision_count += 1
            print("Colisión con la mecha 1")
            self.highlight_mecha('mecha_1')
            self.m_StaticBodies['mecha_1']['available'] = False
        if len(contacts_mecha_2) > 0:
            collision_count += 1
            print("Colisión con la mecha 2")
            self.highlight_mecha('mecha_2')
            self.m_StaticBodies['mecha_2']['available'] = False
        if len(contacts_mecha_3) > 0:
            collision_count += 1
            print("Colisión con la mecha 3")
            self.highlight_mecha('mecha_3')
            self.m_StaticBodies['mecha_3']['available'] = False
        if len(contacts) > 0:
            # Quieto
            pybullet.resetBaseVelocity(body, [0,0,0], [0,0,0])
            pybullet.changeDynamics(body, -1, activationState=pybullet.ACTIVATION_STATE_SLEEP, mass=0.0)
        if not (collision_count > 0):
            now = time.time()
            if now - aliveTime > 10:
                print("Tejo eliminado")
                pybullet.removeBody(body)
                node.removeAndDestroyAllChildren()
                self.m_SceneMgr.destroySceneNode(node)
                tejo_to_remove.append(name)

    for name in tejo_to_remove:
        print("Eliminando tejo: ", name)
        del self.m_MovingBodies[name]
        self.m_SceneMgr.destroyManualObject(name)
        
    return r
    


    # for k in self.m_MovingBodies:
    #   node, nId = self.m_MovingBodies[ k ]
    #   pos, orn = pybullet.getBasePositionAndOrientation( nId )
    #   node.setPosition( pos )
    #   node.setOrientation( Ogre.Quaternion( orn[ 3 ], orn[ 0 ], orn[ 1 ], orn[ 2 ] ) )
    # end for

    return r
  # end def
  def throwTejo(self, duration=None):
    print("Throwing tejo")
    object_id = len(self.m_MovingBodies)
    name = 'red_ball_' + str(object_id)
    # delete all manual objects with name 'red_ball_'
    if self.m_SceneMgr.hasManualObject(name):
        self.m_SceneMgr.destroyManualObject(name)


    # Nodo visual (Ogre)
    red_ball = self._createManualObject(
        self._sphere(0.057, 50, 50),
        name,
        'red_material'
    )

    # Posición inicial del tejo
    cam = self.m_CamMan.getCamera()
    cam_orient = cam._getDerivedOrientation()
    qx, qy, qz, qw = cam_orient
    world_pos = cam._getDerivedPosition()
    x_position = world_pos.x
    y_position = 1.7
    z_position = world_pos.z
    red_ball.setPosition(x_position, y_position, z_position)

    # Collider (PyBullet)
    radius = self.length * self.mecha_proportion * 0.5
    red_ball_shape = pybullet.createCollisionShape(
        pybullet.GEOM_SPHERE,
        radius=radius
    )

    # Masa > 0 para que sea dinámico
    mass = max(random.uniform(0.3, 2.0), 0.1)

    red_ball_body = pybullet.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=red_ball_shape,
        baseVisualShapeIndex=-1,
        basePosition=[x_position, y_position, z_position],
        baseOrientation=[qx, qy, qz, qw]
    )

    pybullet.changeDynamics(
        red_ball_body, -1,
        restitution=0.5,
        lateralFriction=0.6
    )

    # 👉 Velocidad inicial tipo "lanzamiento de tejo"
    # vz = - duration * 5    # un poco de lado
    vz = random.uniform(-12.0, -10.0)
    vy = random.uniform(2.0, 6.0)       # arco hacia arriba
    vx = 0     # hacia la cancha (z negativa)
 
    pybullet.resetBaseVelocity(
        red_ball_body,
        linearVelocity=[vx, vy, vz]
    )

    # Guardar solo lo que de verdad usamos luego
    self.m_MovingBodies[name] = {
        "node": red_ball,
        "body": red_ball_body,
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
