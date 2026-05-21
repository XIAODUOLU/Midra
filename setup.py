from setuptools import find_packages, setup


setup(
    name="midra",
    version="0.1.0",
    description="Midra prompt-to-MIDI framework",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        line.strip()
        for line in open("requirements.txt", encoding="utf-8").read().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "midra=music_agent.main:main",
        ]
    },
)

