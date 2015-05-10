# Cleaner
##Programming Project 4, T-308-PRLA

Run script with *python cleaner.py*

The script will ask for two inputs.
Full path to the download folder that you want to sort as well as the name of the show.
The name of the show must be correctly written because in the sorting process it will create a folder determined by user input and the input determines the regex string used to find the video files.

The scripts goes through the following steps:

1. Creates a Show folder if it doesn't already exist
2. Deletes all files with endings specified in ugly_endings list
3. All files in the download folder that end with formats specified in file_endings list are moved to the newly created Show folder.
4. Go through the download folder and find folders containing the show you asked to sort and move only the video files to Show folder
5. Inside Show folder create a folder for the show specified by user and put all video files in that folder
6. Create Season folders for the shows
7. Move video files to appropriate season folders. This works well with the format ...S02E13. Shows containing other formats for seasons and episodes will be unsorted in a folder with the same name as the show.
8. Remove folders from download folder that previously contained the show you wanted to sort.


