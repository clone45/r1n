
import zipfile
import json

class fileSystemDecompressFolder():

    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def get_definition():
        return {
            "name": "fileSystemDecompressFolder",
            "description": "Decompresses a ZIP file into a folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "archive_path": {
                        "type": "string",
                        "description": "The path of the ZIP file to decompress."
                    },
                    "extract_path": {
                        "type": "string",
                        "description": "The path to extract the contents to."
                    }
                },
                "required": ["archive_path", "extract_path"]
            }
        }

    def run(self, io_handler=None):
        archive_path = self.arguments['archive_path']
        extract_path = self.arguments['extract_path']

        if not os.path.exists(archive_path) or not zipfile.is_zipfile(archive_path):
            return json.dumps({"status": "error", "message": f"Archive '{archive_path}' does not exist or is not a ZIP file."})

        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            return json.dumps({"status": "success", "message": f"ZIP file '{archive_path}' extracted to '{extract_path}'."})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
