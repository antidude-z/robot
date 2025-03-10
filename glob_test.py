import glob

files = glob.glob('images/*')

for file in files:
    print(file, type(file))