#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.

from aws_cdk import core

""" Importing stacks from code modules: """
from my_first_cdk_project.MyArtifactBucketStack import MyArtifactBucketStack
from my_first_cdk_project.my_first_cdk_project_stack import MyFirstCdkProjectStack
from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.custom_ec2 import CustomEc2Stack
from resource_stacks.web_server_stack import WebServerStack
from resource_stacks.vpc_stack import VpcStack

""" Environment Variables below: """
app = core.App()

# Prod Account:
prod_account = app.node.try_get_context("envs")["Prod"]["account"]
prod_account_tags = app.node.try_get_context("envs")["Prod"]["stack-team-support-email"]
prod_east = region = app.node.try_get_context("envs")["Prod"]["regions"]["east"]
prod_west = app.node.try_get_context("envs")["Prod"]["regions"]["west"]

env_US_EAST_Prod = core.Environment(account=prod_account, region=prod_east)
env_US_WEST_Prod = core.Environment(account=prod_account, region=prod_west)

# Dev Account:
dev_account = app.node.try_get_context("envs")["Dev"]["account"]
dev_account_tags = app.node.try_get_context("envs")["Dev"]["stack-team-support-email"]
dev_east = app.node.try_get_context("envs")["Dev"]["regions"]["east"]
dev_west = app.node.try_get_context("envs")["Dev"]["regions"]["west"]

env_US_EAST_Dev = core.Environment(account=dev_account, region=dev_east)
env_US_WEST_Dev = core.Environment(account=dev_account, region=dev_west)

# Master Account:
master_account = app.node.try_get_context("envs")["Master"]["account"]
master_account_tags = app.node.try_get_context("envs")["Master"]["stack-team-support-email"]
master_east = app.node.try_get_context("envs")["Master"]["regions"]["east"]
master_west = app.node.try_get_context("envs")["Master"]["regions"]["west"]


env_US_EAST_Master = core.Environment(account=master_account, region=master_east)
env_US_WEST_Master = core.Environment(account=master_account, region=master_west)

"Stacks: "
# Prod Account Stacks:
# Dev Account Stacks:

# Master Account Stacks:
MyFirstCdkProjectStack(app, "MyFirstCdkProjectStack")
MyArtifactBucketStack(app, "MyDevStack", env=env_US_WEST_Master)
MyArtifactBucketStack(app, "MyMasterStack", is_prod=True, env=env_US_EAST_Master)
CustomVpcStack(app, "MyCustomVpc", env=env_US_EAST_Master)
CustomEc2Stack(app, "My-Web-Server-Stack",env=env_US_EAST_Master)
# WebServerStack(app, "Web-Server-ASG-ALB-stack", env=env_US_EAST_Master)

# Application Stack ASG and ALB
vpc_stack = VpcStack(app, "multi-tier-app-vpc-stack", env=env_US_EAST_Master)
ec2_stack = WebServerStack(app, "multi-tier-app-web-server-stack", vpc=vpc_stack.vpc, env=env_US_EAST_Master)


""" Tagging the stacks: Global tagging, meaning all resources in the stack will have the same tags """

# Prod Account Tagging:
# cdk.Tags.of().add(key="stack-team-support-email", value=prod_account_tags)

# Dev Account Tagging:
# cdk.Tags.of().add(key="stack-team-support-email", value=dev_account_tags)

# Master Account Tagging:
cdk.Tags.of(app).add(key="stack-team-support-email", value=master_account_tags)


app.synth()

