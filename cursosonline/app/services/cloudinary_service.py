import cloudinary
import cloudinary.uploader
from flask import current_app

class CloudinaryService:
    @staticmethod
    def configure():
        cloudinary.config(
            cloud_name=current_app.config['planmejora'],
            api_key=current_app.config['152846835448636'],
            api_secret=current_app.config['TSQ-S0VRCMHmL1ntimkpkgl2WoQ']
        )
    
    @staticmethod
    def upload_file(file, folder='course_platform'):
        """
        Upload file to Cloudinary
        
        :param file: File object to upload
        :param folder: Cloudinary folder to upload to
        :return: Dictionary with upload result
        """
        CloudinaryService.configure()
        
        upload_result = cloudinary.uploader.upload(
            file, 
            folder=folder,
            resource_type='auto'
        )
        
        return upload_result
    
    @staticmethod
    def delete_file(public_id):
        """
        Delete file from Cloudinary
        
        :param public_id: Public ID of the file to delete
        :return: Dictionary with deletion result
        """
        CloudinaryService.configure()
        
        return cloudinary.uploader.destroy(public_id)