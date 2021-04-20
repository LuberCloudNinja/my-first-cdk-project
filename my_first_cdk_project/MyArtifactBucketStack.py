from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    aws_kms as _kms,
    core as cdk
)


class MyArtifactBucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 buckets with different properties depending on the environment.

        mykey = _kms.Key.from_key_arn(self,
                                      "myKeyId",
                                      self.node.try_get_context('Master')["kms_arn"])
        if is_prod:
            artifactBucket = _s3.Bucket(self,
                                        "myMasterArtifactBucketId",
                                        bucket_name="my-master-artifact-bucket-luber",
                                        versioned=True,
                                        encryption=_s3.BucketEncryption.KMS,
                                        encryption_key=mykey,
                                        removal_policy=cdk.RemovalPolicy.RETAIN)
        else:
            artifactBucket = _s3.Bucket(self,
                                        "myDevArtifactBucketId",
                                        bucket_name="my-dev-artifact-bucket-luber",
                                        versioned=None,
                                        encryption=None,
                                        removal_policy=cdk.RemovalPolicy.DESTROY)
