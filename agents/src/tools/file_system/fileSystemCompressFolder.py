
import shutil
import json

class fileSystemCompressFolder():
    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemCompressFolder",
            "description": "Compresses a folder into a ZIP file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The path of the folder to compress."
                    },
                    "archive_path": {
                        "type": "string",
                        "description": "The path for the resulting ZIP file."
                    }
                },
                "required": ["folder_path", "archive_path"]
            }
        }

    def run(self, io_handler=None):
        folder_path = self.arguments['folder_path']
        archive_path = self.arguments['archive_path']

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return json.dumps({"status": "error", "message": f"Folder '{folder_path}' does not exist or is not a directory."})

        try:
            shutil.make_archive(archive_path, 'zip', folder_path)
            return json.dumps({"status": "success", "message": f"Folder '{folder_path}' compressed to '{archive_path}.zip'."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
