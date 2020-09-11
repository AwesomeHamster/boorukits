from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

packages = find_packages(where="src")

setup(
    name="boorukits",
    version="0.0.2",
    description="boorukits is an unofficial asynchronous library for the APIs of booru-like gallery (eg. Danbooru/Moebooru).",
    url="https://github.com/MaikoTan/boorukits",
    project_urls={
        "Documentation": "https://github.com/MaikoTan/boorukits",
        "Source Code": "https://github.com/MaikoTan/boorukits",
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Maiko Tan",
    author_email="maiko.tan.coding@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=packages,
    package_dir={"boorukits": "src/boorukits"},
    python_requires=">=3.7",
    platforms=["nt", "posix", "os2"],
    install_requires=["aiohttp>=3.6.2"],
)
