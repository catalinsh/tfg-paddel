from setuptools import setup, find_packages

setup(
    name="footfg",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"footfg": ["py.typed"]},
    version="0.0.1",
)
