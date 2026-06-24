# AWS 核心认证知识样例

## 高可用与多可用区

Multi-AZ 是 AWS 认证题中常见的高可用关键词。对于 Amazon RDS，Multi-AZ 部署会在不同可用区维护同步备用实例，主要用于故障转移和提高可用性，不用于读扩展。读扩展通常使用 Read Replica。

## 弹性与解耦

Amazon SQS 用于消息队列和异步解耦。Amazon SNS 用于发布订阅和扇出。EventBridge 常用于事件驱动集成和 SaaS/AWS 服务事件路由。

## 存储选择

Amazon S3 适合对象存储、静态网站、备份、日志和数据湖。EBS 是块存储，通常挂载到 EC2。EFS 是托管 NFS 文件系统，支持多个 EC2 实例共享访问。

## 网络

Security Group 是有状态的实例级虚拟防火墙。Network ACL 是无状态的子网级访问控制。NAT Gateway 让私有子网实例访问互联网，但不允许互联网主动访问私有实例。

## 数据库

DynamoDB 是托管 NoSQL 键值和文档数据库，适合低延迟和自动扩展场景。RDS 适合关系型数据库。Aurora 是兼容 MySQL/PostgreSQL 的云原生关系型数据库。
