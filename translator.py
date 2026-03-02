import time
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import numpy as np
import sounddevice as sd

# إعدادات الحساسية للتصفيق
THRESHOLD = 20
COOLDOWN = 1.5
clap_count = 0
last_clap_time = 0


# 1. القاموس العراقي (من تصميمج)
def to_iraqi_ultimate(text):
    words_map = {
        "أنا": "أني", "أين": "وين", "الآن": "هسة", "ماذا": "شنو",
        "كيف": "شلون", "جميل": "حلو", "أريد": "أريد", "نحن": "إحنا"
    }
    words = text.split()
    result = [words_map.get(w.strip("؟.!"), w) for w in words]
    return " ".join(result)


# 2. دالة النطق
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# 3. دالة كشف التصفيق
def audio_callback(indata, frames, time_info, status):
    global clap_count, last_clap_time
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > THRESHOLD:
        current_time = time.time()
        if current_time - last_clap_time > 0.4:
            clap_count += 1
            last_clap_time = current_time
            print(f" (تصفيقة {clap_count}!) ", end='', flush=True)


# 4. الدالة الرئيسية (التشغيل)
def start_program():
    global clap_count
    print("--- البرنامج جاهز ---")
    print("1. اكتبي نص واضغطي Enter")
    print("2. أو اضغطي Enter مباشرة للحجي بالمايك")

    user_input = input("النص: ")

    # إذا المستخدم يريد يحجي صوتياً
    if user_input == "":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            speak("تفضلي احجي")
            print("اسمعج هسة...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio, language='ar-SA')
                print(f"قلتي: {user_input}")
            except:
                print("ما سمعت شي")
                return

    # هسة ننتظر التصفيق لاختيار اللغة
    print("\nصفقي هسة لاختيار اللغة: (1:إنجليزي, 2:عراقي, 3:إسباني)")
    clap_count = 0
    with sd.InputStream(callback=audio_callback):
        start_wait = time.time()
        while time.time() - start_wait < 5:  # ننتظر 5 ثواني للتصفيق
            if clap_count > 0 and (time.time() - last_clap_time) > COOLDOWN:
                if clap_count == 1:
                    res = GoogleTranslator(source='auto', target='en').translate(user_input)
                elif clap_count == 2:
                    res = to_iraqi_ultimate(user_input)
                else:
                    res = GoogleTranslator(source='auto', target='es').translate(user_input)

                print(f"\nالنتيجة: {res}")
                speak(res)
                return

            time.sleep(0.1)


if name == "main":
    start_program()
def listen_and_process():
    while True:
        start_program()
