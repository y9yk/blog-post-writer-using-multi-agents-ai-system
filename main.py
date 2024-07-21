import asyncio

import click

from blog_poster.processor import Processor


@click.command()
@click.option("--query", required=True, type=click.STRING)
@click.option(
    "--verbose",
    required=False,
    type=click.BOOL,
    default=False,
)
def execute(query: str, verbose: bool):
    # create event loop
    loop = asyncio.get_event_loop()

    processor = Processor(query=query, verbose=verbose)
    loop.run_until_complete(processor.run())

    # close event loop
    loop.close()


if __name__ == "__main__":
    execute()
