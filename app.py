#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_python_typescript_setup.cdk_python_typescript_setup_stack import CdkPythonTypescriptSetupStack


app = cdk.App()
CdkPythonTypescriptSetupStack(app, "cdk-python-typescript-setup")

app.synth()
