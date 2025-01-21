# =================================================================================================
# Description: This module contains a set of demos for interacting with Azure Storage Blob
#
#   01/20/2025 - Natalie Carlson
#                   Created
# =================================================================================================

import os
from azure_storage_blob import AzureStorageBlob
from helper_functions import refactor_path


def main():

    # ==============================================
    # Variables
    #================================================

    # Create AzureStorageBlob instance
    account_name = 'nat101demos' # TODO replace with your account name
    account_url = f'https://{account_name}.blob.core.windows.net/'  
    az_sb = AzureStorageBlob(account_url)

    # File Pathways
    source_file_name = 'whiskers.txt'
    source_file_path = refactor_path(f"{os.getcwd()}/Data_Sets/{source_file_name}")

    target_file_name = 'whiskers_downloaded.txt'
    target_file_path = refactor_path(f"{os.getcwd()}/Data_Sets/{target_file_name}")

    # Azure Integration
    container_name = 'animals'
    blob_prefix = 'pets/cats'  # a blob_prefix allows you to organize your blobs into sub groups for easier searching
    blob_name = 'whiskers'
    blob_path = f"{blob_prefix}/{blob_name}"
    # Add container client
    az_sb.add_container_client(container_name, create=True)
    container_client = az_sb.container_clients.get(container_name,{}).get('client')
    # Add blob client
    az_sb.add_blob_client(container_name, blob_path)
    blob_client = az_sb.container_clients[container_name]['blob_clients'][blob_path]
    

    # ================================================================
    #  Demos
    # ================================================================
    
    # Retrieve container metadata 
    try:
        print(f"\nContainer Client:") 
        print(f"\tAccount Name: {container_client.account_name}")
        print(f"\tContainer Name: {container_client.container_name}")
        print(f"\tAPI Version: {container_client.api_version}")
    except Exception as e:
        print(f"\tError: {str(e)}")

    # List all blobs in container
    try:
        print(f"\nBlobs in container {container_name}:")
        results = container_client.list_blob_names()
        for result in results:
            print(f"\t{result}")
    except Exception as e:
        print(f"\tError: {str(e)}")

    # List all blobs in container with blob_prefix
    try:
        print(f"\nBlobs in container {container_name} blob_prefix {blob_prefix}:")
        results = container_client.list_blob_names(name_starts_with=blob_prefix)
        for result in results:
            print(f"\t{result}")
    except Exception as e:
        print(f"\tError: {str(e)}")

    # List all properties of blobs in container with blob_prefix
    try:
        print(f"\nBlob properties in container {container_name} blob_prefix {blob_prefix}:")
        results = container_client.list_blobs(name_starts_with=blob_prefix)
        for result in results:
            for k, v in result.items():
                if k == 'name':
                    print(f"\t{k}: {v}")
                else:
                    print(f"\t\t{k}: {v}")
    except Exception as e:
        print(f"\tError: {str(e)}")
    
    # List all properties of blob
    try:
        print(f"\nBlob properties of {blob_path}:")
        results = blob_client.get_blob_properties()
        for k, v in results.items():
            if k == 'name':
                print(f"\t{k}: {v}")
            else:
                print(f"\t\t{k}: {v}")
    except Exception as e:
       print(f"\tError: {str(e)}")

    # Download a blob from a container
    try:
        print("\nDownload blob.")
        # Retrieves the results from the given blob and writes it to the target file.
        az_sb.retrieve_blob(container_name, blob_path, target_file_path)
    except Exception as e:
        print(f"\tError: {str(e)}")

    # Create a new blob in a container
    try:
        print(f"\nUpload blob {blob_path}:")
        az_sb.create_blob(container_name, blob_path, source_file_path)
    except Exception as e:
       print(f"\tError: {str(e)}")



    # Close all clients
    az_sb.close_all_clients()


if __name__ == '__main__':
    main()