import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qdrant-tools",
    version="0.0.1",
    long_description=long_description,
    author="Nirant Kasliwal",
    author_email="nirant.bits@gmail.com",
    install_requires=[
        "pinecone-client==2.2.1",
        "qdrant-client>=1.2.0",
    ],
    url="https://github.com/NirantK/qdrant-tools",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
