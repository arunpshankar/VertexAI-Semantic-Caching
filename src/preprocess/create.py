from google.api_core.client_options import ClientOptions
from src.config.logging import logger
from src.config.setup import config
from google.cloud import documentai


def create_document_processor(name: str):
    """
    Creates a Document AI processor client and a new OCR processor.
    The processor name is taken from the configuration and error handling is added.
    """

    try:
        # Configure client options with the API endpoint
        client_options = ClientOptions(api_endpoint=f"us-documentai.googleapis.com")

        # Initialize the Document AI client
        client = documentai.DocumentProcessorServiceClient(client_options=client_options)

        # Get the common location path
        parent = client.common_location_path(config.PROJECT_ID, 'us')

        # Create a Document AI processor 
        docai_processor = client.create_processor(
            parent=parent,
            processor=documentai.Processor(
                display_name=name,
                type_='OCR_PROCESSOR'
            )
        )

        # Log the creation of the processor
        logger.info(f"Document AI Processor Created: {docai_processor}")

    except Exception as e:
        # Log any errors that occur during processor creation
        logger.error(f"Error creating Document AI Processor: {e}")

# Usage
create_document_processor('docai-processor')