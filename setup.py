import setuptools

long_description = None;
requirements = None;

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_dcqq_relay_plugin",
    version="0.1.1",
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
    install_requires=[
        "nonebot2>=2.3.1",
        "nonebot-adapter-onebot>=2.4.3",
        "nonebot-adapter-discord>=0.1.8",
        "nonebot2[fastapi]>=2.3.1",
        "nonebot2[httpx]>=2.3.1",
        "nonebot2[websockets]>=2.3.1",
        "tortoise-orm>=0.21.4"
    ],
)
