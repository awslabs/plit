from setuptools import find_packages, setup

setup(
    name="plit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.1.0",
    description="""A distribution of publication quality, static, ML-specific,
    data visualization templates built on Matplotlib.""",
    author="Josiah Davis",
    license="Apache 2.0",
    install_requires=["matplotlib"],
)
