# This is a sample Python script.
import Addons
from Addons import Artist, Album, Song, Genre, Tag, get_filtered_songs
from DSFactory import Factory
from DSnest import LinkedList
from Users import User
from login import LoginView


# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    # Use a breakpoint in the code line below to debug your script.
    app = LoginView()


def set_app():
    app = Factory()
    user1 = User("Carla", "torta2")
    user2 = User("Tomas", "torta2")
    user3 = User("Cecilia", "torta2")
    user4 = User("Diego", "torta2")
    app.add_user(user1)
    app.add_user(user2)
    app.add_user(user3)
    app.add_user(user4)

    pop = Genre("pop".upper())
    rock = Genre("rock".upper())
    metal = Genre("metal".upper())
    lofi = Genre("lofi".upper())
    app.add_genre(pop)
    app.add_genre(rock)
    app.add_genre(metal)
    app.add_genre(lofi)

    a1 = Artist("001", "Kali", "USA", False)
    al1 = Album("Weather", "2017")
    a1.add_album(al1)
    app.add_artist(a1)
    s1 = Song("Hazel", "sh7agA", al1, a1, al1.year, 115, pop, "https://www.youtube.com/watch?v=lp7SDPPbx-s")
    app.add_song(s1)

    a2 = Artist("002", "Mirella", "COL", False)
    al2 = Album("Lucero", "2018")
    a2.add_album(al2)
    app.add_artist(a2)
    s2 = Song("CruzDeSol", "a8a9HA", al2, a2, al2.year, 101, lofi, "https://www.youtube.com/watch?v=lp7SDPPbx-s")
    app.add_song(s2)

    a3 = Artist("003", "Aztecombo", "MX", True)
    al3 = Album("SandiaWine", "2015")
    a3.add_album(al3)
    app.add_artist(a3)
    s3 = Song("Ganzua", "0A89lg", al3, a3, al3.year, 110, rock, "https://www.youtube.com/watch?v=vKgqf1Bo_UI")
    app.add_song(s3)

    a4 = Artist("004", "Angy-G", "MX", False)
    al4 = Album("Alors", "2013")
    a4.add_album(al4)
    app.add_artist(a4)
    s4_1 = Song("Voux", "H97gAa", al4, a4, al4.year, 50, pop, "https://www.youtube.com/watch?v=PrURjtcpBgU")
    s4_2 = Song("Trem", "ah76oP", al4, a4, al4.year, 56, rock, "https://www.youtube.com/watch?v=PrURjtcpBgU")
    s4_3 = Song("Claim", "h7Gaf1", al4, a4, al4.year, 53, pop, "https://www.youtube.com/watch?v=PrURjtcpBgU")
    s4_4 = Song("Solitude", "aj89aG", al4, a4, al4.year, 56, rock, "https://www.youtube.com/watch?v=PrURjtcpBgU")
    app.add_song(s4_1)
    app.add_song(s4_2)
    app.add_song(s4_3)
    app.add_song(s4_4)

    a5 = Artist("005", "Howler", "CDA", False)
    al5 = Album("Luxury", "2021")
    a5.add_album(al5)
    app.add_artist(a5)

    s5 = Song("Beach", "1la0AG", al5, a5, al5.year, 49, pop, "https://www.youtube.com/watch?v=WSukD4Y_QY0")
    s5.add_tag(Tag("Trending"))
    s5.add_tag(Tag("Alelux"))
    s5.add_tag(Tag("Partrend"))
    s5.add_tag(Tag("Atrendding"))
    app.add_song(s5)

    app.add_user_song(user1, s2)
    app.add_user_song(user1, s5)
    app.add_user_song(user1, s4_4)
    app.add_user_song(user1, s1)
    app.add_user_song(user1, s4_1)

    print(str(s5.contains_true_tag(Tag("ding"))) + "\n")
    print(str(s5.contains_partial_tag(Tag("ding"))) + "\n")
    print("Compatibility of tag 'Trend' in all tags of all songs in app\n")

    for song in app.get_songs():
        for tag in song.get_all_tags():
            print(song.get_name(), tag.get_attribute(), "== Trend ->", str(tag.get_compatibility(Tag("Trend"))))
    print("\n----------------------------------------------------------------")
    print("Compatibility of tag 'a' in all tags of all songs in app\n")

    for song in app.get_songs():
        for tag in song.get_all_tags():
            print(song.get_name(), tag.get_attribute(), "== a ->", str(tag.get_compatibility(Tag("a"))))
    print("\n----------------------------------------------------------------")
    print("All tags compatible with 'a' of all songs in app\n")

    for song in app.get_songs():
        for tag in song.get_filtered_tags(Tag("a")):
            print(song.get_name(), tag.get_attribute())
    print("\n----------------------------------------------------------------")
    print("All songs in app\n")

    for song in app.get_songs():
        artist = song.get_artist()
        print(song.get_name(), song.get_id(), artist.get_name(), song.get_url())
    print("\n----------------------------------------------------------------")
    print("Songs in user1\n")

    for song in user1.get_song_list():
        artist = song.get_artist()
        print(song.get_name(), song.get_id(), artist.get_name(), song.get_url())
    print("\n----------------------------------------------------------------")
    print("Songs in user1 after 1 delete\n")

    user1.delete_song(s5)

    for song in user1.get_song_list():
        artist = song.get_artist()
        print(song.get_name(), song.get_id(), artist.get_name(), song.get_url())
    print("\n----------------------------------------------------------------")
    print("Songs in user1 after 1 undo\n")

    user1.undo()

    for song in user1.get_song_list():
        artist = song.get_artist()
        print(song.get_name(), song.get_id(), artist.get_name(), song.get_url())
    print("\n----------------------------------------------------------------")
    print("Songs in user1 after 1 redo\n")

    user1.redo()

    for song in user1.get_song_list():
        artist = song.get_artist()
        print(song.get_name(), song.get_id(), artist.get_name(), song.get_url())
    print("\n----------------------------------------------------------------")
    print("Songs in user1 after 1 undo\n")
    user1.undo()

    for song in user1.get_song_list():
        artist = song.get_artist()
        print(song.get_name(), song.get_id(), artist.get_name(), song.get_url())
    print("\n----------------------------------------------------------------")

    print("All users\n")

    for user in app.get_users():
        print(user.username)

    print("\n----------------------------------------------------------------")
    print("Songs compatible with 'PoP and 'aLOr'")

    aux_tags = LinkedList[Tag]()
    aux_tags.append(Tag("PoP"))
    aux_tags.append(Tag("aLOr"))

    for song in get_filtered_songs(aux_tags, app.get_songs()):
        print(song.get_name())
    print("\n----------------------------------------------------------------")

    for genre in Addons.genre_with_most_songs(app.get_genres()):
        print(genre.get_name())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    # set_app()
