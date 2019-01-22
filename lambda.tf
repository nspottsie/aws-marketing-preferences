resource "aws_lambda_function" "set_marketing_preferences_lambda" {
  filename         = "set_marketing_preferences_lambda.zip"
  function_name    = "set_marketing_preferences"
  role             = "${aws_iam_role.set_marketing_preferences_lambda.arn}"
  handler          = "index.handler"
  source_code_hash = "${base64sha256(file("set_marketing_preferences_lambda.zip"))}"
  runtime          = "nodejs8.10"
  timeout          = 60
  memory_size      = 1024

  environment {
    variables = {
      marketing_preferences_url = "https://pages.awscloud.com/communication-preferences.html"
    }
  }
}
