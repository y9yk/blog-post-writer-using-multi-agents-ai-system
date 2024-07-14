from .arxiv import ArxivScraper
from .beautiful_soup import BeautifulSoupScraper
from .newspaper import NewspaperScraper
from .pymupdf import PyMuPDFScraper
from .web_base_loader import WebBaseLoaderScraper

__all__ = [
    "ArxivScraper",
    "BeautifulSoupScraper",
    "NewspaperScraper",
    "PyMuPDFScraper",
    "WebBaseLoaderScraper",
]
