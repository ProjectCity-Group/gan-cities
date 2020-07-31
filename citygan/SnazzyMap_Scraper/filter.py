import os

# Similar to addressgen.py select the directory that you're going to be filter data from
#CDW_file_location = "E:/Map Photos/Attempt2/"
default_path_location = "C:/Users/Public/Pictures/"

dir_location = default_path_location

# lower kilobyte boundary is set to 75kb, upper is 500kb
lower_kb_boundary = 75
upper_kb_boundary = 500
os.chdir(dir_location)

# Will filter out all 1920*1080 screenshots as well as any files that don't meet the file size requirements
for dirpath, dirs, files in os.walk('.'):
    for file in files:
        path = os.path.join(dirpath, file)

        if not ( path.endswith('-1.png') or path.endswith('-2.png') or path.endswith('-3.png') or path.endswith('-4.png') or path.endswith('-5.png') or path.endswith('-6.png')):
            os.remove(path)
        elif os.stat(path).st_size < lower_kb_boundary * 1024 or os.stat(path).st_size > upper_kb_boundary * 1024:
            os.remove(path)
