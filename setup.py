from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\sm990\Anaconda3\envs\GMTK\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\sm990\Anaconda3\envs\GMTK\tcl\tk8.6'

base = None


executables = [Executable("Main.py", base=base)]

packages = ["pygame", "Player", "Obstacle", "Enemy", "Map", "GenerateMap"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)
