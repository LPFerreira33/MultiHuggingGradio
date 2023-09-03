LargeLanguageModels
===================

*Brief summary of the repository*


## 📐 How to Install

CUDA_VERSION is machine dependent, in this installation version v11.6 (cu116) is installed, change depending on machine cuda version 
```shell
conda activate <your_env_name>

pip install -e multihugginggradio -f https://download.pytorch.org/whl/cu116/torch_stable.html
```

## 📈 Tests

Test files should start with prefix "test_" to become discoverable by pytest
Run tests with:
```shell
pytest <folder_name>
```

## 🖇️ Documentation
*Insert Links to Coding guidelines, Pull Requests and review guidelines, dev workflow guidelines*

## ⚖️ LICENSE
*Insert License*
