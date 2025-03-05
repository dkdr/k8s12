# Intro

A deployment of a simple python server which waits for first connection and terminates only when this connection is closed. This can be used to simulate a long-running connection on k8s cluster

# Usage

Deploy the app and connect to it. In separate terminal you can do things like update the app (example below) to deploy a new version and check what happens when you're holding the connection.

