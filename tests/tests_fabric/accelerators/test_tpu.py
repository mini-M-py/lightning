# Copyright The Lightning AI team.
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
# limitations under the License

import pytest

from lightning.fabric.accelerators.tpu import TPUAccelerator
from tests_fabric.helpers.runif import RunIf


@RunIf(tpu=True)
def test_auto_device_count():
    # this depends on the chip used, e.g. with v4-8 we expect 4
    # there's no easy way to test it without copying the `auto_device_count` so just check that its greater than 1
    assert TPUAccelerator.auto_device_count() > 1


@RunIf(tpu=True)
def test_availability():
    assert TPUAccelerator.is_available()


@pytest.mark.parametrize("devices", (1, 8))
def test_get_parallel_devices(devices, tpu_available):
    expected = TPUAccelerator.get_parallel_devices(devices)
    assert len(expected) == devices


def test_get_parallel_devices_raises(tpu_available):
    with pytest.raises(ValueError, match="devices` can only be"):
        TPUAccelerator.get_parallel_devices(0)
    with pytest.raises(ValueError, match="devices` can only be"):
        TPUAccelerator.get_parallel_devices(5)
    with pytest.raises(ValueError, match="Could not parse.*anything-else'"):
        TPUAccelerator.get_parallel_devices("anything-else")
