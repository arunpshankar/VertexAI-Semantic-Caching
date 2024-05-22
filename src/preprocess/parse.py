from src.config.logging import logger
from src.config.setup import config
from google.cloud import documentai
from pypdf import PdfReader 
from pypdf import PdfWriter
from typing import List 
import os 


docai_client = documentai.DocumentProcessorServiceClient()


def split_pdf(input_path: str, output_dir: str, max_pages_per_document: int = 15) -> None:
    """
    Splits a PDF file into smaller parts each with a maximum of `max_pages_per_document` pages.

    Parameters:
    - input_path (str): Path to the input PDF file.
    - output_dir (str): Directory to save the split PDF files.
    - max_pages_per_document (int, optional): Max pages per split document. Default is 15.
    """
    reader = PdfReader(input_path)
    n = len(reader.pages)
    

    _, file_name = input_file_path.rsplit('/', 1)
    file_name = file_name.replace('.pdf', '')
    output_path = f'{output_dir}/{file_name}/'
    os.makedirs(output_path, exist_ok=True)
    

    for i in range(0, n, max_pages_per_document):
        writer = PdfWriter()
        for j in range(i, min(i + max_pages_per_document, n)):
            writer.add_page(reader.pages[j])
        with open(f'{output_path}/{i+1}-{min(i+max_pages_per_document, n)}.pdf', 'wb') as f:
            writer.write(f)


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.

    Converts layout information from Document AI to a string.

    Parameters:
    - layout (documentai.Document.Page.Layout): The layout information of a document page.
    - text (str): The text of the document.

    Returns:
    - str: Extracted text from the layout.
    """
    extracted_text_segments = []
    
    for segment in layout.text_anchor.text_segments:
        segment_text = text[segment.start_index: segment.end_index]
        extracted_text_segments.append(segment_text)

    return ''.join(extracted_text_segments)


def get_file_paths(dir_name: str) -> List[str]:
    """
    Retrieves file paths from a specified directory.

    Parameters:
    - dir_name (str): Directory name to search for files.

    Returns:
    - List[str]: A list of file paths.
    """
    return [os.path.join(dir_name, file_name) for file_name in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, file_name))]


def ocr_docai(subfolder_path: str) -> dict:
    """
    Performs OCR on a given file using Google Document AI and extracts text.

    Parameters:
    - subfolder_path (str): Path to the subfolder

    Returns:
    - dict: A dictionary mapping page numbers to their extracted text.
    """
    pages_map = {}

    if os.path.isdir(subfolder_path):
        for file in os.listdir(subfolder_path):
            if file.endswith('.pdf'):
                file_path = os.path.join(subfolder_path, file)
            try:
                with open(file_path, 'rb') as f:
                    pdf_content = f.read()

                raw_document = documentai.RawDocument(content=pdf_content, mime_type='application/pdf')
                request = documentai.ProcessRequest(name=config.DOCAI_PROCESSOR_NAME, raw_document=raw_document)
                response = docai_client.process_document(request=request)

                document_text = response.document.text
                file_name = os.path.basename(file_path)
                initial_page_number = int(file_name.split('.')[0].split('-')[-2])

                for page in response.document.pages:
                    page_text = [layout_to_text(paragraph.layout, document_text) for paragraph in page.paragraphs]
                    pages_map[initial_page_number] = ''.join(page_text)
                    initial_page_number += 1

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")

    return pages_map


if __name__ == '__main__':
    input_file_paths = get_file_paths('./data/raw/')
    logger.info('Splitting PDFs')
    for input_file_path in input_file_paths:
        split_pdf(input_file_path, './data/parts/')

    
    # Iterate over each subfolder and then each PDF file in the subfolder
    logger.info('Parse pages')
    for subfolder in os.listdir('./data/parts/'):
        logger.info(subfolder)
        subfolder_path = os.path.join('./data/parts/', subfolder)
        pages_map = ocr_docai(subfolder_path)

        output_dir = f'./data/pages/{subfolder}'
        os.makedirs(output_dir, exist_ok=True)

        # Iterate through the dictionary and write each page to a separate text file
        for page_number, text in pages_map.items():
            file_path = os.path.join(output_dir, f"page_{page_number}.txt")
            with open(file_path, 'w') as file:
                file.write(text)
        break