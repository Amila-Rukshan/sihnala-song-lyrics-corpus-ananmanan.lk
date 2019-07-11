from bs4 import BeautifulSoup
import requests
import copy
import json
import uuid

def findSongSinger(song_name_singer):
    song_name_singer = song_name_singer.split(' ')
    del song_name_singer[0] # remove numbering
    del song_name_singer[-1] # remove date 

    singer = ""
    song = ""
    a =True
    for chunk in song_name_singer:
        if chunk=="-":
            a = False
            continue
        if a:
            singer += (chunk+" ")
        else:
            song += (chunk+" ")
    
    return song, singer




songs_starts_with = ['s','t','u','v','w','y'] # 'a','b','c','d','e','g','h','i','j','k','l','m','n','o','p','r',

for letter in songs_starts_with:

    data_songs= [] 

    print (letter)

    number = 1

    page_link = f'http://www.ananmanan.lk/sinhala-lyrics/lyrics/lyrics-by-{letter}/1'

    page_response = requests.get(page_link, timeout=5)

    page_content = BeautifulSoup(page_response.content, "html.parser")

    number_of_pages = int(page_content.find("div", {"class": "mp3fulllist"}).text.split(" ")[-1])

    print(number_of_pages)

    for number in range(1, number_of_pages+1):

        page_link_2 = f'http://www.ananmanan.lk/sinhala-lyrics/lyrics/lyrics-by-{letter}/{number}'

        page_response_2 = requests.get(page_link_2, timeout=5)

        page_content_2 = BeautifulSoup(page_response_2.content, "html.parser")
        songs = page_content_2.find_all("div", {"class": "mp3"})

        print (len(songs))

        for song in songs:
            
            s = copy.copy(song)

            s = str(s.text)
            # print(s.text)
            singer_name, song_name  = findSongSinger(s)

            song_link = "http://www.ananmanan.lk/sinhala-lyrics/lyric-unicode/"+str(song.find_all("a", href=True)[0]['href'])[12::]

            song_response = requests.get(song_link, timeout=1000)
            song_content = BeautifulSoup(song_response.content, "html.parser")

            song_lyric = song_content.findAll("div", {"class": "lyric-unicode"})

            # print (type(song_lyric[0].text.decode( 'unicode-escape' )))

            # song_lyric[0].text.decode("utf8")

            if (len(song_lyric[0].text)>0):
                
                data_songs.append({  
                    'uuid': str(uuid.uuid1()),
                    'song': song_name,
                    'singer': singer_name,
                    'lyricUnicode':  str(song_lyric[0].text)
                })


    with open(f'{letter}.json', 'w') as outfile:  
        json.dump(data_songs, outfile, indent=4 )
        
  

# textContent = []
# for i in range(0, 5):
    
#     textContent.append(paragraphs)
#     print(paragraphs)
