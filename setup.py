from setuptools import setup, find_packages
from pathlib import Path
import os

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text()

requirements = {
    "install": [
        "requests",
        "tzlocal"
    ],
    "setup": [
    ],
    "test": [
    ]
}

install_requires = requirements["install"]
setup_requires = requirements["setup"]

dirname = os.path.dirname(__file__)
version_file = os.path.join(dirname, "claude", "version.txt")
version = "0.0.0"
with open(version_file, "r") as f:
    version = f.read().strip()

setup(
    name='claude-api',
    version=version,
    author='lingfeng.chen.cn',
    license="MIT",
    author_email='lingfeng.chen.cn@gmail.com',
    description='An unofficial API for claude.ai(Claude2 AI)',
    long_description=open(os.path.join(dirname, "README.md"),
                          encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KoushikNavuluri/Claude-API/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    package_dir={
        "": "claude-api"
    },
    py_modules=["claude_api"],
    keywords=['claude', 'ai', 'claude-ai', 'API', 'requests', 'chatbot',
              'claude2'],
    install_requires=[
        'requests'
    ],
    python_requires=">=3.7",
)
