'''
NAME:
ADEEB ALI ISLAM
'''


import mysql.connector


obj = mysql.connector.MySQLConnection(host="localhost",user="root",passwd="mysql")
mycursor = obj.cursor(buffered=True)

#CREATING DATABASE
k = 0
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    if x == ('music',):
        k=k+1
    else:
        k=k+0
if k ==1:
    mycursor.execute("USE music")
else:
    mycursor.execute("CREATE DATABASE music")
    obj.commit()


#For listening songs
def listen():
    print("**************** WELCOME TO LISTENING CORNER *******************")
    mycursor.execute("SHOW TABLES")
    print("1. To listen song ")
    print("2. To view favorites")
    print("3. Exit")
    x=input("Choose an option: ")
    if x == '1':#To Show playlist, enlist songs and to get the link of the song for the given input
        print("PLAYLISTS WHICH YOU HAVE SAVED:")
        for x in mycursor:
          print(x)
        name = input("What playlist do you want to see:")
        k = 0
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            if x == (name,):
                k=k+1
            else:
                k=k+0
        if k ==1:
            sql = "SELECT songname FROM %s"%(name,)
            mycursor.execute(sql)
            myrecords = mycursor.fetchall()
            if len(myrecords) != 0:
               print("These are songs in the playlist")
               for x in myrecords:
                   print(x)
            else:
                print("You have saved no songs in this playlist")
                listen()
            
            song_name = input("What song do you want to hear:")
            query="SELECT songname FROM %s"%(name,)
            mycursor.execute(query)
            j=0
            for x in mycursor:
                if x == (song_name,):
                    j=j+1
                else:
                    j=j+0
            if j == 1:
                sql_2 = "SELECT songlink FROM %s WHERE songname='%s'"%(name,song_name)
                mycursor.execute(sql_2)
                myrecords = mycursor.fetchall()
                for x in myrecords:
                    print("Here is your song:",x)
                listen()

            else:
                print("The song doesn't exist. Please try again.")
                listen()
        else:
            print("The playlist doesn't exist, Please try again.")
            listen()
    
                
        
    elif x == '2':#To enlist the favorites in the playlist
        print("PLAYLISTS WHICH YOU HAVE SAVED:")
        for x in mycursor:
          print(x)
        name = input("What playlist do you want to see:")
        k = 0
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            if x == (name,):
                k=k+1
            else:
                k=k+0
        if k ==1:
           sql = "SELECT songname FROM %s WHERE favorite = 'T'"%(name,)
           songs = mycursor.execute(sql)
           myrecords = mycursor.fetchall()
           if len(myrecords) != 0:
               print("These are favorites in the playlist")
               for x in myrecords:
                   print(x)
               listen()
           else:
               print("You have saved no songs as a favorite in this playlist")
               listen()
        else:
            print("The playlist doesn't exist. Please try again.")
            listen()
    elif x == '3':#For exit
        menu()
    else:#For exception
        print("Invalid input please try again.")
        listen()
            
        
def manage():
    print("**************** WELCOME TO PLAYLIST MANAGEMENT *******************")
    print("1. To create playlist")
    print("2. To update playlist")
    print("3. Exit")
    x=input("Choose an option: ")
    while True:
        if x == '1':#For playlist creation
            name = input("Name of the new playlist?:")
            k = 0
            mycursor.execute("SHOW TABLES")
            for x in mycursor:
                if x == (name,):
                    k=k+1
                else:
                    k=k+0
            if k ==1:
                print("Playlist already exists")
                manage()
            else:
                query = "CREATE TABLE %s (songname varchar(30) PRIMARY KEY NOT NULL, songlink varchar(1000) NOT NULL, favorite varchar(7))" %(name,)
                mycursor.execute(query)
                obj.commit()
                print("Playlist created.")
                manage()
        elif x == '2':#To update playlist
            update()
        elif x == '3':#For exit
            menu()
        else:#For exception
           print("Invalid input please try again.")
           manage()


