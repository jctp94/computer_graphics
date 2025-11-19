## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

from .BaseApplication import *
import vtk

"""
"""
class BaseApplicationWithVTK( BaseApplication ):

  '''
  '''
  def __init__( self, title, res_file ):
    super( BaseApplicationWithVTK, self ).__init__( title, res_file )
  # end def

  '''
  '''
  def _parametric_data( self, f, u, v ):
    s = vtk.vtkParametricFunctionSource( )
    s.SetParametricFunction( f )
    s.GenerateNormalsOn( )
    s.GenerateTextureCoordinatesOn( )
    s.SetUResolution( u )
    s.SetVResolution( v )
    s.Update( )

    mesh = s.GetOutput( )
    normals = mesh.GetPointData( ).GetAbstractArray( 'Normals' )
    textures = mesh.GetPointData( ).GetAbstractArray( 'Textures' )

    P = []
    N = []
    T = []
    for i in range( mesh.GetNumberOfPoints( ) ):
      P += [ ( mesh.GetPoint( i ) ) ]
      N += [ ( normals.GetTuple( i ) ) ]
      T += [ ( textures.GetTuple( i ) ) ]
    # end for

    C = []
    for i in range( mesh.GetNumberOfCells( ) ):
      C += [ [] ]
      cell = mesh.GetCell( i )
      for j in range( cell.GetNumberOfPoints( ) ):
        C[ -1 ] += [ cell.GetPointId( j ) ]
      # end for
    # end for

    return ( P, N, T, C )
  # end def

  '''
  '''
  def _sphere( self, r, u = 10, v = 10 ):
    f = vtk.vtkParametricEllipsoid( )
    f.SetXRadius( r )
    f.SetYRadius( r )
    f.SetZRadius( r )
    return self._parametric_data( f, u, v )
  # end def

  def _box(self, sx, sy, sz):
    """
    Crea una caja VTK de tamaño (sx, sy, sz)
    y la devuelve como (P, N, T, C) para _createManualObject.
    """
    import vtk

    # 1. Generar la caja con VTK
    c = vtk.vtkCubeSource()
    c.SetXLength(sx)
    c.SetYLength(sy)
    c.SetZLength(sz)
    c.Update()

    poly = c.GetOutput()

    # 2. Generar normales
    normals_gen = vtk.vtkPolyDataNormals()
    normals_gen.SetInputData(poly)
    normals_gen.ComputePointNormalsOn()
    normals_gen.Update()
    poly = normals_gen.GetOutput()

    pts     = poly.GetPoints()
    normals = poly.GetPointData().GetNormals()

    # 3. Generar coordenadas UV simples (basadas en X y Z)
    xmin, xmax, ymin, ymax, zmin, zmax = poly.GetBounds()
    dx = xmax - xmin if xmax > xmin else 1.0
    dz = zmax - zmin if zmax > zmin else 1.0

    P = []
    N = []
    T = []
    for i in range(pts.GetNumberOfPoints()):
        x, y, z = pts.GetPoint(i)
        P.append((x, y, z))

        if normals is not None:
            N.append(normals.GetTuple(i))
        else:
            N.append((0.0, 1.0, 0.0))

        # UV en 2D (importante: Ogre solo acepta 2 componentes)
        u = (x - xmin) / dx
        v = (z - zmin) / dz
        T.append((u, v))

    # 4. Celdas
    C = []
    for i in range(poly.GetNumberOfCells()):
        cell = poly.GetCell(i)
        ids = []
        for j in range(cell.GetNumberOfPoints()):
            ids.append(cell.GetPointId(j))
        C.append(ids)

    return (P, N, T, C)

  '''
  '''
  def _createManualObject( self, data, name, material ):

    P, N, T, C = data

    man = self.m_SceneMgr.createManualObject( name )
    man.begin( material, Ogre.RenderOperation.OT_TRIANGLE_LIST )

    for i in range( len( P ) ):
      man.position( P[ i ] )
      man.normal( N[ i ] )
      man.textureCoord( T[ i ] )
    # end for

    for i in range( len( C ) ):
      if len( C[ i ] ) == 3:
        man.triangle(
            C[ i ][ 0 ], C[ i ][ 1 ], C[ i ][ 2 ]
            )
      elif len( C[ i ] ) == 4:
        man.quad( C[ i ][ 0 ], C[ i ][ 1 ], C[ i ][ 2 ], C[ i ][ 3 ] )
      # end if
    # end for

    man.end( )
    node = self.m_SceneMgr.getRootSceneNode( ).createChildSceneNode( )
    node.attachObject( man )
    return node
  # end def

  def _wedge(self, base=1.0, height=1.0, length=1.0):
    """
    Crea un wedge (prisma triangular) y lo devuelve en el formato
    (P, N, T, C) que usa _sphere.
    - base: tamaño en X de la base triangular
    - height: tamaño en Y (altura del triángulo)
    - length: largo en Z (profundidad del prisma)
    """

    # 1. Puntos del wedge
    points = vtk.vtkPoints()
    # Triángulo inferior (z = 0)
    points.InsertNextPoint(0.0,      0.0,     0.0)       # P0
    points.InsertNextPoint(base,     0.0,     0.0)       # P1
    points.InsertNextPoint(0.0,   height,     0.0)       # P2
    # Triángulo superior (z = length)
    points.InsertNextPoint(0.0,      0.0,  length)       # P3
    points.InsertNextPoint(base,     0.0,  length)       # P4
    points.InsertNextPoint(0.0,   height,  length)       # P5

    # 2. Celda wedge
    wedge = vtk.vtkWedge()
    wedge.GetPointIds().SetId(0, 0)
    wedge.GetPointIds().SetId(1, 1)
    wedge.GetPointIds().SetId(2, 2)
    wedge.GetPointIds().SetId(3, 3)
    wedge.GetPointIds().SetId(4, 4)
    wedge.GetPointIds().SetId(5, 5)

    cx = base * 0.5
    cy = height * 0.5
    cz = length * 0.5
    for i in range(points.GetNumberOfPoints()):
        x, y, z = points.GetPoint(i)
        points.SetPoint(i, x - cx, y - cy, z - cz)


    # 3. UnstructuredGrid
    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(wedge.GetCellType(), wedge.GetPointIds())

    # 4. Pasar a superficie
    geom = vtk.vtkGeometryFilter()
    geom.SetInputData(ugrid)
    geom.Update()
    poly = geom.GetOutput()

    # 5. Normales
    normals_gen = vtk.vtkPolyDataNormals()
    normals_gen.SetInputData(poly)
    normals_gen.ComputePointNormalsOn()
    normals_gen.ComputeCellNormalsOff()
    normals_gen.Update()
    poly = normals_gen.GetOutput()

    pts     = poly.GetPoints()
    normals = poly.GetPointData().GetNormals()

    # Bounds para generar UVs simples
    xmin, xmax, ymin, ymax, zmin, zmax = poly.GetBounds()
    dx = xmax - xmin if xmax > xmin else 1.0
    dz = zmax - zmin if zmax > zmin else 1.0

    P = []
    N = []
    T = []
    for i in range(pts.GetNumberOfPoints()):
        x, y, z = pts.GetPoint(i)
        P.append((x, y, z))

        if normals is not None:
            N.append(normals.GetTuple(i))
        else:
            N.append((0.0, 1.0, 0.0))

        # ✅ UV 2D, mapeando X y Z al rango [0,1]
        u = (x - xmin) / dx
        v = (z - zmin) / dz
        T.append((u, v))   # 👈 solo 2 componentes

    C = []
    for i in range(poly.GetNumberOfCells()):
        cell = poly.GetCell(i)
        ids = []
        for j in range(cell.GetNumberOfPoints()):
            ids.append(cell.GetPointId(j))
        C.append(ids)

    return (P, N, T, C)

# end class

## eof - BaseApplicationWithVTK.py
