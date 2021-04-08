from setuptools import setup

setup(
    name='ArtemisRemoteControl',
    packages=['artemisremotecontrol'],
    url='https://github.com/Nama/ArtemisRemoteControl',
    license='MIT',
    author='Yama',
    author_email='',
    description='Library for RemoteControlModule for Artemis',
    install_requires=[
        'requests>=2.25.1',
        'simple-plugin-loader>=1.6'
    ]
)
