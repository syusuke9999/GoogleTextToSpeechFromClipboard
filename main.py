"""テキストまたはssmlの入力文字列から音声を合成します。
注：SSMLはhttps://www.w3.org/TR/speech-synthesis/に応じて適切に形成されなければなりません
"""
from playsound import playsound
import pyperclip


def main():
    import os
    clip_str = ""
    while True:
        # クリップボードから文字列を取得する
        if type(pyperclip.paste()) is str:
            if clip_str != pyperclip.paste():
                clip_str = pyperclip.paste()
                ssml_text = text_to_ssml(clip_str)
                print(ssml_text)
                if os.path.isfile("output.mp3"):
                    os.remove("output.mp3")
                PlayAudioData(ssml_text)


# noinspection PyCallingNonCallable
def text_to_ssml(ssml_str):
    # プレーンテキスト入力に基づくSSMLテキストの文字列
    # プレーンテキストからSSMLテキストを生成します。
    # 入力ファイル名を指定すると、この関数はテキストファイルの内容をフォーマットされたSSMLテキストの文字列に変換します。
    # この関数は、SSML文字列をフォーマットして、合成時に、合成オーディオがテキストファイルの各行の間で2秒間一時停止するようにします。
    # プレーンテキストをSSMLに変換する
    # 各アドレスの間に2秒待ちます
    import re
    str_ssml = "<speak>" + ssml_str + "</ssml_str>"
    str_ssml = re.sub("\{1}ぶんの\{0}件", '\\{1}' + '\\/' + '\\{0}件', str_ssml)
    str_ssml = re.sub("\{2}ぶんの\{3}件", "分類\\{2}：\\{3}件",str_ssml)
    replace_ssml = str_ssml.replace("万人当たり", "まんにんあたり")
    replace_ssml = replace_ssml.replace('（', '<break time="2s"/>')
    replace_ssml = replace_ssml.replace('）', '<break time="2s"/>')
    replace_ssml = replace_ssml.replace('(', '<break time="2s"/>')
    replace_ssml = replace_ssml.replace(')', '<break time="2s"/>')
    replace_ssml = replace_ssml.replace('。', '。\n<break time="2s"/>')
    replace_ssml = replace_ssml.replace('\n\n', '\n<break time="1s"/>')
    replace_ssml = replace_ssml.replace('\n', '\n<break time="2s"/>')
    replace_ssml = replace_ssml.replace('\n', '\n<break time="2s"/>')
    replace_ssml = replace_ssml.replace('〜', 'から')

    replace_ssml = replace_ssml.replace('討部会', 'とうぶかい')
    # SSMLスクリプトの連結された文字列を返します
    return replace_ssml


def PlayAudioData(clip_str):
    """ssmlの入力文字列から音声を合成します。
    注：ssmlは、次のように整形式である必要があります。
        https://www.w3.org/TR/speech-synthesis/
    Example: <speak>こんにちは。</speak>
    """
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(ssml=clip_str)

    # 注：音声は名前で指定することもできます。
    # ボイスの名前はclient.list_voices（）で取得できます。
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name="ja-JP-Wavenet-C",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    AudioConfig = {"audio_encoding": texttospeech.AudioEncoding.MP3, "speaking_rate": 1.00,"pitch": 0}

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": AudioConfig}
    )
    # 応答のaudio_contentはバイナリデータです。
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('オーディオコンテンツはファイルoutput.mp3へ書き出されました。')
    # 出力されたmp3ファイルを再生する
    playsound("output.mp3")


if main() == __import__:
    main()
