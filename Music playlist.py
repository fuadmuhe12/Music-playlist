import time
import random
from pynput import keyboard


class Song:
    def __init__(self, name, year , artist):
        self.name =  name
        self.yearOf_realese  = year
        self.artist = artist
    def __str__(self):
        return f'Song Name: {self.name}   ~~   artist: {self.artist}   ~~   Year of Realese: {self.yearOf_realese}'
    def __eq__(self, other):
        if isinstance(other, Song):
            return other.name == self.name and other.yearOf_realese == self.yearOf_realese and other.artist == self.artist
        return False

class Song_Node:
    def __init__(self, Song):
        self.Song = Song
        self.previous_song  = None
        self.next_song = None

class MusicPlayList:
    def __init__(self):
        self.__size = 0
        self.head = None
        self.tail = None

    def add(self, e):
        new_Song_Node = Song_Node(e)
        if self.head is None:
            self.head = new_Song_Node
            self.tail = new_Song_Node
            self.__size += 1
        else:
            self.tail.next_song = new_Song_Node
            new_Song_Node.previous_song = self.tail
            self.tail = new_Song_Node
            self.__size += 1
        return True

    def display_songs(self):
        num  = 1
        if self.head is None:
            return None
        else:
            cur = self.head
            while cur is not None:
                print(f'          {num}. {cur.Song} ' )
                cur  = cur.next_song
                num += 1

    def getSize(self):
        return self.__size


    def menu(self):
        menu = '''
                        Welcome to the playlist

                            1. Add song 'format: song--artist--year of release'
                            2. Remove Song By Name
                            3. Search song and Play
                            4. Display songs
                            5. Play
                            6. Shuffle ALL
                            7. Exit

                '''
        print(menu)
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print('ONLY NUMBERS')

    def play(self, song_node):  # here we take link node as argument
        print("=" * 50)
        print("      ~~~~~~~  Now playing  ~~~~~~~"
              "")
        print(f"       Song:             {song_node.Song.name}") #  the song_node has data that is Song class which has details of one song
        print(f"       Artist:           {song_node.Song.artist}")
        print(f'       Year of realese:  {song_node.Song.yearOf_realese}')
        print("=" * 50)
        return song_node

    def removeSong_byName(self, song_name):
        if self.head == None:
            print ("List is empty")
            return
        else:
            temp = self.head
            while temp is not None:
                if temp.Song.name == song_name:
                    if temp.previous_song is not None:
                        temp.previous_song.next_song = temp.next_song
                    else:
                        self.head = temp.next_song
                    if self.getSize() > 1:
                        self.head.previous_song = None
                       
                    self.__size -= 1
                    print('Successful')
                    return True
                temp = temp.next_song
            print("Song not Found")
            return


    def Search_by_Name_and_Play(self, song_name):
        if self.head == None:
            return "List is empty"
        else:
            temp = self.head
            while temp != None:
                if temp.Song.name == song_name:
                    curr_song = self.play(temp)
                    return curr_song
                temp = temp.next_song
            print('Not Found')


            return self.head

    def exit(self):
        print("Thank you for using the playlist")
        exit()

    def previous(self, song_node):
        if self.head == None:
            print("List is empty")
            return
        else:
            temp = song_node
            if temp.previous_song is not None:
                self.play(temp.previous_song)
                return
            print("No previous song")
            return

    def next(self, song_node):

        if self.head == None:
            print("List is empty")
        else:
            temp = song_node
            if temp is not None:
                if temp.next_song:
                    self.play(temp.next_song)
                    return
            print("No next song")

    def detect_keyboard_input(self, time_frame):
        start_time = time.time()  
        keyboard_input = False  

        def on_press(key):
            nonlocal keyboard_input
            keyboard_input = True

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while time.time() - start_time < time_frame:
            if keyboard_input:
                break

        listener.stop()  

        return keyboard_input

    def shuffleSong(self):
        if self.head is None:
            print("Playlist is empty.")

        else:
            map_song_to_list = {}
            curr = self.head
            for i in range(self.getSize()):
                map_song_to_list[i] = curr
                if curr.next_song is not None:
                    curr = curr.next_song
            lists = []
            for i in range(self.getSize()):
                lists.append(i)
            while True:
                if map_song_to_list.__len__() > 0:
                    x = random.choice(lists)
                else:
                    print('''

                    ####################### End of shuffle #######################

                    ''')
                    break
                temp = map_song_to_list.get(x)
                self.play(temp)
                map_song_to_list.pop(x)
                lists.remove(x)

                print('''

                if you want to leave the shuffle press any key:

                 ''')

                if self.detect_keyboard_input(5): #  5 sec playing time for 1 song
                    break

 # Adding some default songs not to leave the playlist empty!

object = MusicPlayList()
waka_waka = Song('Waka waka','2010','Shakira')
ed = Song('Perfect', '2017', 'Ed Sheeran')
abel = Song('Blinding lights', '2020', 'The Weeknd')
tedy = Song("ህለም አይቼ ማታ", "2012",  "ቴዎድሮስ ካሳሁን")
tilahun = Song("የዘንባባ ማር ነሽ" ,"1992" , "ጥላሁን ገሰሰ")

object.add(waka_waka)
object.add(ed)
object.add(abel)
object.add(tedy)
object.add(tilahun)

def main():
    choice = object.menu()
    try:
        if choice < 1 or choice > 7:
            print("Invalid choice")
            main()
        elif choice == 1:
            try:
                song_name, artist, year = input("Enter the song (song_name--artist--year): ").split("--")
                song = Song(song_name, year, artist)
                object.add(song)
                main()

            except ValueError:
                print("Invalid input. Please enter the song name, artist, and year separated by '--'")
                main()

        elif choice == 2:
            song_name = input("Enter the song name: ")
            object.removeSong_byName(song_name)
            main()
        elif choice == 3:
            song = input("Enter the song name: ")
            curr_song = object.Search_by_Name_and_Play(song)
            while True:
                print('''What would you like to do?
                    1. Play Previous Song
                    2. Play Next Song
                    3. Shuffle All Songs
                    4. Back to Main Menu
                ''')

                choice = int(input("Enter your choice: "))
                if choice == 1:
                    song_node = object.previous(curr_song)
                    if curr_song.previous_song is not None:
                        curr_song = curr_song.previous_song
                elif choice == 2:
                    song_node = object.next(curr_song)
                    if curr_song.next_song is not None:
                        curr_song = curr_song.next_song
                elif choice == 3:
                    object.shuffleSong()
                    main()
                elif choice == 4:
                    break
                else:
                    print("Invalid choice. Please try again.")
            main()
        elif choice == 4:
            object.display_songs()
            main()
        elif choice == 5:
            curr_song = object.play(object.head)
            while True:
                print('''What would you like to do?
                    1. Play Previous Song
                    2. Play Next Song
                    3. Shuffle All Songs
                    4. Back to Main Menu
                ''')

                choice = int(input("Enter your choice: "))
                if choice == 1:
                    song_node = object.previous(curr_song)
                    if curr_song.previous_song is not None:
                        curr_song = curr_song.previous_song
                elif choice == 2:
                    song_node = object.next(curr_song)
                    if curr_song.next_song is not None:
                        curr_song = curr_song.next_song
                elif choice == 3:
                    object.shuffleSong()
                    main()
                elif choice == 4:
                    break
                else:
                    print("Invalid choice. Please try again.")
            main()
        elif choice == 6:
            object.shuffleSong()
            main()
        elif choice == 7:
            object.exit()
    except ValueError:
        print('please Enter numbers only!')
        main()
    except TypeError:
        print('please Enter numbers only!')
        main()



main()

















