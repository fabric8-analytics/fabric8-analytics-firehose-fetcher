#!/usr/bin/env python3

import click

from f8a_firehose_fetcher.firehose_fetcher import run_liveness, FirehoseFetcher


@click.command()
@click.option('--liveness', is_flag=True, help="Starts liveness probe")
def cli(liveness):
    """This scripts starts firehose fetcher service or it's liveness probe"""
    if liveness:
        run_liveness()
    else:
        fetcher = FirehoseFetcher()
        fetcher.run()
