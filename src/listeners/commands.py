import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from listeners.handlers import terraform_apply, terraform_destroy, terraform_list_states

def listener(app):
    app.command("/list_states")(
        ack=respond_to_list_states_command_within_3_seconds,  
        lazy=[terraform_list_states.handler]  
    )

    app.command("/apply")(
        ack=respond_to_apply_command_within_3_seconds,  
        lazy=[terraform_apply.handler]  
    )

    app.command("/destroy")(
        ack=respond_to_destroy_command_within_3_seconds,  
        lazy=[terraform_destroy.handler]  
    )

def respond_to_list_states_command_within_3_seconds(ack):
    ack(":robot_face: Terraform State 목록을 조회합니다. (Terraform State List stored in S3 Bucket)")

def respond_to_apply_command_within_3_seconds(body, ack):
    text = body["text"].split('\n', 1)[0]
    if text is None or len(text) == 0:
        ack(":warning: Usage: /apply (state name here)")
    else:
        ack(f":robot_face: *{text}* State에 대한 Terraform Apply를 수행합니다. 작업이 완료되면 그 결과가 출력됩니다. (Terraform Apply executed)")

def respond_to_destroy_command_within_3_seconds(body, ack):
    text = body["text"]
    if text is None or len(text) == 0:
        ack(":warning: Usage: /destroy (state name here)")
    else:
        ack(f":robot_face: *{text}* State에 대한 Terraform Destroy를 수행합니다. 작업이 완료되면 그 결과가 출력됩니다. (Terraform Destroy executed)")