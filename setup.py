import re
import setuptools


with open("canopenx/__init__.py", "r") as f:
	version = re.search(r"^__version__\s*=\s*[\'\"]([^\'\"]*)[\'\"]", f.read(), re.MULTILINE).group(1)


with open("readme.rst", "r") as f:
	long_description = f.read()


setuptools.setup(
	name = "canopenx",
	version = version,
	url = "https://github.com/marcel-kanter/python-canopenx",
	description = "CANopen package for python",
	long_description = long_description,
	author = "Marcel Kanter",
	author_email = "marcel.kanter@googlemail.com",

	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Healthcare Industry",
		"Intended Audience :: Information Technology",
		"Intended Audience :: Manufacturing",
		"Intended Audience :: Science/Research",
		"Intended Audience :: Telecommunications Industry",
		"License :: MIT",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Topic :: System :: Networking",
		"Topic :: Software Development",
		"Topic :: Software Development :: Testing",
		"Topic :: Software Development :: Embedded Systems",
		"Topic :: Utilities"
	],

	python_requires = ">=3.6",

	packages = setuptools.find_packages(include = ["canopenx*"]),

	install_requires = [
		"python-can>=3.0.0"
	]
)
