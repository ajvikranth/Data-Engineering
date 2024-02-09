import json
import pymysql.cursors
from datetime import datetime


# Connect to the database
# connection = pymysql.connect(host='192.168.56.102',
#                              user='hadoop2',
#                              password='Qwerty@123',
#                              database='anime',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

connection = pymysql.connect(host='172.18.0.1',
                             user='hd',
                             password='Qwerty@123',
                             database='anime',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def insert(table_obj,table):

    if table == 'Descriptions':

        with connection.cursor() as cursor:
            print("INSERT INTO `descriptions` (`malID`, `url`,`Synonyms`,`Japanese`,`English`,`Type`,`Episodes`,`Status`,`Score`,`Ranked`,`Popularity`,`Members`,`Favorites`,`Premiered`,`Source`,`StartDate`,`EndDate`,`Broadcast-day`,`Rating`,`Duration-mins`) VALUES(",table_obj['malID'], table_obj['url'], table_obj['Synonyms'], table_obj['Japanese'], table_obj['English'], table_obj['Type'], table_obj['Episodes'], table_obj['Status'], table_obj['Score'], table_obj['Ranked'], table_obj['Popularity'], table_obj['Members'], table_obj['Favorites'], table_obj['Premiered'], table_obj['Source'], table_obj['StartDate'], table_obj['EndDate'], table_obj['Broadcast-day'], table_obj['Rating'], table_obj['Duration-mins'],")")
            sql = "INSERT INTO `descriptions` (`malID`, `url`,`Synonyms`,`Japanese`,`English`,`Type`,`Episodes`,`Status`,`Score`,`Ranked`,`Popularity`,`Members`,`Favorites`,`Premiered`,`Source`,`StartDate`,`EndDate`,`Broadcast-day`,`Rating`,`Duration-mins`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (table_obj.get('malID'), table_obj.get('url'), table_obj.get('Synonyms'), table_obj.get('Japanese'), table_obj.get('English'), table_obj.get('Type'), table_obj.get('Episodes'), table_obj.get('Status'), table_obj.get('Score'), table_obj.get('Ranked'), table_obj.get('Popularity'), table_obj.get('Members'), table_obj.get('Favorites'), table_obj.get('Premiered'), table_obj.get('Source'), table_obj.get('StartDate'), table_obj.get('EndDate'), table_obj.get('Broadcast-day'), table_obj.get('Rating'), table_obj.get('Duration-mins')))
        connection.commit()
        

    elif table == 'Studios':
        for obj in table_obj:
            with connection.cursor() as cursor:
                print("INSERT INTO `Studios` (`sID`, `Studios`) VALUES (",table_obj[obj], obj,")")
                sql = "INSERT INTO `Studios` (`sID`, `Studios`) VALUES (%s, %s)"
                cursor.execute(sql, (table_obj[obj], obj))
            connection.commit()    
    
    elif table == 'Producers':
        for obj in table_obj:
            with connection.cursor() as cursor:
                print("INSERT INTO `Producers` (`pID`, `Producers`) VALUES (",table_obj[obj], obj,")")
                sql = "INSERT INTO `Producers` (`pID`, `Producers`) VALUES (%s, %s)"
                cursor.execute(sql, (table_obj[obj], obj))
            connection.commit()
    
    elif table == 'Licensors':
        for obj in table_obj:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `Licensors` (`lID`, `Licensors`) VALUES (%s, %s)"
                cursor.execute(sql, (table_obj[obj], obj))
            connection.commit()

    elif table == 'Genres':
        for obj in table_obj:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `Genres` (`gID`, `Genres`) VALUES (%s, %s)"
                cursor.execute(sql, (table_obj[obj], obj))
            connection.commit()      

    elif table == 'animeStudios':
        with connection.cursor() as cursor:
            sql = "INSERT INTO `animeStudios` (`malID`,`sID` ) VALUES (%s, %s)"
            cursor.execute(sql,table_obj )
        connection.commit() 

    elif table == 'animeProducers':
        with connection.cursor() as cursor:
            sql = "INSERT INTO `animeProducers` (`malID`,`pID` ) VALUES (%s, %s)"
            cursor.execute(sql,table_obj )
        connection.commit() 

    elif table == 'animeLicensors':
        with connection.cursor() as cursor:
            sql = "INSERT INTO `animeLicensors` (`malID`,`lID` ) VALUES (%s, %s)"
            cursor.execute(sql,table_obj )
        connection.commit() 

    if table == 'animeGenres':
        with connection.cursor() as cursor:
            sql = "INSERT INTO `animeGenres` (`malID`,`gID` ) VALUES (%s, %s)"
            cursor.execute(sql,table_obj )
        connection.commit() 

    


    

# need to edit such runs from data on hdfs
        
from hdfs import InsecureClient
from json import load

client = InsecureClient('http://localhost:9870', user='aj')

with client.read('/user/aj/MAL.json', encoding='utf-8') as reader:
  
  animes = load(reader)
            
# f = open("data/MAL.json",encoding='utf-8')

# animes = json.load(f)

#############################################


descriptions_obj = {}
studios_obj = set()
Producers_obj = set()
Licensors_obj =set()
genres_obj =set()


id=0

for anime in animes:


    descriptions_obj['malID'] = id
    descriptions_obj["url"] = anime.get('url')
    descriptions_obj['Synonyms'] = anime.get('Synonyms')
    descriptions_obj['Japanese'] =anime.get('Japanese')
    descriptions_obj['English'] =anime.get('English')

    descriptions_obj['Type'] = anime.get('Type')
    Episodes = anime.get('Episodes')
    if Episodes:
        if  isinstance(Episodes,int):
            descriptions_obj['Episodes'] = Episodes
        else:
            descriptions_obj['Episodes'] = None

    
    descriptions_obj['Status'] = anime.get('Status')
    descriptions_obj["Score"] = anime.get("Score")
    Ranked = anime.get("Ranked")
    if Ranked:
        if  isinstance(Ranked,int):
            descriptions_obj['Ranked'] = Ranked
        else:
            descriptions_obj['Ranked'] = None

    
    descriptions_obj["Popularity"] = anime.get("Popularity")
    descriptions_obj["Members"] = anime.get("Members")
    descriptions_obj["Favorites"] = anime.get("Favorites")
    descriptions_obj["Premiered"] = anime.get("Premiered")
    descriptions_obj["Source"] = anime.get("Source")

    aired = anime.get("Aired")
    if aired:
        date_l = aired.split(' ')
        if date_l[-1] =='?':
            descriptions_obj['EndDate'] = None

        else:
            descriptions_obj['EndDate'] = datetime.strptime(" ".join(date_l[-3:]), "%b %d %Y")
            descriptions_obj['StartDate'] = datetime.strptime(" ".join(date_l[:3]), "%b %d %Y")

    
    broadcast = anime.get("Broadcast")
    if broadcast:
        descriptions_obj["Broadcast-day"] = broadcast.split(" ")[0]


    Rating = anime.get("Rating")
    if Rating:
        descriptions_obj["Rating"] = Rating.split(" ")[0]

    
    Duration = anime.get("Duration")
    if Duration:
        Duration_l = Duration.split(" ")
        if Duration_l[1] == 'min.':
            descriptions_obj["Duration-mins"] = int(Duration_l[0])
        elif Duration_l[-1] == 'min.':  
            descriptions_obj["Duration-mins"] = int(Duration_l[0])*60 + int(Duration_l[2])

    
    insert(descriptions_obj,'Descriptions')

    id+=1






########################################################################################
   
    Studios = anime.get("Studios")

    if Studios:
        if isinstance(Studios, str):
            studios_obj.add(Studios)
        elif isinstance(Studios, list):
            studios_obj.update(Studios)



    
    Producers = anime.get("Producers")

    if Producers:
        if isinstance(Producers, str):
            Producers_obj.add(Producers)
        elif isinstance(Producers, list):
            Producers_obj.update(Producers)

                

    Licensors = anime.get("Licensors")

    if Licensors:
        if isinstance(Licensors, str):
            Licensors_obj.add(Licensors)
        elif isinstance(Licensors, list):
            Licensors_obj.update(Licensors)

    Genres = anime.get("Genres")

    if Genres:
        if isinstance(Genres, str):
            genres_obj.add(Genres)
        elif isinstance(Genres, list):
            genres_obj.update(Genres)
    
    Genre = anime.get("Genre")

    if Genre:
        if isinstance(Genre, str):
            genres_obj.add(Genre)
        elif isinstance(Genre, list):
            genres_obj.update(Genre)

    Themes = anime.get("Themes")
    
    if Themes:
        if isinstance(Themes, str):
            genres_obj.add(Themes)
        elif isinstance(Themes, list):
            genres_obj.update(Themes)
    
    Theme = anime.get("Theme")

    if Theme:
        if isinstance(Theme, str):
            genres_obj.add(Theme)
        elif isinstance(Theme, list):
            genres_obj.update(Theme)
    

studios_obj.discard("None found")
studios_obj.discard("add some")

Studios_dict = {key: value for value, key in enumerate(studios_obj)}

insert(Studios_dict,'Studios')

Producers_obj.discard("None found")
Producers_obj.discard("add some")

Producers_dict = {key: value for value, key in enumerate(Producers_obj)}

insert(Producers_dict,'Producers')

Licensors_obj.discard("None found")
Licensors_obj.discard("add some")

Licensors_dict = {key: value for value, key in enumerate(Licensors_obj)}



insert(Licensors_dict,'Licensors')

genres_obj.discard("None found")
genres_obj.discard("add some")

Genres_dict = {key: value for value, key in enumerate(genres_obj)}



insert(Genres_dict,'Genres')

print(Genres_dict)


id =0 

for anime in animes:

    Studios = anime.get("Studios")

    if Studios:
  
        if isinstance(Studios, str):

            sID = Studios_dict.get(Studios)
            if sID == None:
                continue

            malID = id

            insert((malID,sID),"animeStudios")

                #insert into connection table
                
        else:

            for j in Studios:
                sID = Studios_dict.get(j)
                if sID == None:
                    continue
                malID = id

                insert((malID,sID),"animeStudios")

                # insert  into connection table
                
    Producers = anime.get("Producers")

    if Producers:
  
        if isinstance(Producers, str):

            pID = Producers_dict.get(Producers)
            if pID == None:
                continue

            malID = id

            insert((malID,pID),"animeProducers")

            #insert into connection table
                
        else:

            for j in Producers:
                pID = Producers_dict.get(j)
                if pID == None:
                    continue
                malID = id

                insert((malID,pID),"animeProducers")
                
            
                # insert  into connection table
    
    Licensors = anime.get("Licensors")

    if Licensors:
  
        if isinstance(Licensors, str):

            lID = Licensors_dict.get(Licensors)
            if lID == None:
                continue

            malID = id

            insert((malID,lID),"animeLicensors")
           

                #insert into connection table
                
        else:

            for j in Licensors:
                lID = Licensors_dict.get(j)
                if lID == None:
                    continue
                malID = id

                insert((malID,lID),"animeLicensors")
            

                    # insert  into connection table
    
    Genres = anime.get("Genres")

    if Genres:

        if isinstance(Genres, str):

            gID = Genres_dict.get(Genres)
            if gID == None:
                continue

            malID = id
            insert((malID,gID),"animeGenres")
          
        else:
            for j in Genres:
                gID = Genres_dict.get(j)
                if gID == None:
                    continue
                malID = id

                insert((malID,gID),"animeGenres")

               
    
    Genre = anime.get("Genre")

    if Genre:
        if isinstance(Genre, str):

            gID = Genres_dict.get(Genre)
            if gID == None:
                continue

            malID = id
            insert((malID,gID),"animeGenres")
            

        else:
            for j in set(Genre):
                gID = Genres_dict.get(j)
                if gID == None:
                    continue
                malID = id
                insert((malID,gID),"animeGenres")

               

    Themes = anime.get("Themes")
    
    if Themes:
        if isinstance(Themes, str):

            gID = Genres_dict.get(Themes)
            if gID == None:
                continue

            malID = id
            insert((malID,gID),"animeGenres")
            

        else:
            for j in Themes:
                gID = Genres_dict.get(j)
                if gID == None:
                    continue
                malID = id
                insert((malID,gID),"animeGenres")

                
    
    Theme = anime.get("Theme")

    if Theme:
        if isinstance(Theme, str):

            gID = Genres_dict.get(Theme)
            if gID == None:
                continue

            malID = id
            insert((malID,gID),"animeGenres")
            

        else:
            for j in set(Theme):
                gID = Genres_dict.get(j)
                if gID == None:
                    continue
                malID = id
                insert((malID,gID),"animeGenres")

                
    id+=1            





    














    
    




    




