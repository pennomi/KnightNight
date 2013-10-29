rm -rf dist/
cxfreeze main.py -OO -s --exclude-modules=tkinter,tcl
cp -r resources/ dist/
