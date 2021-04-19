from aws_cdk import (
    aws_s3 as _s3,
    core as cdk
)


class MyFirstCdkProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _s3.Bucket(
            self,
            "myBucketId",
            bucket_name="my-first-cdk-project-luber",
            versioned=True,
            encryption=_s3.BucketEncryption.S3_MANAGED,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL
        )
