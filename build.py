import sys
import os,shutil
from cx_Freeze import setup, Executable
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
executables = [Executable(script='xk_prepare.pyw',
               base=base,
               targetName="xk_prepare.exe",
               compress=True),
               Executable(script='xk_run.py',
               base=None,
               targetName="xk_run.exe",
               compress=True)]
setup(name='xkmad',
      version='1.0',
      description='xkmad',
      executables=executables,
      options={'build_exe':{'optimize':2,'packages':'lxml'}},)

print('===== CLEANING UP =====')

os.remove('build/exe.win32-3.4/_hashlib.pyd')
os.remove('build/exe.win32-3.4/_ssl.pyd')
shutil.rmtree('build/exe.win32-3.4/tcl/tzdata')
shutil.rmtree('build/exe.win32-3.4/tcl/msgs')
shutil.rmtree('build/exe.win32-3.4/tcl/encoding')
shutil.rmtree('build/exe.win32-3.4/tk/demos')
shutil.rmtree('build/exe.win32-3.4/tk/images')
shutil.rmtree('build/exe.win32-3.4/tk/msgs')

print('===== DONE =====')

