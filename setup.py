from setuptools import setup, find_packages

setup(
    name="nexusos",
    version="0.1.0",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6>=6.4.0",
        "psutil>=5.9.0",
        "pyttsx3>=2.90",
        "requests>=2.28.1",
        "numpy>=1.21.0",
        "pyOpenGL>=3.1.6",
        "python-dotenv>=0.19.0",
        "websockets>=10.3",
        "sounddevice>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "nexusos=main:main",
        ],
    },
)
