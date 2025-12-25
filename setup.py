"""Setup configuration for UML Vision Grader Pro."""

from setuptools import setup, find_packages

setup(
    name="uml-vision-grader-pro",
    version="2.1.0",
    description="Correction automatique de diagrammes UML avec GPT-4o Vision",
    author="UML Vision Grader Pro Team",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.12",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.2",
        "requests>=2.31.0",
        "pillow>=10.1.0",
        "opencv-python>=4.8.1",
        "python-dotenv>=1.0.0",
        "slowapi>=0.1.9",
        "pytest>=8.0.0",
    ],
)
