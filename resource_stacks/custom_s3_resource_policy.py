from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    core as cdk
)


class CustomS3ResourcePolicyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """ Create S3 Bucket: """
        konstone_bkt = _s3.Bucket(self,
                                  "konstoneAssets",
                                  bucket_name="luber-testing-bucket-policy-via-cdk",
                                  versioned=True,
                                  removal_policy=cdk.RemovalPolicy.DESTROY
                                  )

        # Add bucket resource policy:

        konstone_bkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[konstone_bkt.arn_for_objects("*.html")],
                principals=[_iam.AnyPrincipal()]
            )
        )

        konstone_bkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{konstone_bkt.bucket_arn}/*"],
                principals=[_iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTransport": False}
                }
            )
        )
