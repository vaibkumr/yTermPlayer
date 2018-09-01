import setuptools

reqs = (line.strip() for line in open("requirements.txt"))
LONG_DESC = open('README.md').read()
setuptools.setup(
    name="yTermPlayer",
    version="1.0.0",
    author="Time Traveller",
    author_email="notSharing@ever.com",
    description="Play youtube playlists as audio on linux terminal ",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/TimeTraveller-San/yTermPlayer",
    packages=setuptools.find_packages(),
    license="GPLv3",
    install_requires=reqs,
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={"console_scripts": ["yterm=yTermPlayer.__main__:main"]},
)
