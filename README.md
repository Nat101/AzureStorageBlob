# AzureStorageBlob

A demo program of the Azure Storage Blob 

Project dependencies are managed via Pipenv.  See https://pipenv.pypa.io for more information or troubleshooting.ex


# Installation Notes
You need to have an Azure subscription and an Azure storage account.  See https://azure.microsoft.com/en-us/products/storage/blobs/

  
# Credentials
To integrate with your Azure account, you will need credentials.  
It is reccomended to use azure.identity.DefaultAzureCredential, a default credential capable of handling most Azure SDK authentication scenarios. The identity it uses depends on the environment. When an access token is needed, it requests one using these identities in turn, stopping when one provides a token:
    EnvironmentCredential
    ManagedIdentityCredential
    SharedTokenCacheCredential
    AzureCliCredential
    AzurePowerShellCredential
    AzureDeveloperCliCredential

For this program I am using the AzureCliCredential.  See https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli
To install via docker see https://learn.microsoft.com/en-us/cli/azure/run-azure-cli-docker
    docker run -d --name azure-cli -v ${HOME}/.ssh:/root/.ssh mcr.microsoft.com/azure-cli:cbl-mariner2.0

# Role Assignment
To integrate with you Azure Storage, you will need role permissions.  Note this is in addition to being an account "owner".  
See https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal
For this program I assigned the role "Storage Blob Data Owner"
