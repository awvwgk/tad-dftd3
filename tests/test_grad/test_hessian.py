"""
Testing dispersion Hessian (autodiff).
"""
from __future__ import annotations

import pytest
import torch

from tad_dftd3 import dftd3, util

from ..samples import samples
from ..utils import reshape_fortran

sample_list = ["LiH", "SiH4", "PbH4-BiH3", "MB16_43_01"]

tol = 1e-8


def test_fail() -> None:
    sample = samples["LiH"]
    numbers = sample["numbers"]
    positions = sample["positions"]

    # GFN1-xTB parameters
    param = {}

    # differentiable variable is not a tensor
    with pytest.raises(RuntimeError):
        util.hessian(dftd3, (numbers, positions, param), argnums=2)


def test_zeros() -> None:
    d = torch.randn(2, 3, requires_grad=True)

    def dummy(x: torch.Tensor) -> torch.Tensor:
        return torch.zeros_like(x)

    hess = util.hessian(dummy, (d,), argnums=0)
    assert pytest.approx(torch.zeros([*d.shape, *d.shape])) == hess.detach()


@pytest.mark.parametrize("dtype", [torch.double])
@pytest.mark.parametrize("name", sample_list)
def test_single(dtype: torch.dtype, name: str) -> None:
    sample = samples[name]
    numbers = sample["numbers"]
    positions = sample["positions"].type(dtype)

    # GFN1-xTB parameters
    param = {
        "s6": positions.new_tensor(1.00000000),
        "s8": positions.new_tensor(2.40000000),
        "s9": positions.new_tensor(0.00000000),
        "a1": positions.new_tensor(0.63000000),
        "a2": positions.new_tensor(5.00000000),
    }

    ref = reshape_fortran(
        sample["hessian"].type(dtype),
        torch.Size((numbers.shape[0], 3, numbers.shape[0], 3)),
    )

    # variable to be differentiated
    positions.requires_grad_(True)

    hess = util.hessian(dftd3, (numbers, positions, param), argnums=1)
    assert pytest.approx(ref, abs=tol, rel=tol) == hess.detach()

    positions.detach_()


# TODO: Figure out batched Hessian computation
@pytest.mark.parametrize("dtype", [torch.double])
@pytest.mark.parametrize("name1", ["LiH"])
@pytest.mark.parametrize("name2", sample_list)
def skip_test_batch(dtype: torch.dtype, name1: str, name2) -> None:
    sample1, sample2 = samples[name1], samples[name2]
    numbers = util.pack(
        [
            sample1["numbers"],
            sample2["numbers"],
        ]
    )
    positions = util.pack(
        [
            sample1["positions"].type(dtype),
            sample2["positions"].type(dtype),
        ]
    )

    # GFN1-xTB parameters
    param = {
        "s6": positions.new_tensor(1.00000000),
        "s8": positions.new_tensor(2.40000000),
        "s9": positions.new_tensor(0.00000000),
        "a1": positions.new_tensor(0.63000000),
        "a2": positions.new_tensor(5.00000000),
    }

    ref = util.pack(
        [
            reshape_fortran(
                sample1["hessian"].type(dtype),
                torch.Size(
                    (sample1["numbers"].shape[0], 3, sample1["numbers"].shape[0], 3)
                ),
            ),
            reshape_fortran(
                sample2["hessian"].type(dtype),
                torch.Size(
                    (sample2["numbers"].shape[0], 3, sample2["numbers"].shape[0], 3)
                ),
            ),
        ]
    )

    # variable to be differentiated
    positions.requires_grad_(True)

    hess = util.hessian(dftd3, (numbers, positions, param), argnums=1)
    assert pytest.approx(ref, abs=tol, rel=tol) == hess.detach()

    positions.detach_()
