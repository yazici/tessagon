from tessagon.core.grid_tile_generator import GridTileGenerator
from tessagon.core.rotate_tile_generator import RotateTileGenerator

class Tessagon:
  def __init__(self, f, **kwargs):
    self.f = f
    self.tile_class = self.init_tile_class()

    if 'tile_generator' in kwargs:
      self.tile_generator = kwargs['tile_generator'](self, **kwargs)
    elif 'rot_factor' in kwargs:
      self.tile_generator = RotateTileGenerator(self, **kwargs)
    else:
      self.tile_generator = GridTileGenerator(self, **kwargs)

    # Optional post processing function
    self.post_process = None
    if 'post_process' in kwargs:
      self.post_process = kwargs['post_process']

    if 'adaptor_class' in kwargs:
      adaptor_class = kwargs['adaptor_class']
      self.mesh_adaptor = adaptor_class(**kwargs)
    else:
      raise ValueError('Must provide a mesh adaptor class')

    self.tiles = None
    self.face_types = {}
    self.vert_types = {}

  def create_mesh(self):
    self._initialize_tiles()

    self.mesh_adaptor.create_empty_mesh()

    self._calculate_verts()
    self._calculate_faces()

    self.mesh_adaptor.finish_mesh()

    if self.post_process:
      self.post_process()

    return self.mesh_adaptor.get_mesh()

  def inspect(self):
    print("\n=== %s ===\n" % (self.__class__.__name__))
    for i in range(len(self.tiles)):
      self.tiles[i].inspect(tile_number=i)

  ### Below are protected

  def _initialize_tiles(self):
    self.tiles = self.tile_generator.create_tiles()
        
  def _calculate_verts(self):
    for tile in self.tiles:
      tile.calculate_verts()

  def _calculate_faces(self):
    for tile in self.tiles:
      tile.calculate_faces()

