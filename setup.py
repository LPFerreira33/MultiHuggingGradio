from setuptools import setup, find_namespace_packages

try:
    # Read the contents of requirements.txt
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    print("Info: requirements.txt not found")
    requirements = []


setup(
    name="LargeLanguageModel",
    version="0.1.0",
    description="A short description of your package",
    long_description="A longer description of your package",
    long_description_content_type="text/markdown",
    # url="https://github.com/your-username/your-repo",
    packages=find_namespace_packages(include=['largelanguagemodel.*'],
                                     exclude=["tests", ".test_*", ".tests*"]),
    python_requires="==3.8.*",
    install_requires=requirements,
    include_package_data=True,
)
