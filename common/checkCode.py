import os

for filename in os.listdir("."):
    if filename == 'checkCode.py':
        continue
    print('++++++++++++++++++++++++++++++++++++++++++++\n')
    print("Starting messure file: " + filename)
    os.system("pylint " + filename)
    print('++++++++++++++++++++++++++++++++++++++++++++\n')
