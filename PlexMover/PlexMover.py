# /usr/bin/env python3

from __future__ import print_function

import click
import platform

os_name = platform.system()


@click.group()
@click.pass_context
def cli(ctx):
    if os_name == 'Darwin':
        from PlexMover.oslibs.darwin import Darwin
        ctx.obj = Darwin()
    else:
        ctx.fail('%s is not supported' % os_name)


@cli.command('import')
@click.argument('file', type=click.Path(exists=True, dir_okay=False, allow_dash=True))
@click.pass_context
def importSettings(ctx, file):
    ctx.obj.importSettings(file)


@cli.command('export')
@click.argument('file', type=click.Path(writable=True, dir_okay=False, allow_dash=True))
@click.pass_context
def exportSettings(ctx, file):
    print(ctx.obj.exportSettings(file))


if __name__ == '__main__':
    cli()
