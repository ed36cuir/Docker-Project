import os, uuid, shutil
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

print("Azure Blob storage v" + __version__ + " - Python quickstart sample")
# Quick start code goes here
# Retrieve the connection string for use with the application. The storage
# connection string is stored in an environment variable on the machine
# running the application called AZURE_STORAGE_CONNECTION_STRING. If the environment variable is
# created after the application is launched in a console or with Visual Studio,
# the shell or application needs to be closed and reloaded to take the
# environment variable into account.
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Create the BlobServiceClient object which will be used to list the container
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def use_container_function():
    # name of container
    print("1. Create new container")
    print("2. Use existing container")
    use_container = input()

    if(use_container == "1"):
        print("Create container name")
        container_name = input()
        # Create the container
        container_client = blob_service_client.create_container(container_name)
        return container_client, container_name
    elif(use_container == "2"):
        print("Container name:")
        container_name = input()
        # Get existing container
        container_client = blob_service_client.get_container_client(container_name)
        return container_client, container_name
    else:
        print("Choose correctly")
        print("1. Create new container")
        print("2. Use existing container")
        use_container = input()
        use_container_function()

container_client, container_name = use_container_function()

print(container_name)

## Uploading blobs to the container
# Create a file in local data directory to upload and download
local_path = "./data"
isdir = os.path.isdir(local_path)
if(isdir == False):
    os.mkdir(local_path)
local_file_name = "quickstart" + str(uuid.uuid4()) + ".txt"
upload_file_path = os.path.join(local_path, local_file_name)

# Write text to the file
file = open(upload_file_path, 'w')
file.write("Hello, World!")
file.close()

# Create a blob client using the local file name as the name for the blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

# Upload the created file
with open(upload_file_path, "rb") as data:
   blob_client.upload_blob(data)

print("\nListing blobs....")

# Listing blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

# Download the blob to a local file
# Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
download_file_path = os.path.join(local_path, str.replace(local_file_name, 'txt', 'DOWNLOAD.TXT'))
print("\Downloading blob to \n\t" + download_file_path)

with open(download_file_path, 'wb') as download_file:
    download_file.write(blob_client.download_blob().readall())

# Choose if you want to delete container
print("Do you want to delete the container?(yes/no)")
container_opt = input()
def delete_container_function(container_opt):
    if(container_opt == "yes"):
        # Delete container
        print("\nPress the Enter key to begin clean up")
        input()

        print("Deleting container...")
        container_client.delete_container()

        print("Deleting the local files and downloaded files")
        os.remove(upload_file_path)
        os.remove(download_file_path)
        shutil.rmtree(local_path)
        return "Done"
    elif(container_opt == "no"):
        return "Done"
    else:
        print("Choose correctly(yes/no)")
        container_opt2 = input()
        delete_container_function(container_opt2)

delete_container_function(container_opt)
