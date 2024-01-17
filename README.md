# Automate Code Pipeline

This repository contains templates to automate the creation and deployment of AWS CodePipeline resources.

## How it works

The main branch of this repository contains a CloudFormation template (`modify_main_pipeline.json`) that can modify the source of an existing Automation CodePipeline. You can use this template to create a new pipeline by changing the `BranchName` and `FullRepositoryId` parameters.

The demo-pipeline branch of this repository contains another CloudFormation template (`pipeline.json`) that will reset the existing Automation CodePipeline. 
When there's a change in (`modify_main_pipeline.json`) existing Automation CodePipeline source will be changed to demo-pipeline branch and will build a new pipeline, which will then build an actual resource based on the templates.
