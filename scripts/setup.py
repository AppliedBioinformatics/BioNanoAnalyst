from distutils.core import setup
import py2exe
import matplotlib
setup(console=['App.py'],
          options = {
           "py2exe":{"dll_excludes":["MSVCP90.dll"],
            "excludes":["_gtkagg", "_tkagg","_ssl"],
            "includes":["matplotlib.backends.backend_tkagg","matplotlib.backends.backend_ps"]}},data_files=matplotlib.get_py2exe_datafiles())
