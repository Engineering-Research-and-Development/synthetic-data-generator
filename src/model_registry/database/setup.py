from setuptools import setup,find_packages

setup(
    name="database",
    version="0.0.10",
    description="This API contains the database schema and validation tools of our model registry",
    package_dir={"database":"database"},
    packages=find_packages(),
    author="Giuseppe Martinelli",
    requires=[
        "fastapi[standard] == 0.115.6",
        "pydantic == 2.10.3",
        "sqlmodel == 0.0.22",
        "psycopg2"
    ]
)