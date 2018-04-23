from .dense import DENSE_LAY
from .conv1d import CONV1D_LAY
from .conv2d import CONV2D_LAY
from .dropout import DROPOUT_LAY
from .averagepooling1d import AVERAGEPOOLING1D_LAY
from .averagepooling2d import AVERAGEPOOLING2D_LAY
from .maxpooling1d import MAXPOOLING1D_LAY
from .maxpooling2d import MAXPOOLING2D_LAY
from .flatten import FLATTEN_LAY
from .reshape import RESHAPE_LAY
from .permute import PERMUTE_LAY
from .repeatvector import REPEATVECTOR_LAY
from .activityregularization import ACTIVITYREGULARIZATION_LAY
from .masking import MASKING_LAY
from .cropping1d import CROPPING1D_LAY
from .gru import GRU_LAY
from .lstm import LSTM_LAY
from .embedding import EMBEDDING_LAY
from .batchnormalization import BATCHNORMALIZATION_LAY
from .gaussiannoise import GAUSSIANNOISE_LAY
from .gaussiandropout import GAUSSIANDROPOUT_LAY
from .simplernn import SIMPLERNN_LAY
from .convlstm2d import CONVLSTM2D_LAY
from .activation import ACTIVATION_LAY

# version < 4 layers
OLD_LAYERS = [
    DENSE_LAY,
    CONV2D_LAY,
    DROPOUT_LAY,
    AVERAGEPOOLING2D_LAY,
    MAXPOOLING2D_LAY,
    FLATTEN_LAY
]

# version >= 4 layers
NEW_LAYERS = [
    CONV1D_LAY,
    AVERAGEPOOLING1D_LAY,
    MAXPOOLING1D_LAY,
    RESHAPE_LAY,
    PERMUTE_LAY,
    REPEATVECTOR_LAY,
    ACTIVITYREGULARIZATION_LAY,
    MASKING_LAY,
    CROPPING1D_LAY,
    GRU_LAY,
    LSTM_LAY,
    EMBEDDING_LAY,
    BATCHNORMALIZATION_LAY,
    GAUSSIANNOISE_LAY,
    GAUSSIANDROPOUT_LAY,
    SIMPLERNN_LAY,
    CONVLSTM2D_LAY,
    ACTIVATION_LAY
]

LAYERS = OLD_LAYERS + NEW_LAYERS
