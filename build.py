import subprocess

python_ex = "python"

try:
    import wheel
    import setuptools
except ImportError:
    subprocess.call("pip install wheel setuptools", shell=True)

subprocess.call("python setup.py sdist bdist_wheel", shell=True)
subprocess.call("pip install .", shell=True)
