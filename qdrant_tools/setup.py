from setuptools import setup

setup(
    name="qdrant-journey",
    version="0.1.0",
    description="A sample package",
    author="Aditya and Nirant",
    author_email="nirant.bits@gmail.com",
    packages=["qdrant-journey"],
    install_requires=[
        "pinecone-client==2.2.1",
        "qdrant-client==1.2.0",
        "cohere==4.6.0",
    ],
)
