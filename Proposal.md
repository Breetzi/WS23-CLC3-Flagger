
Wir hätten es so konzipiert, dass wir zwei Versionen des Webservers (Flask) anbieten:
* erste Version läuft Problemlos und zeigt einfach einen statischen Text an
* zweite Version wirft ab und zu (z.B. jeder 5te Request) einen schlechten Status-Code (404...), oder braucht länger um die Anfragen zu bearbeiten, z.B. durch sleep Commands. Dieser Version zeigt für Kontroll-Zwecke einen leicht anderen Text an.


Die erste Version läuft zu Beginn auf den Pods, und wird dann durch Canary Releases & Flagger kontinuierlich von der neuen Version ausgetauscht.
Da die neue Version Probleme macht soll automatisch ein Rollback auf die erste Version durchgeführt werden. 
Für die Installation/Konfiguration davon, wird der Package Manager "helm" für Kubernetes verwendet.
Als Ingress-Controller könnte NGINX verwendet werden.
Durch Logging und Alarme könnte man auf relevante Performance-Metriken zugreifen, bzw. die Reaktion auf Probleme verbessern.