def update():
    print("**************** WELCOME TO PLAYLIST UPDATION CORNER *******************")
    print("1. To add a new song")
    print("2. To delete a song")
    print("3. To mark a favorite")
    print("4. To unmark a favorite")
    print("5. Exit")
    x=input("Choose a option: ")
    while True:
        if x == '1':#To add a new song
            mycursor.execute("SHOW TABLES")
            print("PLAYLISTS WHICH YOU HAVE SAVED:")
            for x in mycursor:
              print(x)
            name = input("Name of the playlist?:")
            k = 0
            mycursor.execute("SHOW TABLES")
            for x in mycursor:
                if x == (name,):
                    k=k+1
                else:
                    k=k+0
            if k ==1:
                song_name = input("What is the name of new song?")
                song_link = input("Please put the link:")
                query_1 = "select * from %s" %(name,)
                mycursor.execute(query_1)
                rec = mycursor.rowcount
                query="INSERT INTO {table} VALUES(%s,%s,'F')"
                mycursor.execute(query.format(table= name),(song_name,song_link))
                obj.commit()
                print("New Song",song_name,"added to Playlist",name,"successfully.")
                update()
            else:
                print("The playlist doesn't exist")
                update()
        elif x == '2':#To delete song
            mycursor.execute("SHOW TABLES")
            print("PLAYLISTS WHICH YOU HAVE SAVED:")
            for x in mycursor:
              print(x)
            name = input("Name of the playlist?:")
            k = 0
            mycursor.execute("SHOW TABLES")
            for x in mycursor:
                if x == (name,):
                    k=k+1
                else:
                    k=k+0
            if k ==1:
                sql = "SELECT songname FROM %s"%(name,)
                mycursor.execute(sql)
                myrecords = mycursor.fetchall()
                if len(myrecords) != 0:
                   print("These are songs in the playlist")
                   for x in myrecords:
                       print(x)
                song_name = input("What is the name of song to delete?:")
                query_1="SELECT songname FROM %s"%(name,)
                mycursor.execute(query_1)
                j=0
                for x in mycursor:
                    if x == (song_name,):
                        j=j+1
                    else:
                        j=j+0
                if j == 1:
                    query_2 = "DELETE FROM %s WHERE songname='%s'"%(name,song_name)
                    mycursor.execute(query_2)
                    print("Song has been deleted.")
                    obj.commit()
                    update()
                else:
                    print("The song doesn't exist. Please try again.")
                    update()
                #query to find if song exist if yes delete if no return back
            else:
                print("The playlist doesn't exist")
                update()
        elif x == '3':#To mark a favorite
            mycursor.execute("SHOW TABLES")
            print("PLAYLISTS WHICH YOU HAVE SAVED:")
            for x in mycursor:
              print(x)
            name = input("Name of the playlist?:")
            k = 0
            mycursor.execute("SHOW TABLES")
            for x in mycursor:
                if x == (name,):
                    k=k+1
                else:
                    k=k+0
            if k ==1:
                sql = "SELECT songname FROM %s"%(name,)
                mycursor.execute(sql)
                myrecords = mycursor.fetchall()
                if len(myrecords) != 0:
                   print("These are songs in the playlist")
                   for x in myrecords:
                       print(x)
                song_name = input("What is the name of song to make a favorite?")
                query_1="SELECT songname FROM %s"%(name,)
                mycursor.execute(query_1)
                j=0
                for x in mycursor:
                    if x == (song_name,):
                        j=j+1
                    else:
                        j=j+0
                if j == 1:
                    query_2 = "UPDATE %s SET favorite='T' WHERE songname = '%s'"%(name,song_name)
                    mycursor.execute(query_2)
                    obj.commit()
                    print("The song",song_name,"is now one of your favorite's")
                    update()
                else:
                    print("The song doesn't exist. Please try again.")
                    update()
                #query to find if song exist if yes mark favorite if no return back
            else:
                print("The playlist doesn't exist")
                update()
        elif x == '4':#To unmark a favorite
            mycursor.execute("SHOW TABLES")
            print("PLAYLISTS WHICH YOU HAVE SAVED:")
            for x in mycursor:
              print(x)
            k = 0
            name = input("Name of the playlist?:")
            mycursor.execute("SHOW TABLES")
            for x in mycursor:
                if x == (name,):
                    k=k+1
                else:
                    k=k+0
            if k ==1:
                sql = "SELECT songname FROM %s"%(name,)
                mycursor.execute(sql)
                myrecords = mycursor.fetchall()
                if len(myrecords) != 0:
                   print("These are songs in the playlist")
                   for x in myrecords:
                       print(x)
                song_name = input("What is the name of song to mark unfavorite?")
                query_1="SELECT songname FROM %s"%(name,)
                mycursor.execute(query_1)
                j=0
                for x in mycursor:
                    if x == (song_name,):
                        j=j+1
                    else:
                        j=j+0
                if j == 1:
                    query_2 = "UPDATE %s SET favorite='F' WHERE songname = '%s'"%(name,song_name)  
                    mycursor.execute(query_2)
                    obj.commit()
                    print("The song",song_name,"has been unmarked as a favorite")
                    update()
                else:
                    print("The song doesn't exist. Please try again.")
                    update()
                #query to find if song exist if yes mark favorite if no return back
            else:
                print("The playlist doesn't exist")
                update()    
        elif x == '5':#For exit
            manage()
        else:#For exception
            print("Invalid input please try again.")
            update()

#interface
def menu():
     print("**************** WELCOME *******************")
     print("1. To listen")
     print("2. To manage playlist")
     print("3. Exit")
     x=input("Choose a option: ")
     if x=='1':
        listen()
     elif x=='2':
        manage()
     elif x=='3':
        print('Thankyou')
        exit()
     else:#For exception
        print("************PLEASE CHOOSE A CORRECT OPTION******************")
        menu()

menu()

































