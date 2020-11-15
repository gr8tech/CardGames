import os
import re

path = 'C:/BACKUP/Pirple/pirple.thinkific.com/Python/Project3/assets/cards/'

for filename in os.listdir(path):
    file = path+filename
    mode_filename =  re.sub('\s+', '_', file)
    os.rename(file, mode_filename)