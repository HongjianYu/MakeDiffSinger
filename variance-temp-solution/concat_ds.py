import click
import json
import pathlib
import textgrid

@click.command(help='Concatenate sengmented DS files')
@click.argument('ds_dir', metavar='DS_DIR')
@click.argument('tg_file', metavar='TG_FILE')
def ds(ds_dir, tg_file):
    ds_dir = pathlib.Path(ds_dir).resolve()
    assert ds_dir.exists(), 'The directory of DS files does not exist.'
    tg_file = pathlib.Path(tg_file).resolve()
    assert tg_file.is_file() and tg_file.suffix == '.TextGrid'
    id = tg_file.stem

    ds_files = sorted(ds_dir.glob(f'{id}*.ds'))
    tg = textgrid.TextGrid()
    tg.read(tg_file)
    offsets = [interval.minTime for interval in tg[0].intervals if interval.mark != 'silence']
    offset0 = offsets[0]
    offsets = [offset - offset0 for offset in offsets]

    assert len(ds_files) == len(offsets)
    params = []

    for ds_file, offset in zip(ds_files, offsets):
        with open(ds_file, 'r', encoding='utf8') as f:
            param = json.load(f)
        if not isinstance(param, list):
            param = [param]
        assert len(param) == 1
        param[0]["offset"] = offset
        params.append(param[0])

    with open(ds_dir.parent.absolute() / f'{int(id)}.ds', 'w', encoding='utf8') as f:
        json.dump(params, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    ds()
