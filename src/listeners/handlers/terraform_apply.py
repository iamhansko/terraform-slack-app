import os
from subprocess import Popen, PIPE, STDOUT
import boto3

TERRAFROM_STATE_S3_BUCKET_NAME = os.getenv('TERRAFROM_STATE_S3_BUCKET_NAME')

def handler(respond, body):

    user_text = body['text'].split('\n', 1)

    state_name = user_text[0]
    state_checker = False
    
    if not (state_name is None or len(state_name) == 0):
      s3 = boto3.client('s3')

      states = s3.list_objects(Bucket=TERRAFROM_STATE_S3_BUCKET_NAME, Delimiter='/')
      
      if not(states.get('CommonPrefixes') is None or len(states.get('CommonPrefixes')) == 0):
         for state in states.get('CommonPrefixes'):
            folder = state.get('Prefix')

            if folder[0:-1] == state_name:
               state_checker = True
      
      if state_checker == False:
         respond(':gear: 일치하는 Terraform State가 없습니다. 새로운 State를 생성합니다. (New Terraform State created)')
         if user_text is None or len(user_text) <= 1 or user_text[1] is None or  len(user_text[1]) == 0:
            respond(':warning: main.tf의 본문을 채워주세요. (No main.tf contents)')
            return True
         s3.put_object(
            Bucket = TERRAFROM_STATE_S3_BUCKET_NAME,
            Body = user_text[1],
            Key = f'{state_name}/main.tf'
         )

      s3.download_file(TERRAFROM_STATE_S3_BUCKET_NAME, f'{state_name}/main.tf', '/tmp/main.tf')

      print('---------- TERRAFORM INIT ----------')
      terraform_init_result = Popen('cd /tmp && terraform init', stdout=PIPE, stderr=STDOUT, shell=True, text=True).stdout.read()
      print(terraform_init_result)
      
      print('---------- TERRAFORM APPLY ----------')
      terraform_apply_result = Popen('cd /tmp && terraform apply -no-color -auto-approve', stdout=PIPE, stderr=STDOUT, shell=True, text=True).stdout.read()
      print(terraform_apply_result)

      terraform_state_result = Popen('cat /tmp/terraform.tfstate', stdout=PIPE, stderr=STDOUT, shell=True, text=True).stdout.read()

      s3.put_object(
          Bucket = TERRAFROM_STATE_S3_BUCKET_NAME,
          Body = terraform_state_result,
          Key = f'{state_name}/terraform.tfstate'
      )
      
      respond(f'```{terraform_apply_result}```')