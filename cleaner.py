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
def delete_ugly_endings(path, ugly_endings):
    for root,dirs,files in os.walk(path):   
        for f in files:
                fileName,fileExt = os.path.splitext(os.path.join(path,f))
                if fileExt.lower() in ugly_endings:
                    os.remove(os.path.join(root,f))

#Loose files hanging in downloads folder go to Shows folder
def move_to_shows(path,file_list,file_endings):

    pathfrom = path
    pathto = os.path.join(path,'Shows')
    for x in file_list:
        fileName,fileExt = os.path.splitext(os.path.join(path,x))
        #move loose files to Show folder
        if fileExt.lower() in file_endings:
            pathfrom = os.path.join(path,x)
            shutil.move(pathfrom,pathto)

#goes through all folders and finds show video files and moves them to Show folder
def sort_tv_show(path, show,pathtoshowfolder,file_endings,subtitle_endings):

	showlist = show.lower().split()
	reg = ''
	if len(showlist) == 1:
		reg += show
	else:
		i = 0
		for x in showlist:
			if i == len(showlist) - 1:
				reg += x
			else:	
				reg += x + '[\s|.|-]*'
				i+=1

	reg = '^' + reg 
	pattern = re.compile(reg)

	for root, dirs, files in os.walk(path):
		for f in files:
			m = pattern.search(f.lower())
			if m:
				#print('match')
				#print(m.group(0),f.lower())
				Filename, FileExt = os.path.splitext(os.path.join(root,f))
				if FileExt in file_endings or subtitle_endings:
					if root != pathtoshowfolder:
						try:
							shutil.move(os.path.join(root,f),pathtoshowfolder)
						except:
							print('tried to move from a folder within same folder, me so dumb')
				
def create_folder_and_sort(pathtoshowfolder,show,file_endings,subtitle_endings):

	showlist = show.lower().split()
	reg = ''
	for x in showlist:
		reg += x + '[\s|.|-|\w*]*'

	pattern = re.compile(reg)
	#print('creade folder and sort')
	os.chdir(pathtoshowfolder)
	#print(os.getcwd())
	pathtosortedfolder = ''
	#the dir name will be the user input
	if not os.path.exists(os.path.join(pathtoshowfolder,show)):
		os.mkdir(show)
		pathtosortedfolder = os.path.join(pathtoshowfolder,show)
	else:
		#print('folder exists')
		pathtosortedfolder = os.path.join(pathtoshowfolder,show)

	for root,dirs,files in os.walk(pathtoshowfolder):
		for f in files:
			m = pattern.search(f.lower())
			if m:
				if root != pathtosortedfolder:
					Filename, FileExt = os.path.splitext(os.path.join(root,f))
					if FileExt in file_endings or subtitle_endings:
						try:
							shutil.move(os.path.join(root,f),pathtosortedfolder)
						except:
							print('error when moving from')
							print(os.path.join(root,f))
							print('to ')
							print(pathtosortedfolder)
	return pathtosortedfolder



def create_season_folders(path, pathtosortedfolder, show):

	os.chdir(pathtosortedfolder)
	pattern = re.compile(r'[s|S]\d+')
	#search for season pattern to create folder
	for root,dirs,files in os.walk(pathtosortedfolder):
		for f in files:
			m = pattern.search(f.lower())
			if m:
				#print(m.group(0))
				season = m.group()
				if not os.path.exists(os.path.join(pathtosortedfolder,season)):
					os.mkdir(os.path.join(pathtosortedfolder,season))

def move_episodes_to_season_folders(path,pathtosortedfolder,show):

	pattern = re.compile(r'[s|S]\d+')
	for root,dirs,files in os.walk(pathtosortedfolder):
		if root == pathtosortedfolder:
			for f in files:
				m=pattern.search(f.lower())
				if m:
					if m:
						season = m.group()					
					for d in dirs:
						if season == d:
							try:
								shutil.move(os.path.join(root,f),os.path.join(root,d))
							except:
								print('error')
								print('from')
								print(os.path.join(root,f))
								print('to')
								print(os.path.join(root,d))

#delete recently sorted folder
def delete_unnecessary_folders(path,pathtoshowfolder,show,file_endings):
	showlist = show.lower().split()
	reg = ''
	for x in showlist:
		reg += x + '[\s|.|-|\w*]*'

	pattern = re.compile(reg)
	os.chdir(path)
	for root,dirs,files in os.walk(path):
		if root == path:
			for d in dirs:
				m = pattern.search(d.lower())
				if m:
					try:
						shutil.rmtree(os.path.join(root,d))
					except:
						print('error when trying to delete: ', os.path.join(root,d))

def main():

	ugly_endings = ['.nfo','.txt','.dat','.jpg','.png']
	file_endings = ['.avi', '.mpg', '.mp4', '.mkv', '.m4v','.mp3']
	subtitle_endings = ['.srt']

  	#start by getting path and see if it is valid
	path = getpath()
	if path == None:
		print("Path not valid. Exiting program")
		return

	show = input("name of show you want to sort: ")

	#change path, locate script in downloads folder
	os.chdir(path)

	pathtoshowfolder = ''

	#create Shows folder if it doesn't exist
	if not os.path.exists(os.path.join(path, 'Shows')):
		os.mkdir(os.path.join(path,'Shows'))
		pathtoshowfolder = os.path.join(path,'Shows')
	else:
		pathtoshowfolder = os.path.join(path,'Shows')

	#delete all .nfo, .jpg etc
	delete_ugly_endings(path,ugly_endings)
	#moves loose shows to Show folder
	for root,dirs,files in os.walk(path):
		if root == path:
			file_list = list(files)
			move_to_shows(path, file_list,file_endings)
            #move lose shows in download folder to Shows root = download folder

	#print("ugly endings should be gone and a show folder should be here")
	sort_tv_show(path, show, pathtoshowfolder,file_endings,subtitle_endings)

	pathtosortedfolder = create_folder_and_sort(pathtoshowfolder,show,file_endings,subtitle_endings)

	create_season_folders(path,pathtosortedfolder,show)

	move_episodes_to_season_folders(path,pathtosortedfolder,show)

	delete_unnecessary_folders(path,pathtoshowfolder,show,file_endings)





if __name__ == '__main__':
    main()