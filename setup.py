from setuptools import find_packages, setup
import versioneer

setup(
    name="plit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="""A distribution of publication quality, static, ML-specific,
    data visualization templates built on Matplotlib.""",
    author="Josiah Davis",
    license="Apache 2.0",
    install_requires=["matplotlib"],
)
