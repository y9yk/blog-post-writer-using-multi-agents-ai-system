from fastapi import WebSocket

from blog_poster.processor import Processor


class BlogPosterService(object):
    async def process(
        self,
        query: str,
        verbose: bool = False,
        websocket: WebSocket = None,
    ):
        # create processor
        processor = Processor(
            query=query,
            verbose=verbose,
            websocket=websocket,
        )

        # create report_body
        report_body: str = await processor.run()
        return report_body
