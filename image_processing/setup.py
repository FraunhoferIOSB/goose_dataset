from setuptools import setup

dependencies = [
    "super_gradients==3.7.1",
    "matplotlib",
    "pillow",
    "numpy",
    "torchmetrics",
    "wheel",
]

setup(
    name="goosetools",
    version="1.0",
    description="Official tools for the GOOSE Dataset.",
    author="Miguel Granero",
    author_email="miguel.granero@iosb.fraunhofer.de",
    url="https://github.com/FraunhoferIOSB/goose_dataset",
    packages=["goosetools"],  # would be the same as name
    install_requires=dependencies,  # external packages acting as dependencies
)
