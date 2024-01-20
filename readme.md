# Setup instructions
## Helm
Helm is the package manager of our choice for kubernetes. It can be retrieved from https://github.com/helm/helm/releases. Additionally, https://helm.sh/docs/intro/install/ can be consulted for further instructions.
An environment variable pointing to the path of the executables is advised.

## Install NGINX Ingress
The first step in our case was to setup an ingress server. To do this, the corresponding helm repository has to be added.

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
```

For the sake of clarity, everything is created inside the namespace "test".

```
kubectl create ns test
```

Then, install NGINX inside said namespace, with metrics enabled and setup for prometheus logging.
```
helm upgrade -i ingress-nginx ingress-nginx/ingress-nginx --namespace test --set controller.metrics.enabled=true --set controller.podAnnotations."prometheus\.io/scrape"=true --set controller.podAnnotations."prometheus\.io/port"=10254
```
## Install Flagger and Prometheus
Again, add the relevant repo for flagger to helm.
```
helm repo add flagger https://flagger.app
```
In order to get the new configuration files working, the custom resource definitions need to be fetched and applied:
```
kubectl apply -f https://raw.githubusercontent.com/fluxcd/flagger/main/artifacts/flagger/crd.yaml
```

The following statement installs both flagger and prometheus and configures relevant settings, so that relevant generated metrics are also written to prometheus, and that NGINX is set as the Meshprovider.
```
helm upgrade -i flagger flagger/flagger --namespace test --set prometheus.install=true --set meshProvider=nginx --set metricsServer=http://flagger-prometheus:9090
```

## Configure Ingress
The following command sets up the ingress, so that in the following steps, traffic is routed to our deployment called "podinfo" that contains a webservice.

```
kubectl apply -f ingress.yaml
```

## Setup Deployment
The following command fetches the kubernetes configuration files from the creators of flagger and uses them to create said deployment.
```
kubectl apply -k https://github.com/fluxcd/flagger//kustomize/podinfo?ref=main
```

## Alerts
When canary releases fail, it might be necessary to act fast. This is why alerts can be configured, which send a message to, e.g., a slack or MS Teams channel. In our case, due to simplicity, a discord webhook was created and the necessary resources were applied:
```
kubectl apply -f alert.yaml
```

## Canary deployment
First, before initializing a canary release, a loadtesting environment, that has a horizontal scaling feature based on the required load, is set up.
```
helm upgrade -i flagger-loadtester flagger/loadtester --namespace=test
```

Since the default metric did not work in our case, we opted for a custom prometheus query that checks the latency (time that the website needs to load). This needs to be applied first:
```
kubectl apply -f latencyMetric.yaml
```

Then, a canary configuration is created. Before executing, the last line needs to be altered to contain the external IP adress of the ingress controller, so that the loadtesting service can reach the webpage.
This does not yet start a transition for our deployment, but create necessary services and new deployments and waits for a change in the docker image.
```
kubectl apply -f canary.yaml
```

### Good deployment
At this point, after creation of the necessary services and after transitioning from the "podinfo" to the "podinfo-primary" deployment, the webpage should be available through the external IP of the ingress.

After the webpage is available, by changing the docker image inside the configuration, the canary release is initiated.
```
kubectl -n test set image deployment/podinfo podinfod=ghcr.io/stefanprodan/podinfo:6.0.1
```

The current status, warning messages and other information can be retrieved by the following command:
```
kubectl -n test describe canary/podinfo
```

### Bad deployment
In another step, another image is applied, that makes it possible for us to see a rollback:
```
kubectl -n test set image deployment/podinfo podinfod=ghcr.io/stefanprodan/podinfo:6.0.3
```

To have the rollback take effect, we now simulate traffic that takes long to execute. To do this, the following command is executed in WSL/Ubuntu:
```
watch curl http://<ingress-url>/delay/5
```

## Lessons learned
 * Watch out when it comes to namespaces! If you have two resources in different namespaces, you might not see your changes and ask yourself why. This cost us some time to find out!
 * Also regarding namespaces: If your services can't be reached by other resources, it's probably due to namespaces as well.
 * When it comes to complex setups like canary releases, where additional deployments and services are created automatically, it's necessary to have an overview of how everything plays together first. We've been trying to circumvent using a DNS (since one seemed to be required for the Ingress), when in reality the only necessary thing is the service name, and that would be created later by the canary resource!
 * Sometimes resources are buggy. Just delete them, and re-apply the configurations. Don't waste your time.
 * When it comes to canary releases and metrics, it's detrimental to know what is currently primary, and what falls under canary services/deployments. If you select the wrong metrics/resources, your application won't work as expected!

# Research
This webpage gives a good overview about the different components of flagger:
https://docs.flagger.app/usage/how-it-works

The following guides were used to get the project working:
 * https://docs.flagger.app/install/flagger-install-on-kubernetes#install-flagger-with-helm​
 * https://docs.flagger.app/usage/alerting​
 * https://docs.flagger.app/tutorials/nginx-progressive-delivery​
 * https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks


