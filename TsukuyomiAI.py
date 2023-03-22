import openai
import speech_recognition as sr
import json
import requests
from pydub import AudioSegment, playback

openai.api_key = "chatGPTのAPIキー"

def completion(new_message_text:str, settings_text:str = '', past_messages:list = []):
    if len(past_messages) == 0 and len(settings_text) != 0:
        system = {"role": "system", "content": settings_text}
        past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    past_messages.append(new_message)

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=past_messages
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, past_messages

with open("chat_history.txt", mode = "r", encoding="utf_8") as f:
    history = f.read()

character_settings = "あなたはツクヨミというキャラクターです。カジュアル口調で会話して"

history_settings = f"""また、ツクヨミは過去に以下のようなやり取りを行っています
{history}
"""

system_settings = character_settings + history_settings + "ではシミュレーションを開始します。"

abbreviation_settings = """会話の内容を簡潔にまとめてください。
"""

def chatInit():
    cnt = 0
    while True:
            try:
                if cnt == 0:
                    # マイクから音声を取得
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        print("話しかけてください...")
                        audio = r.listen(source)

                    # 音声をテキストに変換
                    try:
                        user_text = r.recognize_google(audio, language='ja-JP')
                        print("テキスト：" + user_text)
                    except sr.UnknownValueError:
                        print("音声が認識できませんでした。")
                        raise ValueError('例外が発生')
                    except sr.RequestError as e:
                        print("音声認識APIへのリクエストが失敗しました。 {0}".format(e))
                        raise ValueError('例外が発生')
                    
                    new_message, messages = completion(user_text, system_settings, [])
                    # パラメータ
                    text = new_message  # セリフ
                    speaker_id = 0  # スピーカーID (０：つくよみちゃん)

                    # 音声合成のクエリの作成
                    response = requests.post(
                        "http://localhost:50031/audio_query",
                        params={
                            'text': text,
                            'speaker': speaker_id,
                            'core_version': '0.0.0'
                        })
                    query = response.json()

                    # 音声合成のwavの生成
                    response = requests.post(
                        'http://localhost:50031/synthesis',
                        params={
                            'speaker': speaker_id,
                            'core_version': "0.0.0",
                            'enable_interrogative_upspeak': 'true'
                        },
                        data=json.dumps(query))

                    # wavの音声を再生
                    playback.play(AudioSegment(response.content,
                        sample_width=2, frame_rate=44100, channels=1))
                    cnt += 1
                else:
                    # マイクから音声を取得
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        print("話しかけてください...")
                        audio = r.listen(source)

                    # 音声をテキストに変換
                    try:
                        user_text = r.recognize_google(audio, language='ja-JP')
                        print("テキスト: " + user_text)
                    except sr.UnknownValueError:
                        print("音声が認識できませんでした。")
                        raise ValueError('例外が発生')
                    except sr.RequestError as e:
                        print("音声認識APIへのリクエストが失敗しました。 {0}".format(e))
                        raise ValueError('例外が発生')
                    
                    new_message, messages = completion(user_text, system_settings, messages)
                    print("AI: ", new_message)
                    # パラメータ
                    text = new_message  # セリフ
                    speaker_id = 0  # スピーカーID (０：つくよみちゃん)

                    # 音声合成のクエリの作成
                    response = requests.post(
                        "http://localhost:50031/audio_query",
                        params={
                            'text': text,
                            'speaker': speaker_id,
                            'core_version': '0.0.0'
                        })
                    query = response.json()

                    # 音声合成のwavの生成
                    response = requests.post(
                        'http://localhost:50031/synthesis',
                        params={
                            'speaker': speaker_id,
                            'core_version': "0.0.0",
                            'enable_interrogative_upspeak': 'true'
                        },
                        data=json.dumps(query))

                    # wavの音声を再生
                    playback.play(AudioSegment(response.content,
                        sample_width=2, frame_rate=44100, channels=1))
            except:
                print("Ending Conversation...")
                chat_history, _ = completion(str(messages), abbreviation_settings, [])
                with open("chat_history.txt", mode = "w", encoding="utf_8") as f:
                    f.write(chat_history)
                break

if __name__ == "__main__": 
    chatInit()