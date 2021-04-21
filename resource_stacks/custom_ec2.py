from aws_cdk import (
    aws_ec2 as _ec2,
    aws_ssm as _ssm,
    aws_iam as _iam,
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

        """ Read BootStrap Script: """
        with open("bootstrap_script/install_httpd.sh", mode="r") as file:
            user_data = file.read()

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
                                   key_name="A4L",
                                   user_data=_ec2.UserData.custom(user_data)
                                   )

        """ Add permission to web server instance profile: """
        # Allow the instance profile to call SSM:
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )
        # Allow the instance profile to have ReadOnly access to S3:
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )

        """ Allow Web Traffic to WebServer: """
        web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow Web Traffic"
        )

        "Adding  tags to the Instance/s: "
        cdk.Tags.of(web_server).add("Owner", "Luber")

        """ Create an output field to show IP address of the web server: """
        output_1 = cdk.CfnOutput(
            self,
            "WebServer00IP",
            description="WebServer Public IP Address",
            value=f"http://{web_server.instance_public_ip}"
        )
