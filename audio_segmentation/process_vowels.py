import click
import librosa
import pathlib
import textgrid

@click.command(help='Process vowels from audio using fn')
@click.argument('audio_file', metavar='AUDIO_FILE')
@click.argument('tg_file', metavar='TG_FILE')
@click.argument('fn', metavar='FN')
def process_vowels(audio_file, tg_file, fn):
    audio_file = pathlib.Path(audio_file).resolve()
    assert audio_file.is_file() and audio_file.suffix == '.wav'
    tg_file = pathlib.Path(tg_file).resolve()
    assert tg_file.is_file() and tg_file.suffix == '.TextGrid'

    audio, sr = librosa.load(audio_file)
    tg = textgrid.TextGrid()
    tg.read(tg_file)
    phonemes = iter(tg[5].intervals)
    result, length = 0.0, 0.0

    for syllable in tg[2].intervals:
        phoneme = next(phonemes)
        if phoneme.maxTime < syllable.maxTime:
            phoneme = next(phonemes)
        if syllable.mark == 'SP' or syllable.mark == 'AP':
            continue
        audio_segment = audio[phoneme.minTime * sr : phoneme.maxTime * sr]
        result += fn(audio_segment)
        length += phoneme.duration()

    return result / length

if __name__ == '__main__':
    process_vowels()
