import torch
import sys
import numpy as np

print('__pyTorch VERSION:', torch.__version__)
print('__pyTorch CUDA VERSION:', torch.version.cuda)
print('__CUDNN VERSION:', torch.backends.cudnn.version())
print('__Number CUDA Devices:', torch.cuda.device_count())
print("OS: ", sys.platform)
print("Python: ", sys.version)
print("PyTorch: ", torch.__version__)
print("Numpy: ", np.__version__)
