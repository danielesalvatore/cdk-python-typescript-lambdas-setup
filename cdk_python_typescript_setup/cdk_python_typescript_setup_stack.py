from aws_cdk import Stack
from aws_cdk import aws_apigateway as _apigateway
from aws_cdk import aws_lambda as _lambda
from constructs import Construct
import os

class CdkPythonTypescriptSetupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        is_local = os.getenv("CI", False) == "true"

        ###############################
        # Python lambda build
        ###############################

        # Define the lambda layers to host python packages
        lambda_runtime = _lambda.Runtime.PYTHON_3_8
        lambda_layer_for_python_packages = _lambda.LayerVersion(
            self,
            "my_python_function_layer",
            code = _lambda.Code.from_asset("./build_my_python_function/"),
            compatible_runtimes = [ lambda_runtime ],
        )

        # Defines an AWS Lambda resource
        python_lambda = _lambda.Function(
            self, "my_python_function",
            runtime=lambda_runtime,
            code=_lambda.Code.from_asset(f"functions/my_python_function"),
            handler='lambda.handler',
            layers = [lambda_layer_for_python_packages],
        )

        # Local testing news crawling lambda API endpoint
        if is_local:
            python_api = _apigateway.RestApi(self, "my_python_function_api",
                                        description="my_python_function API",
                                        deploy_options= _apigateway.StageOptions(
                                            stage_name="development"
                                        )
                                    )
            api_resource = python_api.root.add_resource("my_python_function")
            api_resource.add_method("GET", _apigateway.LambdaIntegration(python_lambda))

        ###############################
        # TypeScript lambda build
        ###############################

        nodejs_lambda = _lambda.Function(
                self, "my_typescript_function",
                code=_lambda.Code.from_asset("functions/my_typescript_function"),
                handler='lambda.handler',
                runtime=_lambda.Runtime.NODEJS_16_X,
            )

        if is_local:
            typescript_api = _apigateway.RestApi(self, "my_typescript_function_api",
                                        description="my_typescript_function API",
                                        deploy_options= _apigateway.StageOptions(
                                            stage_name="development"
                                        )
                                    )
            api_resource = typescript_api.root.add_resource("my_typescript_function")
            api_resource.add_method("GET", _apigateway.LambdaIntegration(nodejs_lambda))

    