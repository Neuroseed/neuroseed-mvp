from .dense import DENSE_LAY
from .conv2d import CONV2D_LAY
from .dropout import DROPOUT_LAY
from .averagepooling2d import AVERAGEPOOLING2D_LAY
from .maxpooling2d import MAXPOOLING2D_LAY

LAYERS = [
          DENSE_LAY,
          CONV2D_LAY,
          DROPOUT_LAY,
          AVERAGEPOOLING2D_LAY,
          MAXPOOLING2D_LAY
          ]
