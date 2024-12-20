from setuptools import setup, find_packages

setup(
    name="snotify",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "aiohappyeyeballs==2.4.3",
        "aiohttp==3.11.6",
        "aiosignal==1.3.1",
        "aiosmtplib==3.0.2",
        "attrs==24.2.0",
        "colorama==0.4.6",
        "frozenlist==1.5.0",
        "idna==3.10",
        "iniconfig==2.0.0",
        "multidict==6.1.0",
        "packaging==24.2",
        "pluggy==1.5.0",
        "propcache==0.2.0",
        "yarl==1.17.2",
    ],
    description="Lightweight notification manager for Telegram, Webhook, Email and Custom channels",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konstantin Vasilev",
    author_email="swtormy@yahoo.com",
    url="https://github.com/swtormy/snotify",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="notifications telegram , webhook, email",
    project_urls={
        "Documentation": "https://github.com/swtormy/snotify#readme",
        "Source": "https://github.com/swtormy/snotify",
        "Tracker": "https://github.com/swtormy/snotify/issues",
    },
)
