from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    core as cdk
)


class MyFirstCdkProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating first S3 Bucket:
        _s3.Bucket(
            self,
            "myBucketId",
            bucket_name="my-first-cdk-project-luber",
            versioned=True,
            encryption=_s3.BucketEncryption.S3_MANAGED,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY # This object will delete the bucket when destroying
            # the stack using "cdk destroy" only if the bucket is empty.
        )

        # Creating second S3 Bucket:
        my_bucket = _s3.Bucket(
            self,
            "myBucketId1",
            bucket_name="my-first-cdk-project-luber-1",
            removal_policy=cdk.RemovalPolicy.DESTROY  # This object will delete the bucket when destroying
            # the stack using "cdk destroy" only if the bucket is empty.
        )

        snstopicname = "abczys"

        if not cdk.Token.is_unresolved(snstopicname) and len(snstopicname) > 10:
            raise ValueError("Maximum value can be only 10 characters")

        print(my_bucket.bucket_name)

        # Create an IAM group:

        _iam.Group(self,
                   "gid",
                   group_name="MyCDKAdmin"
                   )
        output_1 = cdk.CfnOutput(
            self,
            "myBucketOutput1",
            value=my_bucket.bucket_name,
            description=f"My first CDK Bucket",
            export_name="myBucketOutput1"
        )
