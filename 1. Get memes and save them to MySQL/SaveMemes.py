import requests, time, json, mysql.connector
from mysql.connector import Error

# channel "memy po polsku": https://discord.com/api/v9/channels/466637760132939777/messages?limit=50
# channel "śmieszne filmiki": https://discord.com/api/v9/channels/466640797811343380/messages?limit=50

header = {
        'authorization': 'DISCORD_TOKEN_OF_USER_WHO_IS_ON_SERVER_FROM_YOU_GET_MEMES'
}

supoortedFormats = ["jpg", "jpeg", "png", "gif", "webp", "tif", "tiff", "bmp", "svg", "jif", "jfif", "apng", ".mp4", ".webm", ".mov"]

listOfMessageMemes = []

def getMemesFromChannel(linkToChannel):
    print("getMemesFromChannel started for: ", linkToChannel)
    response = requests.get(linkToChannel, headers=header)
    if response.status_code == 200:
        print("Successful called Discord API!")
        for responseElement in response.json():
            responseElementContent = responseElement["content"]

            if responseElementContent.endswith(tuple(supoortedFormats)):
                if responseElementContent.startswith("https"):
                    listOfMessageMemes.append(responseElementContent)

            responseElementAttachments = responseElement["attachments"]
            for responseElementAttachment in responseElementAttachments:
                if responseElementAttachment["url"].endswith(tuple(supoortedFormats)):
                    if responseElementAttachment["url"].startswith("https"):
                        listOfMessageMemes.append(responseElementAttachment["url"])

        for meme in listOfMessageMemes:
            print("Meme link: ", meme)
    else:
        print("Error has occured on calling Discord API! Error status code: ", response.status_code)



# main part of python script:

getMemesFromChannel("https://discord.com/api/v9/channels/466637760132939777/messages?limit=50")
getMemesFromChannel("https://discord.com/api/v9/channels/466640797811343380/messages?limit=50")

try:
    connection = mysql.connector.connect(host='host',
                                        database='database',
                                        user='user',
                                        password='password')
    if connection.is_connected():
        print("Connected to MySQL server")
        cursor = connection.cursor()
        for meme in listOfMessageMemes:
            print("SQL:", "INSERT IGNORE INTO memes (Link) VALUES ('" + meme + "');")
            cursor.execute("INSERT IGNORE INTO memes (Link) VALUES ('" + meme + "');")
        connection.commit()
        print("Successfuly used SQL querries, now closing MySQL connection")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
