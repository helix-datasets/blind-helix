from setuptools import setup
from setuptools import find_packages

setup(
    name="blind-helix",
    version="0.2.0.dev",
    author="MIT Lincoln Laboratory",
    author_email="helix@ll.mit.edu",
    url="https://github.com/helix-datasets/blind-helix",
    description="Automatic Component generation for HELIX",
    license="MIT",
    license_files=["LICENSE.txt"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=["helix", "lief"],
    extras_require={
        "development": [
            "black",
            "flake8",
            "pip-tools",
            "pre-commit",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["blind-helix = blind_helix.__main__:main"],
        "helix.components.loaders": [
            "blind-helix = blind_helix.library:BlindHelixLibraryLoader"
        ],
    },
)
