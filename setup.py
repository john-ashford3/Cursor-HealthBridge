from setuptools import setup, find_packages

setup(
    name="healthbridge",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'flask-mail',
        'azure-storage-blob',
        'python-magic-bin',
        'werkzeug',
        'requests',
        'oauthlib',
        'python-dotenv',
        'Flask-Dance[sqla]',
    ],
) 