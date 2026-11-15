
import os
import logging

from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

logger = logging.getLogger(__name__)


class AzureBlobManager:
    """
    A manager class to handle read/write operations
    for Azure Blob Storage using a connection string.
    """

    def __init__(
        self,
        account_url=None,
        tenant_id=None,
        client_id=None,
        username=None,
        password=None
    ):
        """
        Initializes Azure Blob Storage using connection string.
        """

        self.account_url = account_url
        self.blob_service_client = None

        logger.info("Connecting to Azure Blob Storage...")

        try:
            connection_string = os.getenv(
                "AZURE_STORAGE_CONNECTION_STRING"
            )

            if not connection_string:
                raise ValueError(
                    "AZURE_STORAGE_CONNECTION_STRING is missing in .env"
                )

            self.blob_service_client = (
                BlobServiceClient.from_connection_string(
                    connection_string
                )
            )

            logger.info(
                "Azure Blob Storage connected successfully."
            )

        except Exception as e:
            logger.error(f"Azure connection failed: {e}")
            raise

    def upload_test_case(
        self,
        container_name,
        db_problem_id,
        test_number,
        input_data,
        output_data
    ):
        """
        Uploads input and output test cases as separate blobs.
        """

        input_blob_name = (
            f"test_cases/{db_problem_id}/{test_number:02d}"
        )

        output_blob_name = (
            f"test_cases/{db_problem_id}/{test_number:02d}.a"
        )

        try:
            input_blob_client = (
                self.blob_service_client.get_blob_client(
                    container=container_name,
                    blob=input_blob_name
                )
            )

            input_blob_client.upload_blob(
                input_data.encode("utf-8"),
                overwrite=True
            )

            logger.info(
                f"Uploaded input for test #{test_number}"
            )

            output_blob_client = (
                self.blob_service_client.get_blob_client(
                    container=container_name,
                    blob=output_blob_name
                )
            )

            output_blob_client.upload_blob(
                output_data.encode("utf-8"),
                overwrite=True
            )

            logger.info(
                f"Uploaded output for test #{test_number}"
            )

        except Exception as e:
            logger.error(
                f"Error uploading test case #{test_number}: {e}"
            )
            raise

    def empty_blob(self, container_name, problem_id):
        """
        Deletes all blobs for a given problem ID.
        """

        prefix = f"test_cases/{problem_id}/"

        try:
            container_client = (
                self.blob_service_client.get_container_client(
                    container_name
                )
            )

            blobs_to_delete = [
                blob.name
                for blob in container_client.list_blobs(
                    name_starts_with=prefix
                )
            ]

            for blob_name in blobs_to_delete:
                logger.info(f"Deleting blob: {blob_name}")
                container_client.delete_blob(blob_name)

            logger.info(
                f"Deleted {len(blobs_to_delete)} blobs "
                f"for problem {problem_id}"
            )

        except ResourceNotFoundError:
            logger.warning(
                f"Container or blobs not found for problem {problem_id}"
            )

        except Exception as e:
            logger.error(
                f"Error deleting blobs for problem {problem_id}: {e}"
            )
            raise
    def download_test_case(self, container_name, db_problem_id, test_number):
        input_blob_name = f"test_cases/{db_problem_id}/{test_number:02d}"
        output_blob_name = f"test_cases/{db_problem_id}/{test_number:02d}.a"

        input_client = self.blob_service_client.get_blob_client(
        container=container_name,
        blob=input_blob_name
        )

        output_client = self.blob_service_client.get_blob_client(
        container=container_name,
        blob=output_blob_name
        )

        input_data = input_client.download_blob().readall().decode("utf-8")
        output_data = output_client.download_blob().readall().decode("utf-8")

        return input_data, output_data
    
    def verify_test_cases(self, container_name, db_problem_id):
        container_client = self.blob_service_client.get_container_client(
        container_name
       )

        prefix = f"test_cases/{db_problem_id}/"

        blobs = {
           blob.name
           for blob in container_client.list_blobs(name_starts_with=prefix)
        }

        results = []

        for number in range(1, 22):
            input_name = f"{prefix}{number:02d}"
            output_name = f"{prefix}{number:02d}.a"

            results.append({
                "test_case": number,
                "input_exists": input_name in blobs,
                "output_exists": output_name in blobs,
                "complete": input_name in blobs and output_name in blobs
           })

        return results

