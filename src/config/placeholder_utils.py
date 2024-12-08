import os

def replace_placeholders(value):
        aws_region = os.getenv('AWS_REGION', '')
        aws_account_id = os.getenv('AWS_ACCOUNT_ID', '')
        env = os.getenv('ENV', '')
        project_name = 'bertybear-smart-nursery'
        
        return value.replace('${AWS::Region}', aws_region) \
                .replace('${AWS::AccountId}', aws_account_id) \
                .replace('${Env}', env) \
                .replace('${ProjectName}', project_name)