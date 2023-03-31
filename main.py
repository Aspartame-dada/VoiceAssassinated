import datetime
import PIL.ImageShow
import speech_recognition as sr   #pyaudio SpeechRecognition模块
def rec(rate=16000):     #从系统麦克风拾取音频数据，采样率为 16000
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")  #这里会打印please say something，提示你说话进行录音
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:   #把采集到的音频数据以 wav 格式保存在当前目录下的recording.wav 文件
        f.write(audio.get_wav_data())
    return 1
from aip import AipSpeech
APP_ID = '31774479'
API_KEY = '4quuiLGGhHA3AoBXrrR1xypm'
SECRET_KEY = 'TpX8ptUclvGjGSdmapRSFirTkxyXKQ4p'  #这三个输入你自己的接口账号密钥哈，我就不放了，有需要可以找我要
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def listen():
    with open('recording.wav', 'rb') as f:    #将录制好的音频文件recording.wav上传至百度语音的服务，返回识别后的文本结果并输出。
        audio_data = f.read()

    results = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,                     #这里的results是一个字典，文本内容在Key名字为result对应的值，这里我恶补了一点字典的知识
    })
    if 'result' in results:
        print("you said: " + results['result'][0])    #results['result']这个是输出Key名字为result对应的值，也就是我们要的文本，至于后面[0]有什么用我还没搞明白，
        return results['result'][0]
    else:
        print("出现错误，错误代码：" , results['err_no'])   #不存在result就返回错误代码err_no
import openai
# 输入你的 api_key
chat_gpt_key = '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'
# 将 Key 进行传入
openai.api_key = chat_gpt_key
def completion(prompt):
    response = openai.Completion.create(
        # text-davinci-003 是指它的模型
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None
    )
    message = response.choices[0].text
    return message
APP_ID = '31775277'
API_KEY = 'IWDdHgYuT8GBrGtlegTmTMFF'
SECRET_KEY = 'BFFGO3COLXziZOIFoVwwTiIIYDSqwMpd'  #这三个输入你自己的接口账号密钥哈，我就不放了，有需要可以找我要
def speak(text=""):
    result = client.synthesis(text, 'zh', 1, {    #这里的参数可以调   zh表示中文
        'spd': 5,   #语速
        'vol': 10,   #音量
        'per': 5,   #类型
    })
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:   #保存为当前目录下mp3格式的音频：audio.mp3，不建议用wav格式，wav格式后面我用的是pygame播放无法识别
            f.write(result)
            f.close()
import pygame
def play():
    pygame.mixer.init()
    pygame.mixer.music.load("D:/MyCode/Project_Python/VoiceAssassinated/audio.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.unload()
import requests
# 替换为你的API key
api_key = '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'
# ChatGPT API的地址
api_url = 'https://api.openai.com/v1/images/generations'
def generate_image(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    # 发送POST请求
    response = requests.post(api_url, headers=headers, json={
        'model': 'image-alpha-001',
        'prompt': prompt,
        'num_images': 1,
        'size': '1024x1024',
        'response_format': 'url'
    })
 # 获取响应中的URL
    response_json = response.json()
    return response_json['data'][0]['url']
from PIL import Image
import io
def save_image(url, filename):
    response = requests.get(url)
    # 将响应中的二进制数据解码为Image对象
    img = Image.open(io.BytesIO(response.content))
    # 保存图像文件
    img.save(filename)
if __name__ == "__main__":
    speak("早上好，我是物联网22级开发的语音助手，请问您有什么需要帮助的")
    play()

    while True:
        rec()  # 保存录音文件：recording.wav
        text = listen()  # 自动打开录音文件recording.wav进行识别,返回 识别的文字存到text

        if str('终止程序') in text:  #这里我设置了一个结束语，说“结束程序”的时候就结束，你也可以改掉
            speak("好的，再见")
            play()
            break
        if str('画') in text:
            speak("好的，正在绘画中，请稍等")
            play()
            url = generate_image(text)
            save_image(url, ('s.jpg'))
            im = Image.open('s.jpg')
            im.show()
            speak("绘画完成了")
            play()
            speak("请问还有什么需要帮助的")
            play()
            rec()  # 保存录音文件：recording.wav
            text = listen()  # 自动打开录音文件recording.wav进行识别,返回 识别的文字存到text
        if str('图') in text:
            speak("好的，正在绘画中，请稍等")
            play()
            url = generate_image(text)
            save_image(url, ('s.jpg'))
            im = Image.open('s.jpg')
            im.show()
            speak("绘画完成了")
            play()
            speak("请问还有什么需要帮助的")
            play()
            rec()  # 保存录音文件：recording.wav
            text = listen()  # 自动打开录音文件recording.wav进行识别,返回 识别的文字存到text

        speak("让我思考一下")
        play()
        gpt_answer=completion(text)
        print(gpt_answer)
        text_1 =  gpt_answer # 将text中的文字发送给机器人，返回机器人的回复存到text_1
        speak(text_1)  # 将text_1中机器人的回复用语音输出，保存为audio.mp3文件
        play() #播放audio.mp3文件
        speak("请问还有什么需要帮助的")
        play()
