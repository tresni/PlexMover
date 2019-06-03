# /usr/bin/env python3

import json
import os.path
import platform
import shutil
import zipfile

import xml.etree.ElementTree as ET

import click
import requests

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


def _is_zip(ctx, param, value):
    if not os.path.splitext(value)[1] == '.zip':
        raise click.BadParameter('must end in .zip')
    return value


@cli.command('export')
@click.argument('file', type=click.Path(writable=True, dir_okay=False,
                                        allow_dash=True),
                callback=_is_zip)
@click.option('-d', '--data-dir', 'datadir',
              type=click.Path(exists=True, file_okay=False))
@click.option('-s', '--server', default='localhost')
@click.option('-p', '--port', type=int, default=32400)
@click.option('-e', '--secure/--no-secure', default=False)
@click.pass_context
def exportSettings(ctx, file, datadir, secure, port, server):
    url = '%s://%s:%s/:/prefs' % ('https' if secure else 'http', server, port)
    with requests.get(url) as resp:
        tree = ET.fromstring(resp.text)

    trash = tree.find('.//Setting[@id=\'autoEmptyTrash\']')
    if trash.attrib['value'] == '0':
        click.echo('"Empty trash automatically after every scan" is disabled')
    else:
        click.echo('Disabling "Empty trash automatically after every scan"')
        resp = requests.put("%s?autoEmptyTrash=0" % url)
        if resp.status_code != 200:
            ctx.fail('Unable to disable '
                     '"Empty trash automatically after every scan"\n'
                     'Please do that through the server settings before '
                     'proceeding.')

    if os.path.exists(file):
        if not click.confirm('We will remove "%s", do you want to continue?'
                             % file):
            ctx.exit(1)
        os.remove(file)

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
