# pytorch UENV

PyTorch and friends: PyTorch built from source together with the CUDA, NCCL and MPI
stack it needs to run distributed on Alps.

Derived from CSCS' [`alps-uenv`](https://github.com/eth-cscs/alps-uenv) recipe
`recipes/pytorch/v2.9.1/gh200`, retargeted from GH200 to A100 (`cuda_arch=80`) for
balfrin. Keep that recipe in mind when updating: diffing against it is the easiest way
to see what has drifted.

## Versions

| version | uarch | contents |
| --- | --- | --- |
| `26.8` | `a100` | python 3.12, py-torch 2.9.1, cray-mpich 9.0.0, cuda/cudnn/cutensor, nccl + aws-ofi-nccl, ucx/ucc, py-triton, py-torchmetrics, py-einops, py-tensorboard |

Everything is exposed through the `default` view, which also sets the NCCL and
libfabric environment variables needed for multi-node training on Slingshot:

```bash
uenv start --view=default pytorch/26.8:v1
```

## Motivation

It was built as the base layer for [anemoi](https://github.com/ecmwf/anemoi-core),
but nothing in it is anemoi-specific, so it is named after what it actually contains.

## Not yet enabled

The following specs are present but commented out in `environments.yaml`, and were
left out to get a first image through: `cutlass`, `cublasmp`, `nvshmem`, `faiss`,
`py-torchvision`, `py-torchaudio`, `py-torch-nvidia-apex`, `py-transformer-engine`,
`py-transformers`, `py-tokenizers`, `py-safetensors`, `py-onnx*`, `py-vllm`.
Re-enabling them is the obvious next step.
