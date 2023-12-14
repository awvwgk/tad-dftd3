# This file is part of tad-dftd3.
# SPDX-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test loading C6 coefficients.
"""
import torch

from tad_dftd3 import reference, constants


def test_ref() -> None:
    c6 = reference._load_c6(dtype=torch.double)
    assert c6.shape == torch.Size(
        (constants.MAX_ELEMENT, constants.MAX_ELEMENT, 7, 7),
    )
