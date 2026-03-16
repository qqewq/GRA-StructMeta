
```python
from setuptools import setup, find_packages

setup(
    name="gra_struct_meta",
    version="0.1.0",
    description="GRA Metaprogramming of Structures",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20",
        "scipy>=1.7",
        "matplotlib>=3.4",
        "jupyter",
    ],
    python_requires=">=3.8",
)
```

