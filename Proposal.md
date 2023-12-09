
Wir hätten es so konzipiert, dass wir zwei Versionen des Webservers (Flask) anbieten:
* erstere wirft ab und zu (z.B. jeder 5te Request) einen schlechten Status-Code (404...), oder braucht länger um die Anfragen zu bearbeiten, z.B. durch sleep Commands.
* zweitere Version, hat diese Probleme nicht mehr und zusätzlich (zur Kontrolle) wird ein anderer Text angezeigt.

Die erste Version läuft zu Beginn auf den Pods, und wird dann durch Canary Releases & Flagger kontinuierlich von der neuen Version ausgetauscht.
Für die Installation/Konfiguration davon, wird der Package Manager "helm" für Kubernetes verwendet.
Als Ingress-Controller könnte NGINX verwendet werden.
Durch Logging und Alarme könnte man auf relevante Performance-Metriken zugreifen, bzw. die Reaktion auf Probleme verbessern.
