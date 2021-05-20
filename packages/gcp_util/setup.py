import setuptools

setuptools.setup(
    name="gcp-util",
    version="0.0.3",
    author="Conall Daly",
    author_email="conalldalydev@:gmail.com",
    description="Google Cloud Platform Utility Package",
    packages=setuptools.find_packages(),
    install_requires=[
          'google-cloud-pubsub',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    url='https://github.com/tunnelWithAC/gcp-cloud-run-pypi/tree/master/packages/gcp_util'
)