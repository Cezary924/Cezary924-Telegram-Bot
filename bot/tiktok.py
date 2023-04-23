import requests, os

rapidapi = None

# open file containing RapidAPI key and read from it
def read_rapidapi():
    global rapidapi
    try:
        with open("../rapidapi.txt") as f:
            rapidapi = f.readlines()
        f.close()
    except OSError:
        print("Open error: Could not open the \'rapidapi.txt\' file.")
    rapidapi = str(rapidapi[0])

# handle TikTok urls
def echo_tiktok(message, bot):
    url = "https://tiktok-full-info-without-watermark.p.rapidapi.com/vid/index"
    querystring = {"url":message.text}
    headers = {
        "X-RapidAPI-Key": rapidapi,
        "X-RapidAPI-Host": "tiktok-full-info-without-watermark.p.rapidapi.com"
    }
    bot.send_message(message.chat.id, "Przetwarzanie linku z TikToka... ⏳")
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        bot.send_message(message.chat.id, "Niestety, pobranie filmiku z TikToka nie jest teraz możliwe... Spróbuj poźniej 😞")
        return
    vid_url = response.json()['video'][0]
    response = requests.request("GET", vid_url, headers=headers, params=querystring)
    if response.status_code != 200:
        bot.send_message(message.chat.id, "Niestety, pobranie filmiku z TikToka nie jest teraz możliwe... Spróbuj poźniej 😞")
        return
    vid_name = str(message.chat.id) + str(message.message_id) + ".mp4"
    try:
        with open(vid_name, "wb") as f:
            f.write(response.content)
            f.close()
    except OSError:
        print("Open error: Could not open the \'.mp4\' file.")
    bot.send_video(message.chat.id, open(vid_name, 'rb'))
    os.remove(vid_name)