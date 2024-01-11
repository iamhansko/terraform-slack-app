FROM public.ecr.aws/lambda/python:3.11

RUN yum install -y yum-utils shadow-utils
RUN yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
RUN yum -y install terraform
COPY ./src/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
COPY ./src ./

CMD [ "app.lambda_handler" ]