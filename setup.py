from setuptools import setup

setup(
	name="mychain",
	version='0.1',
	py_modules=['mychain'],
	install_requires=[
		'Click',
		'ecdsa'
	],
	entry_points='''
        [console_scripts]
        mychain=mychain:cli
    ''',
)
