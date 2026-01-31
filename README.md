# Serverless Personalized Marketing Engine

A cloud-native application that automates the generation of personalised marketing emails. This system leverages an event-driven architecture on AWS to detect new customer entries and immediately generate tailored email content using Generative AI (Meta Llama 3 via AWS Bedrock).

## Project Overview

In traditional marketing, generic email blasts often result in low engagement and high unsubscribe rates. This project solves that problem by automating the creation of 'cold emails' that are specifically contextualised to an individual's unique interests.

**How it works:**
1.  **Ingestion:** A new customer profile is added to the database via a client script.
2.  **Trigger:** The database update automatically triggers a background Lambda function via DynamoDB Streams.
3.  **Analysis:** A Large Language Model (LLM) analyzes the customer's demographics and interests.
4.  **Generation:** The model writes a persuasive, personalized email connecting the product (e.g., Ford Motors) to the customer's specific hobbies.
5.  **Storage:** The generated content is saved back to the customer record, ready for dispatch.

This project demonstrates the integration of **NoSQL databases**, **Serverless Compute**, and **Generative AI** into a cohesive pipeline.

## Key Learnings

Building this project provided hands-on experience with modern cloud engineering concepts:

* **Event-Driven Architecture:** Learned how to utilize **DynamoDB Streams** to trigger asynchronous compute functions (Lambda) in response to database changes, decoupling input logic from processing logic.
* **Infrastructure as Code (Boto3):** Gained proficiency in the AWS SDK for Python (`boto3`) to interact programmatically with cloud resources rather than relying solely on the GUI console.
* **Generative AI Integration:** Implemented **Prompt Engineering** techniques within a programmatic pipeline, managing context windows and temperature settings for **Meta Llama 3** via AWS Bedrock.
* **NoSQL Data Modeling:** Designed a DynamoDB schema to handle unstructured user data and perform efficient conditional writes (e.g., uniqueness checks on Customer ID).

## Technical Details

### Architecture & Stack
* **Language:** Python 3.x
* **Database:** AWS DynamoDB (Key-Value store)
* **Compute:** AWS Lambda (Serverless functions)
* **AI/ML:** AWS Bedrock runtime invoking `meta.llama3-8b-instruct-v1:0`
* **Orchestration:** DynamoDB Streams

### Implementation Highlights
* **Atomic Transactions:** The client-side script (`add_customer.py`) implements a `while` loop with `get_item` checks to ensure Customer ID uniqueness before writing, preventing data overwrite collisions.
* **Stream Processing:** The Lambda function processes `INSERT` events specifically. It filters out non-insert events or records missing required fields to ensure robust error handling.
* **State Management:** The Lambda function performs an `update_item` operation to append the generated email to the existing record without altering the original user data.

## How to Run This Project

### Prerequisites
* **Python 3.8+** installed locally.
* An **AWS Account** with permissions for DynamoDB, Lambda, and Bedrock.
* **AWS CLI** configured locally with valid credentials.
* **Model Access:** Ensure Model Access for "Meta Llama 3 8b Instruct" is granted in the AWS Bedrock console (Region: `us-east-1`).

### 1. Cloud Infrastructure Setup
Before running the code, the following AWS resources must exist:

1.  **DynamoDB Table:**
    * Name: `potential_customers_for_ford`
    * Partition Key: `customer_id` (String)
    * *Note: Enable "DynamoDB Stream" (View type: New images).*
2.  **AWS Lambda Function:**
    * Create a function using Python 3.x.
    * **Environment Variable:** Set Key: `CUSTOMERS`, Value: `potential_customers_for_ford`.
    * **Permissions (IAM):** Attach a policy allowing `dynamodb:UpdateItem` and `bedrock:InvokeModel`.
    * **Trigger:** Add the DynamoDB table as a trigger for this function.
    * **Code:** Paste the contents of `lambda_function.py` into the editor.

### 2. Local Setup
Clone the repository and install the AWS SDK.

```bash
git clone https://github.com/Paarth3/Ford_cloud_automation_for_cold_emails
cd Ford_cloud_automation_for_cold_emails
pip install boto3
```

### 3. Usage
Run the client script to simulate a new customer signup.

```bash
python add_customer.py
```

**Interaction Example:**
```bash
Please enter your unique customer ID: 27
Please enter your first name: Paarth
Please enter your last name: Pasari
Please enter your interests separated by commas (,): Trekking, Mountains, Photography
Please enter your age: 18
```

### 4. Verification
Once the script finishes, the Lambda function triggers automatically in the cloud.
1. Go to the AWS DynamoDB Console.
2. Select the `potential_customers_for_ford` table.
3. View the items. You will see a new field, `cold_email_content`, added to Paarth's record, containing a generated email referencing his interests.
