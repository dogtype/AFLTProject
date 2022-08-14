from setuptools import setup


install_requires = [
	"numpy",
	"scipy",
	"networkx",
	# Libraries used for testing
	"pytest",
	"pytest-cov"
]


setup(
	name="fgglib",
	install_requires=install_requires,
	version="1.0",
	scripts=[],
    url="https://github.com/Dogtype/AFLTProject",
	packages=['fgglib']
)
