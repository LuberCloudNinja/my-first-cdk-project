from aws_cdk import (
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_autoscaling as _autoscaling,
    core as cdk
)


class WebServerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """ Read UserData Script: """
        try:
            with open("bootstrap_script/install_httpd.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print("Unable to read UserData script")

        """ AMI: """
        linux_ami = _ec2.AmazonLinuxImage(generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                          edition=_ec2.AmazonLinuxEdition.STANDARD,
                                          virtualization=_ec2.AmazonLinuxVirt.HVM,
                                          storage=_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                          )

        """ Create ALB: """
        alb = _elbv2.ApplicationLoadBalancer(
            self,
            "MyAlbId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )

        # Allow alb SG to receive traffic from port 80:
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow Internet access on ALB port 80"
        )

        # Add listener to ALB:
        listener = alb.add_listener("listenerId",
                                    port=80,
                                    open=True)

        """ Web server IAM role: """
        web_server_role = _iam.Role(self, "WebServerRoleId",
                                    assumed_by=_iam.ServicePrincipal("ec2.amazonaws.com"),
                                    managed_policies=[
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonSSMManagedInstanceCore",
                                        ),
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonS3ReadOnlyAccess"
                                        )
                                    ])

        """ Create ASG with 2 EC2 instances: """
        web_server_asg = _autoscaling.AutoScalingGroup(self,
                                                       "WebServerAsgId",
                                                       vpc=vpc,
                                                       key_name="A4L",
                                                       vpc_subnets=_ec2.SubnetSelection(
                                                           subnet_type=_ec2.SubnetType.PRIVATE
                                                       ),
                                                       instance_type=_ec2.InstanceType(
                                                           instance_type_identifier="t2.micro",
                                                       ),
                                                       machine_image=linux_ami,
                                                       role=web_server_role,
                                                       min_capacity=1,
                                                       max_capacity=4,
                                                       desired_capacity=2,
                                                       user_data=_ec2.UserData.custom(user_data)
                                                       )
        # Allow ASG SG to receive traffic from ALB SG:
        web_server_asg.connections.allow_from(alb, _ec2.Port.tcp(80),
                                              description="Allow ASG SG to receive traffic from ALB SG")

        # Add ASG Instances to the ALB Target Group:
        listener.add_targets("ListenerId", port=80, targets=[web_server_asg])

        """ Output of the ALB DOmain Name: """
        output_alb_1 = cdk.CfnOutput(self,
                                     "AlbDomainName",
                                     value=f"http://{alb.load_balancer_name}",
                                     description="Web Server ALB Domain Name")

        """ Tags: """
        cdk.Tags.of(alb).add("Owner", "Luber")
        cdk.Tags.of(web_server_role).add("Owner", "Luber")
