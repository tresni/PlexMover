# /usr/bin/env python3

import json
import os.path
import shutil
import zipfile

import click
import platform

SETTINGS_FILE = 'PlexMover.settings.json'


@click.group()
@click.pass_context
def cli(ctx):
    os_name = platform.system()
    if os_name == 'Darwin':
        from PlexMover.oslibs.darwin import Darwin
        ctx.obj = Darwin
    elif os_name == 'Windows':
        from PlexMover.oslibs.windows import Windows
        ctx.obj = Windows
    else:
        ctx.fail('%s is not supported' % os_name)


@cli.command('import')
@click.argument('file', type=click.Path(exists=True, dir_okay=False,
                                        allow_dash=True))
@click.option('-d', '--data-dir', 'datadir',
                type=click.Path(file_okay=False))
@click.pass_context
def importSettings(ctx, file, datadir):
    if datadir is None:
        datadir = ctx.obj.getDataPath()
    try:
        shutil.unpack_archive(file, extract_dir=datadir)
        settingPath = os.path.join(datadir, SETTINGS_FILE)
        with open(settingPath, 'r') as fp:
            settings = json.load(fp)
            ctx.obj.importSettings(settings)
        os.remove(settingPath)
    except ValueError as e:
        ctx.echo('Unable to unpack %s' % file)
        ctx.fail(e)


@cli.command('export')
@click.argument('file', type=click.Path(writable=True, dir_okay=False,
                                        allow_dash=True))
@click.option('-d', '--data-dir', 'datadir',
                type=click.Path(exists=True, file_okay=False))
@click.pass_context
def exportSettings(ctx, file, datadir):
    settings = ctx.obj.exportSettings()
    if datadir is None:
        datadir = ctx.obj.getDataPath()

    if not os.path.isdir(datadir):
        ctx.fail('"%s" does not exist and can\'t be backed up.' % datadir)

    clean = os.path.splitext(file)[0]
    shutil.make_archive(clean, 'zip', datadir)
    with zipfile.ZipFile(file, mode='a',
                         compression=zipfile.ZIP_DEFLATED) as zip:
        zip.writestr(SETTINGS_FILE, json.dumps(settings))


if __name__ == '__main__':
    cli()
