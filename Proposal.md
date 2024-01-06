We plan to offer two versions of our webserver, which will be based on Flask (Python):

* The first version will be problem free and just display a (mostly) static text. It should however be evident, which pod is being accessed, e.g. by fetching the hostname.
* The second version will display the slightly altered information as the first (to check which version one is accessing), but will also feature problems randomly (e.g., 20% of the time, using a RNG) like 404 error-codes and long response times using sleep commands.

Initially, the first version will run on all pods, mimicking a normal, bugfree production environment.
Using canary releases in flagger, the pods will continuously be changed to version 2. By manually accessing the page many times, or by using the testing suite outlined in the flagger documentation, requests will be made and metrics for availability and performance will be generated. Using these metrics, Flagger can (automatically) rollback to the last stable version.

To install this setup, the package manager "helm" for Kubernetes will be used. For loadbalancing the NGINX-Ingress-Controller will be used, which will expose relevant metrics in the prometheus format, which is why the prometheus addon will also be required. By logging these metrics, one can inspect the system performance and even configure alarms (e.g., via Discord or other chat platforms) to react to issues faster.
