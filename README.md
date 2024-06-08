# cloud9
cloud storage using django, #BYOC                                                                                                                                   
- Designed using Azure Container service & App Service
-	Offers scalable and secure cloud storage solutions.  Integrated automation features to streamline deployment and management processes. Provides SSH access for secure command-line interface operations.
-	Authentication and isolation: Implemented Django authentication for robust user verification. Maintained data encryption and isolation, supported by FTP for secure file transfers, providing modularity.

![Screenshot 2024-06-08 221513](https://github.com/sourabhkv/cloud9/assets/55890376/9bb283b5-3796-4ba2-a809-ad7b5944ac4d)
![Screenshot 2024-06-08 221503](https://github.com/sourabhkv/cloud9/assets/55890376/3bda76df-338c-42df-898b-d2551d72c905)
![Screenshot 2024-06-08 221449](https://github.com/sourabhkv/cloud9/assets/55890376/f7bb2005-5098-4a71-ad0b-315dfc786459)
![Screenshot 2024-06-08 213213](https://github.com/sourabhkv/cloud9/assets/55890376/335bf936-2b8f-4fa3-9913-29ada07fe771)
![Screenshot 2024-06-08 210513](https://github.com/sourabhkv/cloud9/assets/55890376/41c9a11a-a04b-4225-8ad9-f515180556c7)


Max Size of drive depends on CLoud provider. Azure offers ~50 GiB for all users.<br>
FTP support limited to azure container service as it supports exposing more ports than app service instance.<br>

## Workarounds

- **Azure Storage Account Integration**: Enhance your storage capabilities by pairing Cloud9 with an Azure storage account.
- **Data Interaction**: Engage in a conversation with your data, making data management more interactive and intuitive.

## Features

- **Scalable Storage**: Cloud9 dynamically scales to meet your storage needs, offering up to 50 GiB of space per user on Azure.
- **Security and Isolation**: With Django's robust authentication system, your data remains encrypted and isolated. Plus, with FTP support, you can transfer files securely.
- **SSH Access**: Manage your container through a secure command-line interface, giving you full control over your environment.
- **Automation**: Streamline your deployment and management processes with integrated automation features.

## Automation
- Execute any Linux command within the secure environment of your container.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for videos only
- Uploading `URL_DOWNLOAD.txt` file containing links of files to be downloaded (works for any file format download).
- Implement file-based triggers for actions like uploading or deleting files (feature in progress).

## Limitations

- FTP support is exclusive to the Azure container service due to its ability to expose additional ports compared to the app service instance.
