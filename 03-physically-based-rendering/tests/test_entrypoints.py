import os
import subprocess
import sys
from pathlib import Path

import cv2 as cv
import flip_evaluator as flip
import numpy as np
import pytest
from numpy.testing import assert_allclose

ENTRYPOINTS_PATH = os.path.join(os.path.dirname(__file__), "../entrypoints")
ENTRYPOINTS = ["01-light_direction.py",
               "02-diffuse.py",
               "03-specular.py",
               "04-ambient.py",
               "05-materials.py"]

THIS_PATH = os.path.dirname(__file__)

FLIP_THRESHOULD = 0.05


def run_entrypoint(name: str):
    path = os.path.join(ENTRYPOINTS_PATH, name)

    try:
        subprocess.run([sys.executable, path],
                       cwd=ENTRYPOINTS_PATH,
                       timeout=5)
    except subprocess.TimeoutExpired:
        pass


@pytest.mark.parametrize("name", ENTRYPOINTS)
def test_entrypoint(name: str):
    run_entrypoint(name)

    image_name = name.removesuffix(".py")+"000.png"

    desired_path = os.path.join(THIS_PATH, image_name)
    actual_path = os.path.join(ENTRYPOINTS_PATH, image_name)

    assert Path(actual_path).is_file(), "Entrypoint did not generate an image."

    desired = cv.imread(desired_path).astype(np.float32)/255
    actual = cv.imread(actual_path).astype(np.float32)/255

    flipErrorMap, meanFLIPError, _ = flip.evaluate(desired, actual, "LDR")

    assert meanFLIPError < 0.03, "Generated image is different from reference."

    wrong_pixels = np.sum(flipErrorMap > FLIP_THRESHOULD)
    n_pixel = flipErrorMap.size
    error_rate = wrong_pixels/n_pixel

    assert error_rate <= 0.01, "Generated image is different from reference."
