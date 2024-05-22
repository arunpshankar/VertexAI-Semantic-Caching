from src.config.logging import logger
from typing import Generator
from typing import Tuple
import os


# given
def merge_markdown_tables_into_text(page_content: str, tables: str) -> str:
    merged_content = []
    merged_content.append('=== START PAGE CONTENT ===')
    merged_content.append(page_content)
    merged_content.append('=== END PAGE CONTENT ===')
    merged_content.append(tables)
    return '\n'.join(merged_content)


def get_directory_details(base_dir: str) -> Generator[Tuple[str, str, str, str], None, None]:
    """
    Recursively iterates through a given base directory.

    This generator walks through each file in the base directory and its subdirectories,
    and for each file, it yields a tuple containing:
    - Base directory name
    - Subdirectory path relative to the base directory
    - File name
    - Full file path

    Parameters:
    base_dir (str): The base directory to start the file search.

    Yields:
    Generator[Tuple[str, str, str, str]: A generator of tuples, each containing details of a file.
    """
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)
            # Yield the base directory, subdirectory, file name, and file path
            yield base_dir, os.path.relpath(root, base_dir), file, file_path


if __name__ == '__main__':
    # Define the directories for pages and tables
    pages_dir = "./data/pages/"
    tables_dir = "./data/tables/"

    # Ensure the output directory exists
    output_base_dir = "./data/merged"
    

    for _, page_doc_name, page_name, page_path in get_directory_details(pages_dir):
        if page_path.endswith(".txt"):
            logger.info(page_path)
            with open(page_path, 'r') as page:
                page_content = page.read()
        
            # Find and read the corresponding table files
            page_number = page_name.split('_')[1].split('.')[0]
            tables_markdown_list = []
            for _, table_doc_name, table_name, table_path in get_directory_details(tables_dir):
                if table_name.startswith(f'page_{page_number}_') and table_doc_name == page_doc_name:
                    with open(table_path, 'r') as file:
                        table_content = file.read()
                        tables_markdown_list.append('=== TABLE START ===')
                        tables_markdown_list.append(table_content)
                        tables_markdown_list.append('=== TABLE END ===')
            table_content = '\n'.join(tables_markdown_list)
            merged_content = merge_markdown_tables_into_text(page_content, table_content)
            
            

        output_dir = f'{output_base_dir}/{page_doc_name}'
        os.makedirs(output_dir, exist_ok=True)
        output_path = f'{output_dir}/{page_name}'
        with open(output_path, 'w+') as out:
            out.write(merged_content)