from aws_cdk import (
    aws_rds as _rds,
    aws_ec2 as _ec2,
    core as cdk
)


class RdsDatabase3TierStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        """ Create an RDS Database: """

        konstone_db = _rds.DatabaseInstance(self,
                                            "konstoneRDS",
                                            database_name="konstone_db",
                                            engine=_rds.DatabaseInstanceEngine.MYSQL,
                                            vpc=vpc,
                                            port=3306,
                                            allocated_storage=30,
                                            multi_az=False,
                                            cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
                                            instance_type=_ec2.InstanceType.of(
                                                _ec2.InstanceClass.BURSTABLE2,
                                                _ec2.InstanceSize.MICRO
                                            ),
                                            removal_policy=cdk.RemovalPolicy.DESTROY,
                                            deletion_protection=False,
                                            delete_automated_backups=True,
                                            backup_retention=cdk.Duration.days(7)
                                            )

        # Get ASG security groups:

        for sg in asg_security_groups:
            konstone_db.connections.allow_default_port_from(sg, "Allow EC2 ASG access to RDS MySQL")

        # Output for DB Endpoint:
        output_1 = cdk.CfnOutput(self,
                                 "DatabaseConnectionCommand",
                                 value=f"mysql - h {konstone_db.db_instance_endpoint_address} -p 3306 -u mystiquemas",
                                 description="Connect to the database using this command")
