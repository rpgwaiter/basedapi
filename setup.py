from setuptools import setup

setup(name='basedapi',
      version='0.1.0',
      packages=["src"],
      entry_points={
        "console_scripts": [
            "basedapi = src.__main__:main"
        ]
    },
)