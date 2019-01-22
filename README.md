## AWS Marketing Preferences
This repository contains a proof of concept solution that uses Selenium inside a Lambda function to set the AWS account marketing preferences for a given email address.

Currently the solution will launch selenium, navigate to the [Marketing Preferences Website](https://pages.awscloud.com/communication-preferences.html), and fill out the form to unsubscribe the email address from all marketing emails.

### Requirements
1. AWS account
1. AWS permissions to install/configure the lambda with supporting resources (Cloudwatch Logs, IAM, etc.)
1. [Terraform](https://www.terraform.io/downloads.html) (solution tested on v11.11)

### Setup
1. Clone repository
1. [Download](https://github.com/nspottsie/aws-marketing-preferences/releases/tag/v1.0) the lambda function bundle into the repository
1. Open terminal/command prompt. Then: `terraform plan -out plan`
1. Verify the terraform plan. Then: `terraform apply plan`
1. When terraform is complete and has created all resources, login to the [AWS Management Console](https://console.aws.amazon.com/), choose the Lambda service, create a sample test event `{ "email_address": "testemail@testdomain.com" }` with a valid email address, and test the function

### Credits
This solution is possible due to previous work from the Blackboard team to get Chromium running inside of AWS Lambda: https://github.com/blackboard/lambda-selenium
