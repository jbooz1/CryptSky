from distutils.core import setup
import sys

from glob import glob

sys.path.append("C:")
data_files = [
    ("msvcp100", glob(r'.\*.dll'))]
setup(
    data_files=data_files,
    windows=['main.py']
)
