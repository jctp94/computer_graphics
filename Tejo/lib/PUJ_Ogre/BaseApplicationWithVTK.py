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


  def _cone(self, height, radius, truncate_ratio=1.3):
    """
    Crea un cono truncado con VTK
    
    Args:
        height: altura total del cono
        radius: radio de la base
        truncate_ratio: fracción de la altura donde hacer el corte (0.0-1.0)
                       0.3 significa cortar al 30% desde el vértice
    """
    print(">> Creating truncated cone with height:", height, " radius:", radius)
    
    # Crear cono original
    cone = vtk.vtkConeSource()
    cone.SetHeight(height)
    cone.SetRadius(radius)
    cone.SetResolution(50)
    cone.SetDirection(0, 0, 1)
    cone.Update()
    
    # **NUEVO: Definir plano de corte**
    # Después de rotar, el cono apunta en dirección Z
    # Calculamos la posición del corte
    cut_height = height * (1 - truncate_ratio)  # altura desde la base
    
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, cut_height)  # posición del plano
    plane.SetNormal(0, 0, 1)  # normal apuntando hacia arriba
    
    # **NUEVO: Aplicar el corte**
    clipper = vtk.vtkClipPolyData()
    # clipper.SetInputConnection(transformFilter.GetOutputPort())
    clipper.SetInputConnection(cone.GetOutputPort())
    clipper.SetClipFunction(plane)
    clipper.InsideOutOn()  # mantener la parte de abajo
    clipper.Update()

        # Rotar el cono
    transform = vtk.vtkTransform()
    transform.RotateX(-90) 
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(clipper.GetOutputPort())
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    
    # **OPCIONAL: Cerrar la superficie (tapar el agujero superior)**
    # Si quieres que el corte quede cerrado:
    capper = vtk.vtkFillHolesFilter()
    capper.SetInputConnection(transformFilter.GetOutputPort())
    capper.SetHoleSize(1000.0)  # tamaño máximo de agujero a cerrar
    capper.Update()
    
    # Continuar con las normales y texturas
    normal_filter = vtk.vtkPolyDataNormals()
    normal_filter.SetInputConnection(capper.GetOutputPort())
    normal_filter.ComputePointNormalsOn()
    normal_filter.ComputeCellNormalsOff()
    normal_filter.ConsistencyOn()           # NUEVO: Forzar consistencia
    normal_filter.AutoOrientNormalsOn()     # NUEVO: Auto-orientar hacia afuera
    normal_filter.SplittingOff()            # NUEVO: No dividir en bordes
    normal_filter.Update()
    
    texture_filter = vtk.vtkTextureMapToCylinder()
    texture_filter.SetInputData(normal_filter.GetOutput())
    texture_filter.Update()
    
    mesh = texture_filter.GetOutput()
    
    # Extraer datos...
    normales_vtk = mesh.GetPointData().GetNormals()
    # print(">> normales_vtk", normales_vtk)
    N = []
    if normales_vtk:
        N = [normales_vtk.GetTuple(i) for i in range(normales_vtk.GetNumberOfTuples())]
    
    texturas_vtk = mesh.GetPointData().GetTCoords()
    T = []
    if texturas_vtk:
        T = [texturas_vtk.GetTuple(i) for i in range(texturas_vtk.GetNumberOfTuples())]
    
    puntos_vtk = mesh.GetPoints()
    P = [puntos_vtk.GetPoint(i) for i in range(puntos_vtk.GetNumberOfPoints())]
    
    caras = mesh.GetPolys()
    caras.InitTraversal()
    C = []
    id_list = vtk.vtkIdList()
    while caras.GetNextCell(id_list):
        C.append([id_list.GetId(j) for j in range(id_list.GetNumberOfIds())])
    
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

  def _mecha(self, base=0.2, height=0.1, length=0.1):
    """
    Crea una 'mecha' como un prisma triangular invertido y
    la devuelve en el formato (P, N, T, C) que usa _sphere/_wedge.

    - base: ancho del triángulo (eje X)
    - height: altura del triángulo (punta hacia -Y)
    - length: profundidad a lo largo del eje Z
    """
    import vtk

    # 1. Definir los 6 puntos de un wedge (prisma triangular)
    #
    # Visto de frente (eje X-Y):
    #
    #        (0, 0)
    #       /     \
    # (-b/2, 0)  (b/2, 0)
    #        \
    #        (0, -h)   ← punta hacia abajo
    #
    # Luego lo extruimos en Z (0 y length).
    half_base = base * 0.5

    points = vtk.vtkPoints()
    # Triángulo "superior" (y = 0)
    points.InsertNextPoint(-half_base, 0.0,       0.0)      # P0
    points.InsertNextPoint( half_base, 0.0,       0.0)      # P1
    points.InsertNextPoint( 0.0,      -height,    0.0)      # P2 (punta abajo)
    # Triángulo "superior" extruido en Z
    points.InsertNextPoint(-half_base, 0.0,       length)   # P3
    points.InsertNextPoint( half_base, 0.0,       length)   # P4
    points.InsertNextPoint( 0.0,      -height,    length)   # P5

    # 2. Celda wedge
    wedge = vtk.vtkWedge()
    wedge.GetPointIds().SetId(0, 0)
    wedge.GetPointIds().SetId(1, 1)
    wedge.GetPointIds().SetId(2, 2)
    wedge.GetPointIds().SetId(3, 3)
    wedge.GetPointIds().SetId(4, 4)
    wedge.GetPointIds().SetId(5, 5)

    # 3. Centrar la geometría en el origen (más cómodo para rotar/posicionar)
    #    Tomamos el bounding box de los puntos y lo llevamos al centro.
    cx = 0.0
    cy = -height * 0.5        # centro entre 0 y -height
    cz = length * 0.5
    for i in range(points.GetNumberOfPoints()):
        x, y, z = points.GetPoint(i)
        points.SetPoint(i, x - cx, y - cy, z - cz)

    # 4. UnstructuredGrid
    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(wedge.GetCellType(), wedge.GetPointIds())

    # 5. Pasar a superficie
    geom = vtk.vtkGeometryFilter()
    geom.SetInputData(ugrid)
    geom.Update()
    poly = geom.GetOutput()

    # 6. Normales
    normals_gen = vtk.vtkPolyDataNormals()
    normals_gen.SetInputData(poly)
    normals_gen.ComputePointNormalsOn()
    normals_gen.ComputeCellNormalsOff()
    normals_gen.Update()
    poly = normals_gen.GetOutput()

    pts     = poly.GetPoints()
    normals = poly.GetPointData().GetNormals()

    # 7. Bounds para UVs simples (X-Z → u-v)
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

        u = (x - xmin) / dx
        v = (z - zmin) / dz
        T.append((u, v))

    # 8. Celdas
    C = []
    for i in range(poly.GetNumberOfCells()):
        cell = poly.GetCell(i)
        ids = []
        for j in range(cell.GetNumberOfPoints()):
            ids.append(cell.GetPointId(j))
        C.append(ids)

    return (P, N, T, C)

  def _cylinder(self, height, radius):
    """
    Crea un cilindro rotado 90 grados con tapas cerradas
    
    Args:
        height: altura del cilindro
        radius: radio del cilindro
    """
    print(">> Creating cylinder with height:", height, " radius:", radius)
    
    # 1. Crear el cuerpo del cilindro SIN tapas
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetHeight(height)
    cylinder.SetRadius(radius)
    cylinder.SetResolution(50)
    cylinder.SetCapping(False)
    cylinder.Update()
    
    # Rotar el cilindro
    transform_cyl = vtk.vtkTransform()
    transform_cyl.RotateX(-90) 
    transformFilter_cyl = vtk.vtkTransformPolyDataFilter()
    transformFilter_cyl.SetInputConnection(cylinder.GetOutputPort())
    transformFilter_cyl.SetTransform(transform_cyl)
    transformFilter_cyl.Update()
    
    # 2. Crear tapa frontal (Z = +height/2)
    disk1 = vtk.vtkDiskSource()
    disk1.SetInnerRadius(0.0)
    disk1.SetOuterRadius(radius)
    disk1.SetRadialResolution(1)
    disk1.SetCircumferentialResolution(50)
    disk1.Update()
    
    # **INVERTIR normales de la tapa frontal**
    reverse1 = vtk.vtkReverseSense()
    reverse1.SetInputConnection(disk1.GetOutputPort())
    reverse1.ReverseNormalsOn()
    reverse1.ReverseCellsOn()
    reverse1.Update()
    
    # Posicionar tapa frontal
    transform1 = vtk.vtkTransform()
    transform1.Translate(0, 0, height/2)
    transformFilter1 = vtk.vtkTransformPolyDataFilter()
    transformFilter1.SetInputConnection(reverse1.GetOutputPort())
    transformFilter1.SetTransform(transform1)
    transformFilter1.Update()
    
    # 3. Crear tapa trasera (Z = -height/2)
    disk2 = vtk.vtkDiskSource()
    disk2.SetInnerRadius(0.0)
    disk2.SetOuterRadius(radius)
    disk2.SetRadialResolution(1)
    disk2.SetCircumferentialResolution(50)
    disk2.Update()
    
    # **INVERTIR normales de la tapa trasera**
    reverse2 = vtk.vtkReverseSense()
    reverse2.SetInputConnection(disk2.GetOutputPort())
    reverse2.ReverseNormalsOn()
    reverse2.ReverseCellsOn()
    reverse2.Update()
    
    # Rotar y posicionar tapa trasera
    transform2 = vtk.vtkTransform()
    transform2.RotateX(180)  # Voltear el disco
    transform2.Translate(0, 0, -height/2)
    transformFilter2 = vtk.vtkTransformPolyDataFilter()
    transformFilter2.SetInputConnection(reverse2.GetOutputPort())
    transformFilter2.SetTransform(transform2)
    transformFilter2.Update()
    
    # 4. Combinar todas las partes
    append = vtk.vtkAppendPolyData()
    append.AddInputConnection(transformFilter_cyl.GetOutputPort())
    append.AddInputConnection(transformFilter1.GetOutputPort())
    append.AddInputConnection(transformFilter2.GetOutputPort())
    append.Update()
    
    # 5. Limpiar
    clean = vtk.vtkCleanPolyData()
    clean.SetInputConnection(append.GetOutputPort())
    clean.Update()
    
    # 6. Triangular
    triangulate = vtk.vtkTriangleFilter()
    triangulate.SetInputConnection(clean.GetOutputPort())
    triangulate.Update()
    
    # 7. Calcular normales finales
    normal_filter = vtk.vtkPolyDataNormals()
    normal_filter.SetInputConnection(triangulate.GetOutputPort())
    normal_filter.ComputePointNormalsOn()
    normal_filter.ComputeCellNormalsOff()
    normal_filter.ConsistencyOn()
    normal_filter.AutoOrientNormalsOn()
    normal_filter.SplittingOff()
    normal_filter.Update()
    
    # 8. Aplicar mapeo de textura cilíndrica
    texture_filter = vtk.vtkTextureMapToCylinder()
    texture_filter.SetInputData(normal_filter.GetOutput())
    texture_filter.Update()
    
    mesh = texture_filter.GetOutput()
    
    print(">> Cilindro creado - Puntos:", mesh.GetNumberOfPoints(), 
          "Caras:", mesh.GetNumberOfPolys())
    
    # Extraer normales
    normales_vtk = mesh.GetPointData().GetNormals()
    print(">> normales_vtk", normales_vtk)
    N = []
    if normales_vtk:
        N = [normales_vtk.GetTuple(i) for i in range(normales_vtk.GetNumberOfTuples())]
    
    # Extraer coordenadas de textura
    texturas_vtk = mesh.GetPointData().GetTCoords()
    T = []
    if texturas_vtk:
        T = [texturas_vtk.GetTuple(i) for i in range(texturas_vtk.GetNumberOfTuples())]
    
    # Extraer puntos
    puntos_vtk = mesh.GetPoints()
    P = [puntos_vtk.GetPoint(i) for i in range(puntos_vtk.GetNumberOfPoints())]
    
    # Extraer caras
    caras = mesh.GetPolys()
    caras.InitTraversal()
    C = []
    id_list = vtk.vtkIdList()
    while caras.GetNextCell(id_list):
        C.append([id_list.GetId(j) for j in range(id_list.GetNumberOfIds())])
    
    return (P, N, T, C)  
# end class

## eof - BaseApplicationWithVTK.py
