from setuptools import setup, find_packages

setup(
    name="plateviz",
    version="0.1.0",
    description="Plate reader data visualization",
    author="Radium2000",
    author_email="rudrakalra20@gmail.com",
    url="https://github.com/Radium2000/plate-viz",
    packages=find_packages(),
    install_requires=["numpy", "matplotlib", "customtkinter", "seaborn"]
)