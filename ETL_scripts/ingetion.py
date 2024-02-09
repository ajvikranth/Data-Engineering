from hdfs import InsecureClient
import os,json

def upload_folder_to_hdfs(client, local_folder_path, hdfs_folder_path, block_size):
    # Create the HDFS directory if it doesn't exist
    if not client.status(hdfs_folder_path, strict=False):
        client.makedirs(hdfs_folder_path)

    # Upload files from the local folder to HDFS
    for root,dir, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            hdfs_file_path = os.path.join(hdfs_folder_path, file)
            with open(local_file_path, 'rb') as f:
                client.write(hdfs_file_path, local_file_path, blocksize=block_size)

def upload_json(client,local_file,hdfs_file, block_size):
    f = open(local_file,encoding='utf-8')
    animes = json.load(f)   
    from json import dumps
    client.write(hdfs_file, dumps(animes),blocksize=block_size)

def upload_csv(client,local_file,hdfs_file):
    with open(local_file) as reader, client.write(hdfs_file) as writer:
        for line in reader:
            writer.write(line)


if __name__ == "__main__":
    # Initialize HDFS client
    hdfs_client = InsecureClient('http://localhost:9870', user='aj')

    # Set local and HDFS folder paths
    local_folder_path = 'data/images'
    hdfs_folder_path = '/user/aj'
    json_file ="data/MAL.json"
    json_hdfs_file ="/user/aj/MAL.json"
    csv_file ="data/ADB.csv"
    csv_hdfs_file ="/user/aj/ADB.csv"

    # Specify custom block size in bytes
    img_block_size = 1 * 1024 * 1024  # 1 MB
    file_bloak_size = 5 * 1024 * 1024 #5 MB


    upload_json(hdfs_client,json_file,json_hdfs_file,file_bloak_size)
    upload_csv(hdfs_client,csv_file,csv_hdfs_file,file_bloak_size)

    # Upload folder to HDFS
    upload_folder_to_hdfs(hdfs_client, local_folder_path, hdfs_folder_path, img_block_size)












