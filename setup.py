from setuptools import setup, find_packages

setup(
    name="paddel",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"paddel": ["py.typed"]},
    version="0.0.1",
)
