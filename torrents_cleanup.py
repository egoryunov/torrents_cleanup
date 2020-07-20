import os
import re
import time
import subprocess

'''
Useful links:
torrent file structure: https://fileformats.fandom.com/wiki/Torrent_file
open file with buffer for byte-read: http://www.djangospin.com/python-file-buffering/
RegExp for byte search: https://stackoverflow.com/questions/31019854/typeerror-cant-use-a-string-pattern-on-a-bytes-like-object-in-re-findall
'''

def main():
    startTimer = time.perf_counter()

    # Scan 'Downloads' folder for torrent files.
    # Store them in lstTorrentFiles[(path, file)]
    # dictTorrentFiles = {'torrentFileName': {'filePath':path, 'fileName':name}}
    dictTorrentFiles = {}
    reTorrentFile = re.compile('.+\.torrent')
    for root, dirs, files in os.walk('C:/Users/test/Downloads'):
        for file in files:
            if reTorrentFile.match(file):
                dictTorrentFiles[file] = {}
                dictTorrentFiles[file]['filePath'] = root
                dictTorrentFiles[file]['fileName'] = file

    # Add some comments to check github
    # Loop through list of torrent files and extracts where it stores local files
    # add result to
    # dictTorrentFiles = {'torrentFileName': {'localFiles': file/dir}}
    # and
    # dictTorrentFiles = {'torrentFileName': {'singleFiles': true/false}}
    for torrentFile in dictTorrentFiles.keys():
        filePath, fileName = dictTorrentFiles[torrentFile]['filePath'], dictTorrentFiles[torrentFile]['fileName']

        # open file with buffer for byte search
        with open(f"{filePath}/{fileName}", buffering=5) as readFile:
            rawFileContent = readFile.buffer
            torrentHeader = rawFileContent.readline()

            # RegExp should be with rb"mask" for byte search
            reInfoD = re.search(rb"infod(\d+):", torrentHeader)
            # Single file torrent - infod6:length (==6)
            # Multi files torrent - infod5:files (==5)
            dictTorrentFiles[torrentFile]['singleFile'] = reInfoD.group(1).decode('UTF-8') == "6"

            # Looking for a name in torrent file
            currentPos = reInfoD.span()[1]
            reNameD = re.search(rb"4:name(\d+):", torrentHeader[currentPos::])
            nameLength = int(reNameD.group(1))

            currentPos += reNameD.span()[1]
            dictTorrentFiles[torrentFile]['localFiles'] = torrentHeader[currentPos:currentPos+nameLength].decode('UTF-8')

        # Searching local directories for download files
        # reDownloadedFile = re.compile(rf"{dictTorrentFiles[torrentFile]['localFiles']}")
        for root, dirs, files in os.walk('C:/Users/test/Downloads'):
            if dictTorrentFiles[torrentFile]['singleFile'] == False:
                for dir in dirs:
                    if dictTorrentFiles[torrentFile]['localFiles']==dir:
                        dictTorrentFiles[torrentFile]['downloadedFiles'] = root + '/' + dir
            else:
                for file in files:
                    if dictTorrentFiles[torrentFile]['localFiles']==file:
                        dictTorrentFiles[torrentFile]['downloadedFiles'] = root + '/' + file


    # adding torrents to tracker and move them to proper location
    for key in dictTorrentFiles.keys():
        if 'downloadedFiles' in dictTorrentFiles[key]:
            ## !!! UNCOMMENT TO EXECUTE (SUBPROCESS)
            # Add torrent file if it's downloaded
            fileToDownload = dictTorrentFiles[key]['filePath'] + '\\' + dictTorrentFiles[key]['fileName']
            dirToDownload = 'C:/Users/test/Downloads/'
            cmdAddTorrent = f'C:/Users/test/AppData/Roaming/uTorrent/uTorrent.exe /DIRECTORY "{dirToDownload}" "{fileToDownload}"'
            print(cmdAddTorrent)
            # subprocess.Popen(cmdAddTorrent)
            time.sleep(5)

            ## !!! UNCOMMENT TO EXECUTE (SUBPROCESS)
            # Move torrent file to flash card
            cmdMvFile = f'MOVE "{fileToDownload}" "C:\\tmp\\"'
            print(cmdMvFile)
            # subprocess.run(cmdMvFile, shell=True)
            time.sleep(5)

    # To check
    # for key in dictTorrentFiles.keys():
    #     if 'downloadedFiles' in dictTorrentFiles[key]:
    #         print(f"torrent:\t\t{dictTorrentFiles[key]['fileName']}\nfiles:\t\t\t{dictTorrentFiles[key]['localFiles']}")
    #         print(f"download:\t\t{dictTorrentFiles[key]['downloadedFiles']}")
    #         print(f"single?:\t\t{dictTorrentFiles[key]['singleFile']}\n")


    finishTimer = time.perf_counter()
    print(f"Finished in {round(finishTimer-startTimer, 2)} second(s)")

if __name__ == '__main__':
    main()