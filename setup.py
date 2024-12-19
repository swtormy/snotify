from setuptools import setup, find_packages

setup(
    name="snotify",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.6",
        "aiosmtplib>=3.0.2",
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
