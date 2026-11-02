# Sprint 5.1 — CDK Packaging + AWS Marketplace + Metering

> **Slice**: v5.0 · **Duration**: Weeks 17–18 · **Story Points**: 34

## Goal

Package the entire platform as a deployable CDK application, pass the AWS FTR audit, list on AWS Marketplace, and implement SaaS usage metering.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-13.1.1](../user-stories/13-deployment-and-aws-marketplace/README.md#us-1311-cdk-infrastructure-stack-packaging) | Deployment | 13 | CDK stack packaging |
| P0 | [US-13.1.2](../user-stories/13-deployment-and-aws-marketplace/README.md#us-1312-aws-marketplace-listing--ftr-compliance) | Deployment | 13 | FTR compliance + listing |
| P0 | [US-13.1.3](../user-stories/13-deployment-and-aws-marketplace/README.md#us-1313-saas-metering--usage-based-billing) | Deployment | 8 | SaaS metering |

## Key Deliverables

- Single `cdk deploy --all` deploys entire platform
- FTR self-assessment passes all checks
- Quick Start CloudFormation template published
- Hourly metering reports to AWS Marketplace
- Free / Standard / Enterprise pricing tiers configured

## Definition of Done

- [ ] `cdk deploy` works in clean AWS account
- [ ] `cdk destroy` cleanly removes all resources
- [ ] FTR checklist 100% compliant
- [ ] Metering data appears in AWS Marketplace console
- [ ] Free tier limits enforced correctly
