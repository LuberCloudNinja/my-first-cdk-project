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

""" Environment Variables below: """
app = core.App()

# Prod Account:
pro_account = app.node.try_get_context("Prod")["account"]
prod_east = region = app.node.try_get_context("Prod")["regions"]["east"]
prod_west = app.node.try_get_context("Prod")["regions"]["west"]

env_US_EAST_Prod = core.Environment(account=pro_account, region=prod_east)
env_US_WEST_Prod = core.Environment(account=pro_account, region=prod_west)

# Dev Account:
dev_account = app.node.try_get_context("Dev")["account"]
dev_east = app.node.try_get_context("Dev")["regions"]["east"]
dev_west = app.node.try_get_context("Dev")["regions"]["west"]

env_US_EAST_Dev = core.Environment(account=dev_account, region=dev_east)
env_US_WEST_Dev = core.Environment(account=dev_account, region=dev_west)

# Master Account:
master_account = app.node.try_get_context("Master")["account"]
master_east = app.node.try_get_context("Master")["regions"]["east"]
master_west = app.node.try_get_context("Master")["regions"]["west"]

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


app.synth()
