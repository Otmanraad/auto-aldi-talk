# Was ist dieses Projekt

Dieses Projekt soll automatisch 1 GB nachladen, immer wenn dein Guthaben unter den von ALDI-TALK festgelegten Schwellenwert fällt.

Ich habe es erstellt, weil ich es nervig fand, jedes Mal die App öffnen zu müssen, um 1 GB nachzuladen
also habe ich den Prozess automatisiert.

## Wie benutzt man dieses Projekt

Das Skript öffnet eine Chrome-Seite, auf der du dich in deinen Account einloggen musst.
Nach dem Login holt das Skript die Nutzerdaten von ALDI-TALK und speichert sie in user_data/.
```
python refill.py get
```

Das Skript extrahiert contractId, ResourceID usw. aus den Nutzerdaten, die mit ```python refill get``` geholt wurden.
```
python refill.py extract
```

Sobald deine Nutzerdaten verfügbar sind, wird 1 GB nachgeladen falls der Schwellenwert unter 1 GB liegt, passiert nichts.
```
python refill.py request.
```

Das ist der automatische Prozess.
Du brauchst einen Computer oder Server, der 24/7 läuft zum Beispiel kannst du einen Oracle Free Tier Server nutzen.
Dafür überträgst du deine user_data auf den Server und startest das Skript dort. 
Es überprüft ständig dein Guthaben und wartet eine bestimmte Zeit, bevor es erneut prüft. 
Sobald du weniger als den Schwellenwert hast, wird auto_request.py ausgeführt

```
python auto_check
```



## Getting Started

Auf Arch Linux (wenn du ein anderes System hast, installiere pip, python3 und git)
```
sudo pacman -S python python-pip git
```

Projekt klonen
```
git clone https://gitlab.com/raad.h.othman/auto-aldi-talk
```

In das Projektverzeichnis wechseln:
```
cd auto-aldi-talk
```

Create python envimorment(Umgebung) erstellen
```
python3 -m venv aldi-talk-venv
```

Umgebung aktivieren
```
source aldi-talk-venv/bin/activate
```

Python-Abhängigkeiten installieren
```
pip install -r requirements.txt
```

Playwright Browser installieren
```
playwright install
```


**Fertig**


## Mitwirkende

Ich selbst, ChatGPT, und ursprünglich hat mir Deepseek ein bisschen geholfen (auch wenn das die Sache erst mal nicht besser gemacht hat).
Aber nachdem ChatGPT-4 Plus rauskam, war es so gut, dass ich es nach pywebview gefragt habe, um meinen Code zu retten 
stattdessen hat es das ganze Projekt neu gemacht.
Ich hatte pywebview benutzt, aber es wollte einfach nicht so funktionieren, wie ich es wollte.
Also ein spezieller Dank an ChatGPT-4 etwa 50–60 % dieses Projekts stammen von ChatGPT-4, vielen Dank!


## Info

**übersetzt aus README.md**

Wenn du das Skript automatisch laufen lassen möchtest, ohne dich nochmal darum zu kümmern, kannst du Oracle Cloud Free Tier benutzen.
Es funktioniert problemlos auf dem kostenlosen x86 AMD Modell. Andere kostenlose oder kostenpflichtige Modelle kannst du natürlich auch verwenden ganz wie du möchtest.

Nur zur Info: ALDI-TALK ändert oft sein Backend, daher kann es sein, dass das Skript mal nicht funktioniert.
Dann warte einfach, bis ich es fixiere, oder eröffne ein Issue.

Du kannst das Projekt gern forken und Beiträge leisten. Vorschläge und Bug Reports sind willkommen. Vielen Dank fürs Benutzen meines Projekts! Vergiss nicht, einen Stern zu geben.