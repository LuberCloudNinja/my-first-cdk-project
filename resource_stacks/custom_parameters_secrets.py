import json

from aws_cdk import (
    aws_ssm as _ssm,
    aws_secretsmanager as _secretsmanager,
    core as cdk
)


class CustomParametersSecretsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        "Create Secrets & SSM Parameters: "
        param1 = _ssm.StringParameter(
            self,
            "Parameter1",
            description="Load testing configuration",
            parameter_name="No_Of_Concurrent_Users",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )

        param2 = _ssm.StringParameter(
            self,
            "Parameter2",
            description="Load testing configuration",
            parameter_name="/locust/configs/No_Of_Concurrent_Users",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )

        param3 = _ssm.StringParameter(
            self,
            "Parameter3",
            description="Load testing configuration",
            parameter_name="/locust/configs/DurationInSec",
            string_value="300",
            tier=_ssm.ParameterTier.STANDARD
        )

        """ Build Secrets in Secrets Manager: """
        secret1 = _secretsmanager.Secret(
            self,
            "Secret1",
            description="Customer DB password",
            secret_name="Custom_DB_Password"
        )

        templated_secret = _secretsmanager.Secret(
            self,
            "Secret2",
            description="A Templated secret for user data",
            secret_name="User_Kon_Attributes",
            generate_secret_string=_secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {"username": "Kon"}
                ),
                generate_string_key="password"
            )
        )

        """ Output: """
        output_1 = cdk.CfnOutput(self,
                                 "Parameter1Value",
                                 description="No_Of_Concurrent_Users",
                                 value=f"{param1.string_value}"
                                 )

        output_2 = cdk.CfnOutput(self,
                                 "Secret1Value",
                                 value=f"{secret1.secret_value}")