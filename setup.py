from setuptools import setup

setup(
    name="footfg",
    packages=["footfg"],
    package_dir={"": "src"},
    package_data={"footfg": ["py.typed"]},
    version="0.0.1",
)
