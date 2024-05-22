 
from src.config.logging import logger
from src.config.setup import config
from google.cloud import documentai
from typing import Sequence
from typing import List 
from typing import Dict
import pandas as pd
import os


# Global constants
DOCAI_PROCESSOR_NAME = 'projects/390991481152/locations/us/processors/44d7292d4313fc58'
OUTPUT_FILE_PREFIX = './data/tables'

# Document AI client
docai_client = documentai.DocumentProcessorServiceClient()


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Converts layout information from Document AI to a string.

    Args:
        layout: The layout information of a document page.
        text: The text of the document.

    Returns:
        Extracted text from the layout.
    """
    return ''.join(text[int(segment.start_index):int(segment.end_index)]
                   for segment in layout.text_anchor.text_segments)


def text_anchor_to_text(text_anchor: documentai.Document.TextAnchor, text: str) -> str:
    """
    Converts text anchor information from Document AI to a string.

    Args:
        text_anchor: Text anchor information.
        text: The text of the document.

    Returns:
        A string representation of the text anchor.
    """
    response = ""
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response.strip().replace("\n", " ")


def get_table_data(rows: Sequence[documentai.Document.Page.Table.TableRow], text: str) -> List[List[str]]:
    """
    Extracts text data from table rows.

    Args:
        rows: The rows of a table.
        text: The text of the document.

    Returns:
        A list of lists containing the cell values.
    """
    return [[text_anchor_to_text(cell.layout.text_anchor, text) for cell in row.cells] for row in rows]


def parse_tables(subfolder_path: str) -> None:
    """
    Performs OCR on PDF files in a given folder using Google Document AI and extracts table data.

    Args:
        subfolder_path: Path to the subfolder containing PDF files.

   
    """

    if not os.path.isdir(subfolder_path):
        logger.error("Invalid subfolder path")

    doc_name = os.path.basename(subfolder_path)

    for file in os.listdir(subfolder_path):
        if not file.endswith('.pdf'):
            continue

        file_path = os.path.join(subfolder_path, file)
        try:
            with open(file_path, 'rb') as f:
                pdf_content = f.read()

            raw_document = documentai.RawDocument(content=pdf_content, mime_type='application/pdf')
            request = documentai.ProcessRequest(name=DOCAI_PROCESSOR_NAME, raw_document=raw_document)
            response = docai_client.process_document(request=request)
            document = response.document

            for page in document.pages:
                page_tables = []

                for index, table in enumerate(page.tables):
                    header_row_values = get_table_data(table.header_rows, document.text)
                    body_row_values = get_table_data(table.body_rows, document.text)

                    df = pd.DataFrame(data=body_row_values, columns=pd.MultiIndex.from_arrays(header_row_values))
                    page_tables.append(df)

                    markdown = df.to_markdown()
                    output_path = f'{OUTPUT_FILE_PREFIX}/{doc_name}'
                    os.makedirs(output_path, exist_ok=True)
                    output_filename = f"{output_path}/page_{page.page_number}_table_{index+1}.txt"
                    with open(output_filename, 'w') as out:
                        out.write(markdown)

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

    
if __name__ == '__main__':
    for subfolder in os.listdir('./data/parts/'):
        logger.info(f"Processing subfolder: {subfolder}")
        subfolder_path = os.path.join('./data/parts/', subfolder)
        parse_tables(subfolder_path)
