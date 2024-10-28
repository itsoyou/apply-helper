from apply_helper.config import Config, logger


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENTIONS
    )


def upload_pdf_to_vector_store(client, assistant_id, file_path):
    try:
        file_data = client.files.create(
            file=open(file_path, "rb"), purpose="assistants"
        )
        logger.debug("File uploaded with ID: %s", file_data.id)

        vector_store = client.beta.vector_stores.create(
            name="Document Vector Store"
        )
        vector_store_id = vector_store.id
        logger.debug("Vector store created with ID: %s", vector_store_id)

        vector_store_response = client.beta.vector_stores.files.create(
            vector_store_id=vector_store.id, file_id=file_data.id
        )
        logger.debug("File added to vector store: %s", vector_store_response)

        client.beta.assistants.update(
            assistant_id,
            tool_resources={
                "file_search": {"vector_store_ids": [vector_store_id]}
            },
        )
        logger.debug(
            "Assistant updated with Vector Store ID: %s", vector_store_id
        )
        return vector_store_id

    except Exception as e:
        logger.error("Error uploading file or creating vector store: %s", e)
        return None
