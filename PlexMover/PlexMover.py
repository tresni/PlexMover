# /usr/bin/env python3

import json
import os.path
import shutil
import zipfile

import click
import platform


@click.group()
@click.pass_context
def cli(ctx):
    os_name = platform.system()
    if os_name == 'Darwin':
        from PlexMover.oslibs.darwin import Darwin
        ctx.obj = Darwin()
    elif os_name == 'Windows':
        from PlexMover.oslibs.windows import Windows
        ctx.obj = Windows()
    else:
        ctx.fail('%s is not supported' % os_name)


@cli.command('import')
@click.argument('file', type=click.Path(exists=True, dir_okay=False,
                                        allow_dash=True))
@click.pass_context
def importSettings(ctx, file):
    dataPath = ctx.obj.getDataPath()
    try:
        shutil.unpack_archive(file, extract_dir=dataPath)
        ctx.obj.importSettings(os.path.join(dataPath,
                                            'PlexMover.settings.json'))
    except ValueError as e:
        ctx.echo('Unable to unpack %s' % file)
        ctx.fail(e)


@cli.command('export')
@click.argument('file', type=click.Path(writable=True, dir_okay=False,
                                        allow_dash=True))
@click.pass_context
def exportSettings(ctx, file):
    settings = ctx.obj.exportSettings(file)

    dataPath = ctx.obj.getDataPath()

    if not os.path.isdir(dataPath):
        ctx.fail('"%s" does not exist and can\'t be backed up.' % dataPath)

    clean = os.path.splitext(file)[0]
    shutil.make_archive(clean, 'zip', dataPath)
    with zipfile.ZipFile(file, mode='a',
                         compression=zipfile.ZIP_DEFLATED) as zip:
        zip.writestr('PlexMover.settings.json', json.dumps(settings))


if __name__ == '__main__':
    cli()
