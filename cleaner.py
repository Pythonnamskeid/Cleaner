#!/bin/python
import os
import shutil
import re
#path = '/Users/BH/Desktop/downloads'


def getpath():
	path = input('full path to folder: ')

	if not os.path.isdir(path):
		print('this program needs full path to folder: ')
	else:
		return path

#Works
def delete_ugly_endings(path):
    ugly_endings = ['.nfo']
    print('in ugly')
    for root,dirs,files in os.walk(path):   
        for f in files:
                #print("here")
                fileName,fileExt = os.path.splitext(os.path.join(path,f))
                if fileExt.lower() in ugly_endings:
                    os.remove(os.path.join(root,f))

#works, loose files go to Shows folder
def move_to_shows(path,file_list):

    file_endings = ['.avi', '.mpg', '.mp4', '.mkv', '.m4v']
    pathfrom = path
    pathto = os.path.join(path,'Shows')
    for x in file_list:
        fileName,fileExt = os.path.splitext(os.path.join(path,x))
        #move loose files to Show folder
        if fileExt.lower() in file_endings:
            pathfrom = os.path.join(path,x)
            shutil.move(pathfrom,pathto)

def sort_tv_show(path, show,pathtoshowfolder):
	#show=show.lower()
	showlist = show.lower().split()
	reg = ''
	for x in showlist:
		reg += x + '[\s|.]*'

	#reg = reg[:-1]
	'''print("reg: ", reg)
	pattern = re.compile(reg)
	m = pattern.match("8.out.of.10.cats")
	print("m: ", m)
	if m:
		print('Yes', m.group())
	else:
		print('No match')'''

	



def main():
  	#start by getting path and see if it is valid
	path = getpath()
	if path == None:
		print("Path not valid. Exiting program")
		return

	show = input("name of show you want to sort: ")

	#change path, locate script in downloads folder
	os.chdir(path)
	pathtoshowfolder = ''
	print("current directory: ", os.getcwd())

	if not os.path.exists(os.path.join(path, 'Shows')):
		print('creating dir')
		os.mkdir('Shows')
		pathtoshowfolder = os.path.join(path,'Shows')
	else:#for debugging reasons, delte eventually else statement
		print('Shows folder already exists')
		pathtoshowfolder = os.path.join(path,'Shows')

	#delete all .nfo etc
	delete_ugly_endings(path)
	#moves loose shows to Show folder
	for root,dirs,files in os.walk(path):
		if root == path:
			file_list = list(files)
			move_to_shows(path, file_list)
            #move lose shows in download folder to Shows root = download folder

	#print("ugly endings should be gone and a show folder should be here")
	sort_tv_show(path, show)












if __name__ == '__main__':
    main()