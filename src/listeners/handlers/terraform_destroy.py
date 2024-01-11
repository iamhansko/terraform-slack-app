import os
from subprocess import Popen, PIPE, STDOUT
import boto3

TERRAFROM_STATE_S3_BUCKET_NAME = os.getenv('TERRAFROM_STATE_S3_BUCKET_NAME')

def handler(respond, body):
    state_name = body['text']
    
    if not (state_name is None or len(state_name) == 0):
      s3 = boto3.client('s3')

      states = s3.list_objects(Bucket=TERRAFROM_STATE_S3_BUCKET_NAME, Delimiter='/')
      
      if states.get('CommonPrefixes') is None or len(states.get('CommonPrefixes')) == 0:
         respond(':warning: 저장된 Terraform State가 없습니다. S3 Bucket에 State가 있는지 확인해주세요. (No Matching State)')
         return True
      
      for state in states.get('CommonPrefixes'):
         folder = state.get('Prefix')

         if folder[0:-1] == state_name:
            s3.download_file(TERRAFROM_STATE_S3_BUCKET_NAME, f'{state_name}/main.tf', '/tmp/main.tf')
            s3.download_file(TERRAFROM_STATE_S3_BUCKET_NAME, f'{state_name}/terraform.tfstate', '/tmp/terraform.tfstate')
            
            print('---------- TERRAFORM INIT ----------')
            terraform_init_result = Popen('cd /tmp && terraform init', stdout=PIPE, stderr=STDOUT, shell=True, text=True).stdout.read()
            print(terraform_init_result)
            
            print('---------- TERRAFORM DESTROY ----------')
            terraform_destroy_result = Popen('cd /tmp && terraform destroy -no-color -auto-approve', stdout=PIPE, stderr=STDOUT, shell=True, text=True).stdout.read()
            print(terraform_destroy_result)

            s3.delete_object(Bucket=TERRAFROM_STATE_S3_BUCKET_NAME, Key=f'{state_name}/terraform.tfstate')
            # s3.delete_object(Bucket=TERRAFROM_STATE_S3_BUCKET_NAME, Key=f'{state_name}/main.tf')
            # s3.delete_object(Bucket=TERRAFROM_STATE_S3_BUCKET_NAME, Key=f'{state_name}/')

            respond(f'```{terraform_destroy_result}```')

            return True
      
      respond(':warning: 일치하는 Terraform State가 없습니다. State명을 다시 확인해주세요. (No Matching State)')