from distutils.core import setup
setup(
    name='lib_import',
    packages=['lib_import'],
    version='0.0.1',
    license='apache-2.0',
    description='Django library for importing data',
    author='Fanny Dufresne',
    author_email='dufresne.fany@gmail.com',
    url='',  # TODO: fill in
    download_url='',  # TODO: fill in
    keywords=['django', 'import'],
    install_requires=[
        "django >= 2.2",
        "django-import-export == 1.2"
        "tablib >= 0.12"
        "pycontracts >= 1.7"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache 2.0',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
    ],
)
