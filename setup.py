from setuptools import setup

setup(
    name="system-dash",
    version="0.0.1",
    install_requires=["psutil", "PyGObject", "pycairo"],
    packages=["system_dash"],
    entry_points={
        "console_scripts": [
            "system-dash = system_dash.gui:main"
        ],
        "gui_scripts": [
            "system-dash = system_dash.gui:main"
        ]
    }
)