import pathlib
import sys

from markdown_html_pdf.tools import markdown_to_html

file_path = pathlib.Path(sys.argv[1])


markdown_to_html(
    markdown_file_path=file_path, html_output_file_path=file_path.with_suffix(".html"), html_output_title=file_path.stem
)
