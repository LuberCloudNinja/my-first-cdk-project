from aws_cdk import (
    aws_ec2 as _ec2,
    core as cdk
)


class CustomEc2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """ Get environment variables from cdk.json: """
        prod_configs = self.node.try_get_context("envs")["Master"]

        """ Importing VPC to be use to launch EC2 instance: """
        vpc = _ec2.Vpc.from_lookup(self,
                                   "ImportVPC",
                                   vpc_id="vpc-0b8f4202bd52ea0d1")

        """ Creating Ec2 Instance: """
        web_server = _ec2.Instance(self,
                                   "WebServerId",
                                   instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
                                   instance_name="WebServer001",
                                   machine_image=_ec2.MachineImage.generic_linux(
                                       {prod_configs["regions"]["east"]: "ami-0742b4e673072066f"}
                                   ),
                                   vpc=vpc,
                                   vpc_subnets=_ec2.SubnetSelection(
                                       subnet_type=_ec2.SubnetType.PUBLIC
                                   ),
                                   availability_zone="us-east-1a",
                                   key_name="A4L")

        "Adding  tags to the Instance/s: "
        cdk.Tags.of(web_server).add("Owner", "Luber")