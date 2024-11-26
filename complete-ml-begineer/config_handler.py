
from pathlib import Path
import json
import boto3

# from anomaly_detection_services.utils.s3handler import download_file_from_s3

APP_CONFIG_FILE = 'critical_config.json'
S3_CONFIG_PATH = 'anomaly_detection/config'


def get_config_file(app_config_file=APP_CONFIG_FILE)->dict: 
  """
  Gets the configuration file, downloading it from S3 if necessary.

  Args:
      app_config_file (str, optional): The name of the configuration file. Defaults to 'critical_config.json'.

  Returns:
      dict: The contents of the configuration file.
  """
  path = Path(Path(__file__).parent.resolve(), app_config_file)

  if path.exists():
    print("EXIST",path)
    with open(path) as f:
      return json.load(f)
  # else:
  #   # Use the download_file_from_s3 function to download and load the config file
  #   s3_path = f'{S3_CONFIG_PATH}/{APP_CONFIG_FILE}'
  #   print(s3_path)
  #   return download_file_from_s3(boto3.client('s3'),str(s3_path),path)


app_configs = get_config_file()
print("configs", app_configs)
if __name__ == "__main__":
    pass