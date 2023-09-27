# Prometheus

Prometheus is a monitoring system which consist of several components. The main one is a prometheus server which is responsible for data retrieval, data storing, querying and alerting. However, alert routing is usually done by Alertmanager. Prometheus server also ships with a simple Web UI. 

# Prometheus operator

To make the deployment of prometheus easy we'll use prometheus operator, which is a tool to simplify deployment of prometheus. It allows us not only to deploy prometheus instance, but it will also help us to manage it.

# Kube-prometheus-stack

We're talking about prometheus, prometheus-operator, and now we're at kube-prometheus-stack. This is a collection of tools which is suitable to deploying full stack kubernetes cluster monitoring. It implements simple way to deploy prometheus-operator, which deploys prometheus itself, but also has built-in grafana and some nice grafana dashboards.

Enough theory, lets deploy it!

# Deployment

In OKD/OpenShift Prometheus Operator is already deployed and needs to be enabled for users as described in [documentation](https://docs.okd.io/4.13/monitoring/enabling-monitoring-for-user-defined-projects.html#enabling-monitoring-for-user-defined-projects_enabling-monitoring-for-user-defined-projects).
