# ============================================================================================================
# Description:  This class integrates with Azure Storage Blob
#
#   01/20/2025 - Natalie Carlson
#                   Created
# ============================================================================================================

# Imports
import azure.storage.blob as asb
from azure.identity import DefaultAzureCredential


class AzureStorageBlob:

    def __init__(self, account_url):

        self.credential = DefaultAzureCredential()
        self.account_url = account_url
        self.container_clients = {}

        self.storage_blob_object_name_id = f"asb_{str(id(self))}"


    def add_container_client(self, container_name, create=False):
        """This method adds a container client used for interacting with the Azure Storage Account
        optionally creates an Azure container if it doesn't exist"""
        
        # Establish client
        container_client = asb.ContainerClient(self.account_url, container_name, self.credential)

        # Add to class
        self.container_clients[container_name] = {
            'client': container_client,
            'blob_clients': {}
        }

        if create:
            self. create_container(container_name)
    
    def create_container(self, container_name):
        """This method creates a new container in the Azure Storage Account"""
        
        # Retrieve client
        container_client = self.container_clients[container_name]['client']
        
        # Determine if container exists
        exists = container_client.exists()
        
        if exists:
            print(f"Container {container_name} already exists.")
        
        else:
            # Create container
            container_client.create_container()
            print(f"Container {container_name} created.")

            
    def add_blob_client(self, container_name, blob_path):
        """This method adds a blob client used for interacting with the Azure Storage Account"""

        # Establish client
        container_client = self.container_clients[container_name]['client']
        blob_client = container_client.get_blob_client(blob_path)
        
        # Add to class
        self.container_clients[container_name]['blob_clients'][blob_path] = blob_client
    
    def create_blob(self, container_name, blob_path, source_file_path):
        """This method creates/uploads a blob if it doesn't already exist"""
        
        # Retrieve client
        container_client = self.container_clients[container_name]['client']
        blob_client = container_client.get_blob_client(blob_path)
        
        # Verify blob exists
        exists = blob_client.exists()
        if exists:
            print(f"Blob {blob_path} already exists.")
        
        else:
            # Create blob
            with open(source_file_path, "rb") as f:
                blob_client.upload_blob(data=f)
            print(f"Blob {blob_path} created.")
    
    def retrieve_blob(self, container_name, blob_path, target_file_path):
        """This method retrieves/downloads a blob if it exists"""

        #  Retrieve client
        container_client = self.container_clients[container_name]['client']
        blob_client = container_client.get_blob_client(blob_path)
        
        # Verify blob exists
        exists = blob_client.exists()
        if exists:
            download_stream = blob_client.download_blob()
            with open(target_file_path, "wb") as f:
                f.write(download_stream.readall())
        else:
            print(f"Blob {blob_path} doesn't exist.")
    
    def close_all_clients(self):
        """This method loops through all the containers in self.container_clients
        It closes each blob client and then the container client"""
        for container_name, container_dict in self.container_clients.items():
            print(f"Closing clients for container {container_name}")
            container_client = container_dict['client']
            for blob_path, blob_client in container_dict['blob_clients'].items():
                print(f"Closing clients for blob {blob_path}")
                blob_client.close()
            container_client.close()

    