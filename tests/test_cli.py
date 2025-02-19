"""
Tests for CLI.
"""
import subprocess
from pathlib import Path

import argbind
import numpy as np
from audiotools import AudioSignal

from dac.__main__ import run


def setup_module(module):
    data_dir = Path(__file__).parent / "assets"
    data_dir.mkdir(exist_ok=True, parents=True)
    input_dir = data_dir / "input"
    input_dir.mkdir(exist_ok=True, parents=True)

    for i in range(5):
        signal = AudioSignal(np.random.randn(1000), 44_100)
        signal.write(input_dir / f"sample_{i}.wav")
    return input_dir


def teardown_module(module):
    repo_root = Path(__file__).parent.parent
    subprocess.check_output(["rm", "-rf", f"{repo_root}/tests/assets"])


def test_reconstruction():
    # Test encoding
    input_dir = Path(__file__).parent / "assets" / "input"
    output_dir = input_dir.parent / "encoded_output"
    args = {
        "input": str(input_dir),
        "output": str(output_dir),
    }
    with argbind.scope(args):
        run("encode")

    # Test decoding
    input_dir = output_dir
    output_dir = input_dir.parent / "decoded_output"
    args = {
        "input": str(input_dir),
        "output": str(output_dir),
    }
    with argbind.scope(args):
        run("decode")


# CUDA_VISIBLE_DEVICES=0 python -m pytest tests/test_cli.py -s
