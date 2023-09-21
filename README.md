MultiHuggingGradio  ![MultiHuggingGradio Demo](https://github.com/LPFerreira33/MultiHuggingGradio/actions/workflows/env_creation_linter_and_tests.yml/badge.svg)
===================

*Brief summary of the repository*


## 📐 How to Install

CUDA_VERSION is machine dependent, in this installation version v11.6 (cu116) is installed, change depending on machine cuda version 
```shell
conda activate <your_env_name>

pip install -e multihugginggradio -f https://download.pytorch.org/whl/cu116/torch_stable.html
```

## 📈 Tests

Test files should start with prefix "test_" to become discoverable by pytest. --cov flag will also create a coverage information for the tests
Run tests with:
```shell
pytest --cov=multihugginggradio/multihugginggradio
```

## 🖇️ Documentation
*Insert Links to Coding guidelines, Pull Requests and review guidelines, dev workflow guidelines*

## ⚖️ LICENSE
*Insert License*
