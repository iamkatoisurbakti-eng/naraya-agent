"""Shim agar `pip install -e .` (editable) tetap berfungsi pada setuptools lawas
yang belum mendukung PEP 660. Metadata sebenarnya ada di pyproject.toml."""
from setuptools import setup

setup()
