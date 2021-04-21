from aws_cdk import (
    aws_ec2 as _ec2,
    aws_s3 as _s3,
    core as cdk
)


class CustomVpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC:

        prod_configs = self.node.try_get_context("envs")["Master"]

        "Create Custom VPC: "
        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr=prod_configs["vpc_configs"]["vpc_cidr"],
            max_azs=3,
            nat_gateways=3,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="PublicSubnet", cidr_mask=prod_configs["vpc_configs"]["cidr_mask"],
                    subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="PrivateSubnet", cidr_mask=prod_configs["vpc_configs"]["cidr_mask"],
                    subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="DBSubnet", cidr_mask=prod_configs["vpc_configs"]["cidr_mask"],
                    subnet_type=_ec2.SubnetType.ISOLATED
                )

            ]

        )

        "Adding  tags to the vpc resources: "
        cdk.Tags.of(custom_vpc).add("Owner", "Luber")

        """ Export this VPC by creating an output object: """
        cdk.CfnOutput(self,
                      "customVpcOutput",
                      value=custom_vpc.vpc_id,
                      export_name="customVpcId")

        """ Creating S3 Bucket: """
        my_bkt = _s3.Bucket(self, "CustomBktId")

        "Adding tags to S3: "
        cdk.Tags.of(my_bkt).add("Owner", "Luber")

        """ Resource in same account: """
        bkt_1 = _s3.Bucket.from_bucket_name(
            self,
            "MyImportedBucket",
            "luber-emr-cluster"
        )

        cdk.CfnOutput(self,
                      "myImportedBucket",
                      value=bkt_1.bucket_name)
