from setuptools import setup


install_requires = [
	"numpy",

	# Libraries used for testing
	"pytest"
]


setup(
	name="fgglib",
	install_requires=install_requires,
	version="0.1",
	scripts=[],
    url="https://github.com/Dogtype/AFLTProject",
	packages=['fgglib']
)
