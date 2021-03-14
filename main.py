"""テキストまたはssmlの入力文字列から音声を合成します。
注：SSMLはhttps://www.w3.org/TR/speech-synthesis/に応じて適切に形成されなければなりません
"""
from playsound import playsound
import pyperclip


def main():
    clip_str = ""
    while True:
        # クリップボードから文字列を取得する
        if type(pyperclip.paste()) is str:
            if clip_str != pyperclip.paste():
                clip_str = pyperclip.paste()
                PlayAudioData(clip_str)


def PlayAudioData(clip_str):
    """テキストの入力文字列から音声を合成する"""
    from google.cloud import texttospeech
    import os
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=clip_str)

    # 注：音声は名前で指定することもできます。
    # ボイスの名前はclient.list_voices（）で取得できます。
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name="ja-JP-Wavenet-C",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    os.remove("output.mp3")
    # 応答のaudio_contentはバイナリデータ
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('オーディオコンテンツはファイルoutput.mp3へ書き出されました。')
    # 出力されたmp3ファイルを再生する
    playsound("output.mp3")


if main() == __import__:
    main()
