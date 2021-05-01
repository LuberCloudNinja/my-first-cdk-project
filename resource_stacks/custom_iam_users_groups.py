from aws_cdk import (
    aws_secretsmanager as _secrets_manager,
    aws_iam as _iam,
    aws_ssm as _ssm,
    core as cdk
)


class CustomIamUsersGroupsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """ Create IAM, Users & Groups: """

        # Create Users passwords:
        user1_pass = _secrets_manager.Secret(
            self,
            "user1Pass",
            description="Password for User1",
            secret_name="user1_pass"
        )

        # Add user1 with SecretsManager Password:
        user1 = _iam.User(self,
                          "user1",
                          password=user1_pass.secret_value,
                          user_name="user1")

        # Add user2 with Literal Password (NOT RECOMMENDED):
        user2 = _iam.User(self,
                          "user2",
                          password=cdk.SecretValue.plain_text(
                              "Dont-Use-B@d-Passw0rds"
                          ),
                          user_name="user2")

        """ Add IAM Group: """
        # Create IAM Group:
        konstone_group = _iam.Group(self,
                                    "konStoneGroup",
                                    group_name="konstone_group"
                                    )

        # Add Users to Group:
        konstone_group.add_user(user1)

        # Add Manage Policy To Group:
        konstone_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )
        # SSM parameter store 1:
        param1 = _ssm.StringParameter(
            self,
            "Parameter1",
            description="Keys to KonStone",
            parameter_name="/konstone/keys/fish",
            string_value="130481",
            tier=_ssm.ParameterTier.STANDARD
        )

        # SSM parameter store 2:
        param1 = _ssm.StringParameter(
            self,
            "Parameter2",
            description="Keys to KonStone",
            parameter_name="/konstone/keys/fish/gold",
            string_value="130481",
            tier=_ssm.ParameterTier.STANDARD
        )

        # Grant Group to LIST/describe all SSM Parameters in the console:
        group_statement_1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        # This's the SID in the policy
        group_statement_1.sid = "DescribeAllParametersInTheConsole"

        # Add policy to the group:
        konstone_group.add_to_policy(group_statement_1)

        # Create IAM Role:
        konstone_ops_role = _iam.Role(
            self,
            "konstoneOpsRole",
            assumed_by=_iam.AccountPrincipal(f"{cdk.Aws.ACCOUNT_ID}"),
            role_name="konstone_ops_role"
        )

        # Create Managed Policy & Attached ROle:
        list_ec2_policy = _iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="List ec2 instances in the account",
            managed_policy_name="list_ec2_policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            roles=[
                konstone_ops_role
            ]
        )
        # Grant Konstone group permission to Param 1:
        param1.grant_read(konstone_group)

        """ Login Url Autogenerate: """
        # Below we'll get the user Url to sign in to the AWS console:
        output_1 = cdk.CfnOutput(self,
                                 "user2Login",
                                 description="LoginUrl for User2",
                                 value=f"https://{cdk.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
                                 )
