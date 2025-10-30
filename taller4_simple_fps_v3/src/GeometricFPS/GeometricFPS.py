## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, random, sys
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, '../../lib' ) )
sys.path.append( imp_dir )
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites
from FPSListener import *


"""
"""
class GeometricFPS( PUJ_Ogre.BaseApplicationWithVTK ):

  '''
  '''
  m_Ground = None
  m_Camera = None
  m_CamMan = None
  m_BadGuys = None
  m_AliveBadGuys = None
  m_AvailableNames = None
  m_Bullets = None
  m_AliveBullets = None

  '''
  '''
  def __init__( self ):
    super( GeometricFPS, self ).__init__( 'GeometricFPS v0.1', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )
  # end def

  def setup( self ):
    self.m_Listener = FPSListener( self.getRoot( ), self )
    super( GeometricFPS, self ).setup( )

  def shootBullet( self ):
    if not self.m_AvailableNames['bullet']:
      print("No bullets available to shoot.")
      return
    name = self.m_AvailableNames['bullet'].pop( 0 )
    print('Shooting bullet: ' + name)
    print(self.m_Bullets['bullet'][0])
    print(self.m_Bullets['bullet'][1])
    print(self.m_Bullets['bullet'][3])
    node = self._createManualObject(
        self.m_Bullets['bullet'][ 5 ], name, self.m_Bullets['bullet'][ 0 ]
        )
    pos = node.getAttachedObject( 0 ).getBoundingBox( ).getMinimum( )
    qos = Ogre.Vector3(
      random.uniform( self.m_Ground[ 0 ], self.m_Ground[ 1 ] ),
      pos.y * -1.0,
      random.uniform( self.m_Ground[ 2 ], self.m_Ground[ 3 ] )
      )
    # cameraPosition = self.m_CamMan.getCamera( ).getTarget( )

    print('Camera target: ' , self.m_CamMan.getCamera( ).getOrientation())

    # d = distance in front of the camera (in world units)
    d = 5.0

    cam = self.m_CamMan.getCamera()
    cam_node = cam.getParentSceneNode()

    cam_pos = cam.getPosition()

    print('Camera position: ' , cam_pos)
    
    cam_orient = cam.getOrientation()
    cam_forward = cam_orient * Ogre.Vector3(0, 0, -1)
    cam_forward.normalise()
    
    # World position d units in front of the camera (camera looks along local -Z)
    target_pos = cam_pos + cam_forward * d

    # Move your object
    node.setPosition(target_pos)
    # If you want it to face the same way as the camera:
    node.setOrientation(cam_orient)
    node.vector =  ( ( node.getPosition( ) - cam_pos ).normalisedCopy( ) ) * self.m_Bullets['bullet'][3]

    # node.setPosition( cameraPosition[0], cameraPosition[1], cameraPosition[2] - 5)
    self.m_AliveBullets.append({'node': node, 'name': name})

  '''
  '''
  def _loadScene( self ):

    # Some objects
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )
    res_mgr = Ogre.ResourceGroupManager.getSingleton( )
    mesh_mgr = Ogre.MeshManager.getSingleton( )

    # Read scene descriptor
    scene_stream = res_mgr.openResource( 'scene.txt', 'General' )
    scene = dict( [ ( s.split( )[ 0 ], s.split( )[ 1 : ] ) for s in scene_stream.getAsString( ).splitlines( ) ] )
    scene_stream.close( )

    # Floor_limits
    self.m_Ground = [ -100.0, 100.0, -100.0, 100.0 ]
    if 'ground' in scene:
      self.m_Ground = [ float( v ) for v in scene[ 'ground' ] ]
    # end if
    self._ground( 'ground', self.m_Ground )

    # Camera
    self.m_Camera = [ 1e-3, 1.7, 1.0 ]
    if 'camera' in scene:
      self.m_Camera = [ float( v ) for v in scene[ 'camera' ] ]
    # end if
    cam = self._camera( self.m_Ground, self.m_Camera )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_POINT )
    light.setDiffuseColour( 1, 1, 1 )
    light_node = root_node.createChildSceneNode( )
    light_node.setPosition(
      ( self.m_Ground[ 1 ] + self.m_Ground[ 0 ] ) * 0.5,
      500 * self.m_Camera[ 1 ],
      ( self.m_Ground[ 3 ] + self.m_Ground[ 2 ] ) * 0.5
      )
    light_node.attachObject( light )

    # Viewport
    skycolor = [ 1, 1, 1 ]
    if 'skycolor' in scene:
      skycolor = [ float( v ) for v in scene[ 'skycolor' ] ]
    # end if
    vp = win.addViewport( cam )
    vp.setBackgroundColour( skycolor )

    # Load 'bad guys'
    self.m_BadGuys = { 'sphere' : None, 'cylinder' : None, 'cone' : None }
    self.m_Bullets = { 'bullet' : None }
    self.m_AliveBullets = []
    self.m_AliveBadGuys = { 'sphere' : [], 'cylinder' : [], 'cone' : [] }
    self.m_AvailableNames = { 'sphere' : [], 'cylinder' : [], 'cone' : [], 'bullet' : [] }
    if 'sphere' in scene:
      bad_guy_material = scene[ 'sphere' ][ -4 ]
      bad_guy_stamina = int( scene[ 'sphere' ][ -3 ] )
      bad_guy_spawn_prob = float( scene[ 'sphere' ][ -2 ] )
      bad_guy_max = int( scene[ 'sphere' ][ -1 ] )
      self.m_BadGuys[ 'sphere' ] = [ bad_guy_material, bad_guy_stamina, bad_guy_spawn_prob, bad_guy_max, self._sphere( float( scene[ 'sphere' ][ 0 ] ), 100, 100 ), float( scene[ 'sphere' ][ 0 ] ) ]
      self.m_AvailableNames[ 'sphere' ] = [ 'sphere_' + str( i ) for i in range( bad_guy_max ) ]
    if 'bullet' in scene:
      print('Loading bullet parameters')
      print(scene[ 'bullet' ]) 
      #bullet 0.1 bullet 1 15 100 5
      bullet_material = scene[ 'bullet' ][ -5 ]
      bullet_damage = int( scene[ 'bullet' ][ -4 ] )
      bullet_max = int( scene[ 'bullet' ][ -3 ] )
      bullet_speed = float( scene[ 'bullet' ][ -2 ] )
      bullet_time_spawn = int( scene[ 'bullet' ][ -1 ] ) 
      self.m_Bullets[ 'bullet' ] = [ bullet_material, bullet_damage, bullet_max, bullet_speed, bullet_time_spawn, self._sphere( float( scene[ 'bullet' ][ 0 ] ), 100, 100 ), float( scene[ 'bullet' ][ 0 ] ) ]
      self.m_AvailableNames[ 'bullet' ] = [ 'bullet_' + str( i ) for i in range( bullet_max ) ] 

    # end if
  # end def

  '''
  '''
  # evt tiene un parametro para el tiempo entre frames
  def frameRenderingQueued( self, evt ):
    r = super( PUJ_Ogre.BaseApplication, self ).frameRenderingQueued( evt )

    # Create bad guys
    for k in self.m_BadGuys:
      if not self.m_BadGuys[ k ] is None:
        n_max = self.m_BadGuys[ k ][ 3 ]
        n_bad = len( self.m_AliveBadGuys[ k ] )
        p = random.uniform( 0, 1 )
        if p <= self.m_BadGuys[ k ][ 2 ] and n_bad < n_max:
          if len( self.m_AvailableNames[ k ] ) > 0:
            name = self.m_AvailableNames[ k ].pop( 0 )
            node = self._createManualObject(
              self.m_BadGuys[ k ][ 4 ], name, self.m_BadGuys[ k ][ 0 ]
              )
            pos = node.getAttachedObject( 0 ).getBoundingBox( ).getMinimum( )
            qos = Ogre.Vector3(
              random.uniform( self.m_Ground[ 0 ], self.m_Ground[ 1 ] ),
              pos.y * -1.0,
              random.uniform( self.m_Ground[ 2 ], self.m_Ground[ 3 ] )
              )
            node.setPosition( qos )
            self.m_AliveBadGuys[ k ] += [ {
              'node': node,
              'radius': self.m_BadGuys[ k ][ -1 ],
              'stamina': float(self.m_BadGuys[ k ][ 1 ]),
              'name': name
            } ]
          # end if
        # end if
      # end if
    # end for

    # Get camera position and force it to the ground
    pos = self.m_CamMan.getCamera( ).getPosition( )
    pos.y = self.m_Camera[ 1 ]
    self.m_CamMan.getCamera( ).setPosition( pos )

    # Move bad guys
    for k in self.m_AliveBadGuys:
      for n in self.m_AliveBadGuys[ k ]:
        d = ( ( pos - n['node'].getPosition( ) ).normalisedCopy( ) ) * 1e-1
        n['node'].translate( d )
      # end for
    # end for
    # Move bullets
    for k in self.m_AliveBullets:
      node = k['node']
      node.translate( node.vector)
    # end for

    bullets_to_remove = []
    for bullet in self.m_AliveBullets:
      for bad_guy_type in self.m_AliveBadGuys:
        bad_guys_to_remove = []
        for bad_guy in self.m_AliveBadGuys[bad_guy_type]:
          if bullet['node'].getPosition().distance(bad_guy['node'].getPosition()) < self.m_BadGuys[bad_guy_type][-1]:
            bad_guy['stamina'] -= self.m_Bullets['bullet'][1]
            bullets_to_remove.append(bullet)
            if bad_guy['stamina'] <= 0:
              print('Destroying bad guy: ', bad_guy['node'].getName())
              bad_guys_to_remove.append(bad_guy)
            break  # end if
        # end for
        for bad_guy in bad_guys_to_remove:
          node = bad_guy['node']
          self.m_SceneMgr.destroySceneNode(node)
          self.m_AvailableNames[bad_guy_type].append(bad_guy['name'])
          self.m_AliveBadGuys[bad_guy_type].remove(bad_guy)
          self.m_SceneMgr.destroyManualObject(bad_guy['name'])
        # end for
    for bullet in bullets_to_remove:
      node = bullet['node']
      self.m_SceneMgr.destroySceneNode(node)
      self.m_AvailableNames['bullet'].append(bullet['name'])
      self.m_AliveBullets.remove(bullet)
      self.m_SceneMgr.destroyManualObject(bullet['name'])
    # end for
    return r
  # end def

  '''
  '''
  def _ground( self, i, l ):
    c = [ ( l[ 1 ] + l[ 0 ] ) * 0.5, 0.0, ( l[ 3 ] + l[ 2 ] ) * 0.5 ]
    p = Ogre.Plane( 0, 1, 0, 0 )
    m = Ogre.MeshManager.getSingleton( ).createPlane(
      i, 'General', p,
      l[ 1 ] - l[ 0 ],
      l[ 3 ] - l[ 2 ],
      20, 20, True, 1, 5, 5, [ 0, 0, 1 ]
      )
    e = self.m_SceneMgr.createEntity( i, i )
    e.setMaterialName( i )
    n = self.m_SceneMgr.getRootSceneNode( ).createChildSceneNode( )
    n.attachObject( e )
    n.setPosition( c )
  # end def

  # def bulletHit( self, evt ):
  #   if 'bullet' in scene:
  #     bad_guy_material = scene[ 'sphere' ][ -4 ]
  #     bad_guy_stamina = int( scene[ 'sphere' ][ -3 ] )
  #     bad_guy_spawn_prob = float( scene[ 'sphere' ][ -2 ] )
  #     bad_guy_max = int( scene[ 'sphere' ][ -1 ] )
  #     self.m_BadGuys[ 'sphere' ] = [ bad_guy_material, bad_guy_stamina, bad_guy_spawn_prob, bad_guy_max, self._sphere( float( scene[ 'sphere' ][ 0 ] ), 100, 100 ) ]
  #     self.m_AvailableNames[ 'sphere' ] = [ 'sphere_' + str( i ) for i in range( bad_guy_max ) ]

  '''
  '''
  def _camera( self, l, p ):
    cam = self.m_SceneMgr.createCamera( 'camera' )
    cam.setNearClipDistance( p[ 0 ] )
    cam.setAutoAspectRatio( True )

    cam_node = self.m_SceneMgr.getRootSceneNode( ).createChildSceneNode( )
    cam_node.setPosition( l[ 0 ], p[ 1 ], l[ 1 ] )
    cam_node.lookAt( [ 0, 0, 0 ], Ogre.Node.TS_WORLD )
    cam_node.attachObject( cam )

    self.m_CamMan = OgreBites.CameraMan( cam_node )
    self.m_CamMan.setStyle( OgreBites.CS_FREELOOK )
    self.m_CamMan.setTopSpeed( 10 )
    self.m_CamMan.setFixedYaw( True )
    self.addInputListener( self.m_CamMan )

    return cam
  # end def


# end class

"""
"""
def main( argv ):
  app = GeometricFPS( )
  app.go( )
# end def

if __name__ == '__main__':
  main( sys.argv )
# end def

## eof - GeometricFPS.py
