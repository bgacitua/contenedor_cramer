from setuptools import setup, find_packages

setup(
    name="api-mysql-integration",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    description="Proyecto para extraer datos de una API y almacenarlos en una base de datos MySQL.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "requests",
        "sqlalchemy",
        "mysql-connector-python",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "api-mysql-integration=main:main",  # Ajusta esto según la función principal en main.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)