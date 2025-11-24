# CraftbeerpIi4 Plugin to monitor Kettle and Fermenter Parameters

KettleSensor extends the graphical output in craftbeerpi4. Your You can add target temperatur and powerlevel to your Kettle analytics.
The Fermentersonsor will add target temperature to your analytics

## Installation

- sudo pip3 install cbpi4-KettleSensor

or

- sudo pip3 install https://github.com/avollkopf/cbpi4-KettleSensor/archive/main.zip

## Update

- sudo pip3 install --upgrade cbpi4-KettleSensor

or

- sudo pip3 install --upgrade https://github.com/avollkopf/cbpi4-KettleSensor/archive/main.zip

### Changelog:

- 24.11.25: (0.1.0) Add pyproject.tonl to support pip 25.3+
- 17.06.22: (0.0.6) Fix to transfer also float values for fermenter target temp (required for ramp to temp step)
- 27.01.22: (0.0.5) Bug fixed for kettle sensor
- 16.01.22: (0.0.4) Adaption for cbpi 4.0.1.2
- 12.01.22: (0.0.3) Bug Fixes + Fermenter Status (-1: cooling, 0: no actor active, 1: heating)
- 03.01.21: (0.0.2) Added FermenterSensor
