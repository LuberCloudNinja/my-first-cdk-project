from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    core as cdk
)


class MyArtifactBucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 buckets with different properties depending on the environment.
        if is_prod:
            artifactBucket = _s3.Bucket(self,
                                        "myProdArtifactBucketId",
                                        bucket_name="my-prod-artifact-bucket-luber",
                                        versioned=True,
                                        encryption=_s3.BucketEncryption.S3_MANAGED,
                                        removal_policy=cdk.RemovalPolicy.RETAIN)
        else:
            artifactBucket = _s3.Bucket(self,
                                        "myDevArtifactBucketId",
                                        bucket_name="my-dev-artifact-bucket-luber",
                                        versioned=None,
                                        encryption=None,
                                        removal_policy=cdk.RemovalPolicy.DESTROY)
