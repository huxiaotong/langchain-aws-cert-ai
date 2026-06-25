from __future__ import annotations

from aws_cdk import CfnOutput, Duration, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from constructs import Construct


class AwsCertAiStack(Stack):
    """CDK stack that deploys the LangChain API to ECS Fargate."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        project_name: str,
        container_port: int,
        bedrock_model_id: str,
        bedrock_knowledge_base_id: str,
        **kwargs,
    ) -> None:
        """Create networking, container, load balancer, logs, and Bedrock IAM access."""

        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            nat_gateways=1,
        )

        repository = ecr.Repository(
            self,
            "Repository",
            repository_name=project_name,
            image_scan_on_push=True,
        )

        cluster = ecs.Cluster(
            self,
            "Cluster",
            cluster_name=project_name,
            vpc=vpc,
        )

        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            cpu=1024,
            memory_limit_mib=2048,
        )

        task_definition.task_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream",
                    "bedrock:Retrieve",
                    "bedrock:RetrieveAndGenerate",
                ],
                resources=["*"],
            )
        )

        log_group = logs.LogGroup(
            self,
            "LogGroup",
            log_group_name=f"/ecs/{project_name}",
            retention=logs.RetentionDays.ONE_MONTH,
        )

        container = task_definition.add_container(
            "AppContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository, tag="latest"),
            logging=ecs.LogDrivers.aws_logs(stream_prefix=project_name, log_group=log_group),
            environment={
                "APP_ENV": "aws",
                "LLM_PROVIDER": "bedrock",
                "RAG_PROVIDER": "bedrock_kb",
                "BEDROCK_MODEL_ID": bedrock_model_id,
                "BEDROCK_KNOWLEDGE_BASE_ID": bedrock_knowledge_base_id,
                "AWS_REGION": self.region,
            },
            health_check=ecs.HealthCheck(
                command=[
                    "CMD-SHELL",
                    f"python -c \"import urllib.request; urllib.request.urlopen('http://localhost:{container_port}/health')\"",
                ],
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                retries=3,
            ),
        )
        container.add_port_mappings(ecs.PortMapping(container_port=container_port))

        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "Service",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
            desired_count=1,
            listener_port=80,
        )

        service.target_group.configure_health_check(path="/health")

        CfnOutput(self, "RepositoryUri", value=repository.repository_uri)
        CfnOutput(self, "ServiceUrl", value=f"http://{service.load_balancer.load_balancer_dns_name}")
