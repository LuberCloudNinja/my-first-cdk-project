from aws_cdk import (
    aws_ec2 as _ec2,
    aws_s3 as _s3,
    core as cdk
)


class CustomVpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """ Get environment variables from cdk.json: """
        prod_configs = self.node.try_get_context("envs")["Master"]

        "Create Custom VPC: "
        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr=prod_configs["vpc_configs"]["vpc_cidr"],
            max_azs=2,
            nat_gateways=2,
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

        """ Export this VPC by creating an output object: """
        cdk.CfnOutput(self,
                      "customVpcOutput",
                      value=custom_vpc.vpc_id,
                      export_name="customVpcId")

        """ Creating S3 Bucket: """
        my_bkt = _s3.Bucket(self, "CustomBktId")

        "Adding tags to S3: "

        """ Resource in same account: """
        bkt_1 = _s3.Bucket.from_bucket_name(
            self,
            "MyImportedBucket",
            "luber-emr-cluster"
        )

        """ Importing S3 bucket from a different account"""
        bkt_2 = _s3.Bucket.from_bucket_arn(
            self,
            "CrossAccountBucket",
            "arn:aws:s3:::luberhayproduction")

        cdk.CfnOutput(self,
                      "myImportedBucket",
                      value=bkt_1.bucket_name)

        """ Importing default VCP: """
        vpc_2 = _ec2.Vpc.from_lookup(self,
                                     "ImportedVPC",
                                     vpc_id="vpc-0b8f4202bd52ea0d1")
        cdk.CfnOutput(self,
                      "ImportedVPC_2",
                      value=vpc_2.vpc_id)

        # """ Peering VPCs: """
        # peer_vpc = _ec2.CfnVPCPeeringConnection(self,
        #                                         "peerVpc",
        #                                         peer_vpc_id=custom_vpc.vpc_id,
        #                                         vpc_id=vpc_2.vpc_id
        #                                         )
