import setuptools

# reqs = (line.strip() for line in open("requirements.txt"))
LONG_DESC = open('README.md').read()
setuptools.setup(
    name="yTermPlayer",
    version="1.1.2",
    author="Time Traveller",
    author_email="time.traveller.san@gmail.com",
    description="Play youtube playlists as audio on linux terminal ",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/TimeTraveller-San/yTermPlayer",
    packages=setuptools.find_packages(),
    license="GPLv3",
    install_requires=[
                'pafy>=0.5.4',
                'python-dateutil>=2.7.3',
                'python-mpv>=0.3.9',
                'urwid>=2.0.1',
                'virtualenv>=15.1.0',
                'youtube-dl>=2018.8.4',
    ],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={"console_scripts": ["yterm=yTermPlayer.__main__:main"]},
)
