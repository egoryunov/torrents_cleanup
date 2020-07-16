import os
import re
import time

'''
Useful links:
torrent file structure: https://fileformats.fandom.com/wiki/Torrent_file
open file with buffer for byte-read: http://www.djangospin.com/python-file-buffering/
RegExp for byte search: https://stackoverflow.com/questions/31019854/typeerror-cant-use-a-string-pattern-on-a-bytes-like-object-in-re-findall
'''

def main():
    startTimer = time.perf_counter()


    fileTest = "C:/Users/test/Downloads/Форсаж The Fast and the Furious (Роб Коэн Rob Cohen) [2001, США, боевик, триллер, криминал, WEB-DLRip-AVC] [Open Matte] Dub + [rutracker-5433397].torrent"

    #
    # TEST PUSH
    # TEST PUSH 2
    #


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
    for file in dictTorrentFiles.keys():
        filePath, fileName = dictTorrentFiles[file]['filePath'], dictTorrentFiles[file]['fileName']

        # open file with buffer for byte search
        with open(f"{filePath}\{fileName}", buffering=5) as readFile:
            rawFileContent = readFile.buffer
            torrentHeader = rawFileContent.readline()

            # RegExp should be with rb"mask" for byte search
            reInfoD = re.search(rb"infod(\d+):", torrentHeader)

            currentPos = reInfoD.span()[1]
            reNameD = re.search(rb"4:name(\d+):", torrentHeader[currentPos::])
            nameLength = int(reNameD.group(1))

            currentPos += reNameD.span()[1]
            dictTorrentFiles[file]['localFiles'] = torrentHeader[currentPos:currentPos+nameLength].decode('UTF-8')

    # To check
    for key in dictTorrentFiles.keys():
        print(f"torrent:\t\t{dictTorrentFiles[key]['fileName']}\nfiles:\t\t\t{dictTorrentFiles[key]['localFiles']}\n")

    # # Single file torrent - infod6:length (==6)
    # # Multi files torrent - infod5:files (==5)
    # boolSingleFile = reInfoD.group(1) == "6"
    # print(boolSingleFile)
    #
    # currentPos = reInfoD.span()[1]
    # # if it's a single file torrent
    # if boolSingleFile:
    #     reNameD = re.search(r"4:name(\d+):", torrentHeader[currentPos::])
    #     nameLength = int(reNameD.group(1))
    #     currentPos += reNameD.span()[1]
    #     print(torrentHeader[currentPos:currentPos+nameLength])
    # # if it's a multi files torrent
    # else:
    #     reNameD = re.search(r"4:name(\d+):", torrentHeader[currentPos::])
    #     nameLength = int(reNameD.group(1))
    #     currentPos += reNameD.span()[1]
    #     print(torrentHeader[currentPos:currentPos+nameLength])


    # reBencodingSting = re.compile('(\d+):')
    # for i in range(0, len(torrentHeader)):
    #     char = torrentHeader[i]
    #     if char == 'd':
    #         dictTorrent = {}
    #         if reBencodingSting.match(torrentHeader[i+1::]): keyMatch = int(reBencodingSting.match(torrentHeader[i+1::]).group()[0])
    #         print(keyMatch)

    finishTimer = time.perf_counter()
    print(f"Finished in {round(finishTimer-startTimer, 2)} second(s)")



if __name__ == '__main__':
    main()