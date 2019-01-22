resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${aws_lambda_function.set_marketing_preferences_lambda.function_name}"
  retention_in_days = 14
}
