from setuptools import setup, find_packages

setup(
    name="feigenbaum-ia",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=["torch>=2.0", "numpy>=1.24", "scipy>=1.11", "tqdm>=4.65"],
    description="Fractal-adaptive neural architecture based on Feigenbaum constant",
    author="Daniel Estefani & Melissa Solari (IA)",
    license="MIT",
)
