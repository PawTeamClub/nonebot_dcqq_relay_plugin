import setuptools

long_description = None;
requirements = None;

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="nonebot_dcqq_relay_plugin",
    version="0.1.0",
    author="Robonyantame",
    author_email="robonyantame@gmail.com",
    description="使用Nonebot2让Discord和QQ群实现互相通信",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin",
    packages=setuptools.find_packages(),
    python_requires=">=3.8, <4.0",
    classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
    ],
    install_requires=requirements,
)
