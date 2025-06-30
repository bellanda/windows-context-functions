import asyncio
import pathlib
import sys

from markdown_html_pdf.tools import markdown_to_pdf

file_path = pathlib.Path(sys.argv[1])


async def convert():
    await markdown_to_pdf(markdown_file_path=file_path, pdf_output_file_path=file_path.with_suffix(".pdf"))


asyncio.run(convert())
