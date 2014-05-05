===============================
PyToon
===============================

.. image:: https://badge.fury.io/py/pytoon.png
    :target: http://badge.fury.io/py/pytoon
    
.. image:: https://travis-ci.org/marcofinalist/pytoon.png?branch=master
        :target: https://travis-ci.org/marcofinalist/pytoon

.. image:: https://pypip.in/d/pytoon/badge.png
        :target: https://crate.io/packages/pytoon?version=latest


PyToon measures electricity, water and gas meters and creates fancy graphs

* Free software: BSD license
* Documentation: http://pytoon.rtfd.org.

Features
===============================

* Measures electricity, gas and water
* Detects usual and unusual energy consumption patterns
* Robust detection
* Insight into historical data
* Runs on Raspberry Pi
* Nice graphs
* Interfaces with Tinkerforge bricks and bricklets
* Hardware not included

Hardware
===============================

Raspberry Pi
-------------------------------


Core bricks
-------------------------------

Master Brick
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/masterbrick.jpg
    :alt: Master Brick 2.0
    :width: 300px

The master brick is the basis for the hardware. It has connection points for four bricklets and supplies power to the
whole stack. The bricklets are connected to the master brick through 1.5m long cables. These cables are shielded, but
this is not really necessary.

Ethernet Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/ethernet_extension.jpg
    :alt: Ethernet Extension (without PoE)
    :width: 300px

The ethernet brick sits on top of the master brick. I didn't want to connect the brick through USB with the Raspberry
Pi, because this would make programming and debugging a lot harder. With the Ethernet Extension, I can connect directly
 to the hardware even on my development machine. Without the Ethernet Extension, I would have to connect to the
 Raspberry Pi and then to the bricks.
 This setup also enables me to use the brick viewer program for simple testing.

Bricklets
-------------------------------

The sensors are the most important part of the hardware. I had to use three different types, because each meter uses
different indicators. For example, the gas meter uses a spinning magnet while the water meter uses a rotating dial.

Ambient Light Bricklet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/ambient_light_bricklet.jpg
    :alt: Ambient Light Bricklet
    :width: 300px

This was the trickiest sensor to get right. The electricity meter has a little diode or led that flashes every time a
Wh is consumed. When I first installed the ambient light bricklet and used the brick viewer to test it, it didn't seem
to work consistently. The graph of the viewer sometimes didn't show a spike when the diode flashed.
After a little testing I found that the problem was not in the bricklet, but in the graph. The graph updates every half
second or so. The illumination would go from 0 to 80 lux and back to zero in less time. These

Hall Effect Bricklet

.. image:: images/hall_effect_bricklet.jpg
    :alt: Hall Effect Bricklet
    :width: 300px

Line Bricklet

.. image:: images/line_bricklet.jpg
    :alt: Line Bricklet
    :width: 300px