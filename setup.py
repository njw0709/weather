import setuptools

# reading long description from file
with open("README.md") as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = [
    "rasterio",
    "geopandas",
    "pandas",
    "netCDF4",
    "shapely",
    "pytest",
]

# some more details
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Development Status :: 4 - Beta",
]

# calling the setup function
# TODO: separate dev / test / deploy setup with options
setuptools.setup(
    name="cdr_weather",
    version="0.0.1",
    description="processing weather data for CDR",
    long_description=long_description,
    author="Jong Woo Nam",
    author_email="namj@usc.edu",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords="CDR, weather, raster, geopandas",
)
