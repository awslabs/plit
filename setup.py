from setuptools import find_packages, setup
import os
import versioneer


def read(fname):
    """Read content on file name."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="plitlib",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["config/general.json", "config/default.mplstyle"]},
    include_package_data=True,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A wrapper for automating common matplotlib tasks",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/awslabs/plit",
    keywords="plit visualization data science analytics analysis matplotlib",
    author="Josiah Davis",
    license="Apache 2.0",
    python_requires=">=3.6.0",
    install_requires=["matplotlib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
