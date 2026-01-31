import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CUSTOMERS'])
bedrock_runtime = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    
    for record in event['Records']:
        if record['eventName'] != 'INSERT':
            print("Wasn't a new entry. Skipping...")
            continue

        new_item = record['dynamodb']['NewImage']
        customer_id = new_item['customer_id']['S']
        customer_first_name = new_item['first_name']['S']

        if 'interests' not in new_item:
            print("No Interests field. Skipping...")
            continue

        interests = new_item['interests']['S']
        print(f"Processing ID: {customer_id} with Interests: {interests}")

        prompt_text = f"""
                    You are a cold email writer whose main purpose is to write concise, friendly, 
                    natural, and personalised cold emails for potential Ford Motor customers. This 
                    particular customer ({customer_first_name}) has the following interests: {interests}. The objective is to write a 
                    100-150-word cold email main body that tries to get the person interested in Ford products. 
                    You will take full advantage of the above interests provided to you by personalising the 
                    cold email with these. For example, if the potential customer likes snowboarding, one 
                    (or more) of the lines in the email body can be about how XYZ (choose any) model by Ford Motor 
                    can help the potential customer achieve the same. Write a natural, friendly, warm, and 
                    personalised email (main) body for marketing a Ford Motor car model. The email should 
                    be personalised to the person using the interests mentioned above. 
                    Do NOT include a subject line. Do NOT use markdown. Do NOT use bullet points. Only the email.
                    You can use the customer's first name in the email. Signature will be from "Ford Motors"
                    """
        
        llama_prompt = f"""
                        <|begin_of_text|><|start_header_id|>user<|end_header_id|>
                        {prompt_text}
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
                        """

        body = json.dumps({
            "prompt": llama_prompt,
            "max_gen_len": 512,
            "temperature": 0.7,
            "top_p": 0.9
        })

        try:
            response = bedrock_runtime.invoke_model(
                modelId='meta.llama3-8b-instruct-v1:0', 
                contentType='application/json',
                accept='application/json',
                body=body
            )

            response_body = json.loads(response['body'].read())
            
            generated_text = response_body['generation']
            
            table.update_item(
                Key={'customer_id': customer_id},
                UpdateExpression="set cold_email_content = :val",
                ExpressionAttributeValues={':val': generated_text}
            )
            print("Successfully added cold email content")
            
        except Exception as e:
            print(f"Error calling Bedrock or updating DB: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Process Complete')
    }
