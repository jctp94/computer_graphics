## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, sys
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, './lib' ) )
sys.path.append( imp_dir )
import pybullet, Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites
import random
import math

from TejoListener import *

"""
"""
class MovingSpheres( PUJ_Ogre.BaseApplicationWithVTK ):

  '''
  '''
  m_MovingBodies = {}
  m_StaticBodies = {}

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

    # Get root and create scene manager
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )

    # Configure camera
    self._createCamera(
      top_speed = 3,
      position = [ 0, 1.70, 5.00 ],
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
    pybullet.changeDynamics( ground_body, -1, restitution = 1, lateralFriction = 0.8 )
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
    base = 1.0
    height = 0.2
    length = 2.0
    pit_incline_deg = 15.0

    wedge_node = self._createManualObject(
        self._wedge(base=base, height=height, length=length),
        'tejo_wedge',
        'red_material'
    )

    # posición de la caja en el mundo
    wx, wy, wz = 0.0, 0.5, -2.0
    wedge_node.setPosition(wx, wy, wz)
    wedge_node.pitch(Ogre.Radian(math.radians(-pit_incline_deg)))

    # collider como BOX + rotación (no wedge)
    wedge_shape = pybullet.createCollisionShape(
        pybullet.GEOM_BOX,
        halfExtents=[base * 0.5, height * 0.5, length * 0.5]
    )

    theta = math.radians(-pit_incline_deg)
    qx = math.sin(theta / 2.0)
    qw = math.cos(theta / 2.0)

    wedge_body = pybullet.createMultiBody(
        baseMass=0.0,  # estático
        baseCollisionShapeIndex=wedge_shape,
        baseVisualShapeIndex=-1,
        basePosition=[wx, wy, wz],
        baseOrientation=[qx, 0.0, 0.0, qw]
    )

    pybullet.changeDynamics(
        wedge_body, -1,
        restitution=0.5,
        lateralFriction=0.6
    )

    self.m_StaticBodies['tejo_wedge'] = wedge_body

       # de createCollisionShape
    box_node = self._createManualObject(
        self._box(base, height, length),
        "debug_box",
        "debug_material"
    )

    box_node.setPosition(wx, wy, wz)
    box_node.setOrientation( Ogre.Quaternion(qw, qx, 0, 0) )
    box_node.setVisible(True)

    for i in range(1):
      name = f"red_ball_{i}"

      # Nodo visual
      red_ball = self._createManualObject(
          self._sphere(0.057, 50, 50),
          name,
          "red_material"
      )

      x0 = 0.0
      y0 = 1.2
      z0 = 3.0   # por ejemplo, delante de la rampa
      red_ball.setPosition(x0, y0, z0)

      # Collider de PyBullet
      radius = 0.057
      col_id = pybullet.createCollisionShape(
          pybullet.GEOM_SPHERE,
          radius=radius
      )

      mass = 0.5
      body_id = pybullet.createMultiBody(
          baseMass=mass,
          baseCollisionShapeIndex=col_id,
          baseVisualShapeIndex=-1,
          basePosition=[x0, y0, z0]
      )

      pybullet.changeDynamics(
          body_id, -1,
          restitution=0.3,
          lateralFriction=0.8
      )

      # Velocidad inicial tipo “lanzamiento de tejo”
      vx = random.uniform(-1.0, 1.0)         # un poquito de lado
      vy = random.uniform(2.0, 5.0)          # arco
      vz = random.uniform(-8.0, -5.0)        # hacia la rampa

      pybullet.resetBaseVelocity(
          body_id,
          linearVelocity=[vx, vy, vz]
      )

      self.m_MovingBodies[name] = {
          "node": red_ball,
          "body": body_id,
      }
    # Finish pybullet configuration
    pybullet.setPhysicsEngineParameter( numSolverIterations = 10 )
  # end def

  '''
  '''
  def frameRenderingQueued(self, evt):
    r = super(PUJ_Ogre.BaseApplicationWithVTK, self).frameRenderingQueued(evt)

    dt = evt.timeSinceLastFrame
    pybullet.setTimeStep(dt)
    pybullet.stepSimulation()

    for name, info in self.m_MovingBodies.items():
        node = info["node"]
        body = info["body"]

        # Obtener posición real
        pos, orn = pybullet.getBasePositionAndOrientation(body)
        node.setPosition(pos)
        node.setOrientation(Ogre.Quaternion(orn[3], orn[0], orn[1], orn[2]))

        # Detectar colisión con la cancha
        contacts = pybullet.getContactPoints(bodyA=body, bodyB=self.m_StaticBodies['tejo_wedge'])

        if len(contacts) > 0:
            # Quieto
            pybullet.resetBaseVelocity(body, [0,0,0], [0,0,0])
            pybullet.changeDynamics(body, -1, activationState=pybullet.ACTIVATION_STATE_SLEEP)

    return r
    


    # for k in self.m_MovingBodies:
    #   node, nId = self.m_MovingBodies[ k ]
    #   pos, orn = pybullet.getBasePositionAndOrientation( nId )
    #   node.setPosition( pos )
    #   node.setOrientation( Ogre.Quaternion( orn[ 3 ], orn[ 0 ], orn[ 1 ], orn[ 2 ] ) )
    # end for

    return r
  # end def
  def throwTejo(self):
    print("Throwing tejo")
    object_id = len(self.m_MovingBodies)
    name = 'red_ball_' + str(object_id)

    # Nodo visual (Ogre)
    red_ball = self._createManualObject(
        self._sphere(0.057, 50, 50),
        name,
        'red_material'
    )

    # Posición inicial del tejo
    x_position = 0.0
    y_position = 1.7
    z_position = 4.0
    red_ball.setPosition(x_position, y_position, z_position)

    # Collider (PyBullet)
    radius = 0.057
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
        basePosition=[x_position, y_position, z_position]
    )

    pybullet.changeDynamics(
        red_ball_body, -1,
        restitution=0.5,
        lateralFriction=0.6
    )

    # 👉 Velocidad inicial tipo "lanzamiento de tejo"
    vx = random.uniform(-1.0, 1.0)      # un poco de lado
    vy = random.uniform(2.0, 6.0)       # arco hacia arriba
    vz = random.uniform(-8.0, -5.0)     # hacia la cancha (z negativa)

    pybullet.resetBaseVelocity(
        red_ball_body,
        linearVelocity=[vx, vy, vz]
    )

    # Guardar solo lo que de verdad usamos luego
    self.m_MovingBodies[name] = {
        "node": red_ball,
        "body": red_ball_body,
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
