from github import Github
import requests
import json

def main():
    gitToken = input("GitHub Input Token : ")
    songToken = input("Song Input Token : ")
    list = []
    list = getInfoFromGitHub(gitToken, songToken)
    countsDict =  listToDictWithCount(list)
    with open("artist.json", "w") as outfile:
        json.dump(countsDict, outfile)
    with open("myfile.txt", 'w') as f: 
        for key, value in countsDict.items(): 
            f.write('%s:%s\n' % (key, value))
    
    
def listToDictWithCount(list):
    countsDict = dict()
    for i in list:
        countsDict[i] = countsDict.get(i, 0) + 1
    return countsDict

def getInfoFromGitHub(gitToken,songToken):
    g = Github(login_or_token=gitToken)

    repo = g.get_repo("hci-singaporetech/ict2102-lab02-2022")
    contents = repo.get_contents("")
    list = []
    count = len(contents)
    while len(contents)>0:
        file_content = contents.pop(0)
        firstLineOfFile = file_content.decoded_content.decode("utf-8").split("\n")[0]
        list.append(findSongViaShazam(firstLineOfFile,songToken))
        print(count," items left ")
        count -= 1
    return list


def findSongViaShazam(titleAndArtist,songToken):
    url = "https://shazam.p.rapidapi.com/search"

    querystring = {"term":titleAndArtist,"locale":"en-US","limit":"1"}

    headers = {
        "X-RapidAPI-Key": songToken,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        return(response.json()["artists"]["hits"][0]["artist"]["name"])
    except:
        return("Cannot find Song")
    
    
main()