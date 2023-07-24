import os
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from dotenv import load_dotenv
load_dotenv()

class DriveFunctions:
    @staticmethod
    def login_with_service_account(credentials=None):
        """
        Google Drive service with a service account.
        note: for the service account to work, you need to share the folder or
        files with the service account email.

        :return: google auth
        """
        # Define the settings dict to use a service account
        # We also can use all options available for the settings dict like
        # oauth_scope,save_credentials,etc.
        settings = {
                    "client_config_backend": "service",
                    "service_config": {
                        "client_json_file_path": "son-of-anton-368302-5d69bab81ff0.json" if not credentials else None,
                        "client_json_dict": credentials,
                    }
                }
        # Create instance of GoogleAuth
        gauth = GoogleAuth(settings=settings)
        # Authenticate
        gauth.ServiceAuth()
        return gauth

    # -----------------
    # listing files
    # -----------------
    # Auto-iterate through all files that matches this query
    @staticmethod
    def list_files(folder_id=None):
        drive = GoogleDrive(DriveFunctions.login_with_service_account(json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))))
        if folder_id is None:
            # search in root folder
            file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        else:
            # search in a specific folder
            file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
    
    @staticmethod
    def get_share_link(file):
        def convert_link_to_download_link(link):
            '''
                link:           https://drive.google.com/file/d/1WoSOw86YZMGvL9QP1er65Igm72_QCG3P/view?usp=drivesdk
                download_link:  https://drive.usercontent.google.com/download?id=1WoSOw86YZMGvL9QP1er65Igm72_QCG3P&export=download&confirm=t
            '''
            if link.startswith('https://drive.google.com/file/d/') and link.endswith('/view?usp=drivesdk'):
                file_id = link.split('https://drive.google.com/file/d/')[1].split('/view?usp=drivesdk')[0]
                download_link = link.replace('https://drive.google.com/file/d/', 'https://drive.usercontent.google.com/download?id=')
                download_link = download_link.replace('/view?usp=drivesdk', '&export=download&confirm=t')
            else:
                download_link = link
            return {'link': link, 'download_link':download_link, 'google_drive_file_id':file_id}
        
        # Insert the permission: reader -> anyone
        permission = file.InsertPermission({
                                'type': 'anyone',
                                'value': 'anyone',
                                'role': 'reader'})
        
        return convert_link_to_download_link(file['alternateLink'])  # Return the link.
        # print(file['alternateLink'])  # Display the sharable link.

    @staticmethod
    def upload_file_to_drive(file_to_upload, parent_folder_id, drive):
            # upload to given folder
            file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": parent_folder_id}]})
            file.SetContentFile(file_to_upload)
            file.Upload()
            def get_file_type(file_name):
                img_files = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
                text_files = ['.txt', '.js', '.py', '.json', '.html', '.css', '.scss', '.md', '.c', '.cpp', '.ts', '.pl']
                file_extension = '.' + file_name.split('.')[-1]  
                if file_extension in img_files:
                    return 'img'
                elif file_extension in text_files:
                    return 'text'
                else:
                    return 'other'
            filename = file_to_upload.split('/')[-1]
            metadata = {'filename' : filename, 'type': get_file_type(filename)}
            metadata.update(DriveFunctions.get_share_link(file))
            return metadata

    @staticmethod
    def upload_multiple_files(files_to_upload, parent_folder_id = '1ZeiruMO_zyQtFwt_XT45fgD8yhCW-Nr1'):
        # returns list of urls
        drive = GoogleDrive(DriveFunctions.login_with_service_account(json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))))
        print('---------uploading multiple files---------')
        uploaded_files = []
        for file in files_to_upload:
            uploaded_files.append(DriveFunctions.upload_file_to_drive(f'uploads/file_upload/{file.name}', parent_folder_id, drive))

            # delete file from media folder
            os.remove(f'uploads/file_upload/{file.name}')
        return uploaded_files

    @staticmethod
    def delete_files(files):
        print(f'---------deleting multiple files:{type(files)}{files}---------')
        drive = GoogleDrive(DriveFunctions.login_with_service_account(json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))))
        
        if type(files) == str:
            file_id = files.split('file/d/')[1].split('/view?usp=drivesdk')[0]
            print(f'deleting file id: {id} \n\n')
            
            # get file by id
            file = drive.CreateFile({'id': file_id})
            
            # file1 = drive.CreateFile({'id': file_id})
            file.Delete()

            DriveFunctions.list_files('1ZeiruMO_zyQtFwt_XT45fgD8yhCW-Nr1')
        else:
            for file in files:
                # print(f'type: {type(file)} val: {file}, str:{str(file)} \n\n')
                file_id = file.split('file/d/')[1].split('/view?usp=drivesdk')[0]
                print(f'deleting file id: {id} \n\n')
                
                # get file by id
                file = drive.CreateFile({'id': file_id})
                
                # file1 = drive.CreateFile({'id': file_id})
                file.Delete()

                DriveFunctions.list_files('1ZeiruMO_zyQtFwt_XT45fgD8yhCW-Nr1')