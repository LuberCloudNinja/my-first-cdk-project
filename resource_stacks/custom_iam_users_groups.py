from aws_cdk import (
    aws_secretsmanager as _secrets_manager,
    aws_iam as _iam,
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
                                    group_name="konstone_group",
                                    managed_policies=[])

        # Add Users to Group:
        konstone_group.add_user(user2)

        """ Login Url Autogenerate: """

        output_1 = cdk.CfnOutput(self,
                                 "user2Login",
                                 description="LoginUrl for User2",
                                 value=f"https://{cdk.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
                                 )
