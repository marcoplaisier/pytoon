===============================
PyToon
===============================

.. image:: https://badge.fury.io/py/pytoon.png
    :target: http://badge.fury.io/py/pytoon
    
.. image:: https://travis-ci.org/marcofinalist/pytoon.png?branch=master
        :target: https://travis-ci.org/marcofinalist/pytoon

<<<<<<< HEAD
.. image:: https://landscape.io/github/marcofinalist/pytoon/master/landscape.png
   :target: https://landscape.io/github/marcofinalist/pytoon/master
   :alt: Code Health

PyToon measures electricity, water and gas meters and creates fancy graphs
=======
.. image:: https://pypip.in/d/pytoon/badge.png
        :target: https://crate.io/packages/pytoon?version=latest

PyToon measures electricity, water and gas consumption and gives you the ability to monitor your energy and water usage
every second of every day.
Most hardware available on the market today costs at least € 200,-. You may even need to enter into an new contract with
an energy supplier. And even then it can't even measure your water consumption! PyToon will measure your water
consumption, your data is safe inside your home network, and it will only set you back € 120,- but you do need to
install it yourself.
>>>>>>> electricity

* Free software: BSD license
* Documentation: http://pytoon.rtfd.org.

Features
===============================

* Measure and view realtime electricity, gas and water consumption
* Detect usual and unusual consumption patterns
* Great insight into historical data
* Tinkering, extend and control your setup and data
* Use hardware from Tinkerforge and the Raspberry Pi foundation

Hardware
===============================
PyToon is based on open off-the-shelf hardware. It uses hardware from
.. _Tinkerforge: http://www.tinkerforge.com/
and a .. _Raspberry Pi: http://www.raspberrypi.org/.

Raspberry Pi
-------------------------------

The Raspberry Pi is the central control unit. It analyses energy and water consumption and creates insight into your
consumption patterns.

Flask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flask is the web application stack used to generate the mobile website.

Measurement hardware
-------------------------------

All measurement is done by bricklets from .. _Tinkerforge: http://www.tinkerforge.com/. Together with the master brick
and Ethernet extension brick, the bricklets provide a robust, cheap and extensible method for creating hardware systems.

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

The ethernet brick sits on top of the master brick. It is also possible to connect the master brick directly through USB
with the Raspberry Pi. However, this would make programming and debugging a lot harder. With the Ethernet Extension, it
is possible to connect directly to the hardware through your network. You can put the Raspberry Pi anywhere with an
(wired) connection.

Sensors (bricklets)
-------------------------------

The sensors are the most important part of the hardware. PyToon uses three different types, because each meter uses
different indicators. For example, the gas meter uses a spinning magnet while the water meter uses a rotating reflective
dial.

Ambient Light Bricklet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/ambient_light_bricklet.jpg
    :alt: Ambient Light Bricklet
    :width: 300px

This was the trickiest sensor to get right. The electricity meter has a little diode or led that flashes every time a
Wh is consumed. When I first installed the ambient light bricklet and used the brick viewer to test it, it didn't seem
to work consistently. The graph of the viewer sometimes didn't show a spike when the diode flashed.
After a little testing I found that the problem was not in the bricklet, but in the graph. The graph updates every half
second or so. The illumination would go from 0 to 80 lux and back to zero in less time and the spikes did not show in
the graph.
Fortunately, the bricklet does register the brief flash.

Hall Effect Bricklet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/hall_effect_bricklet.jpg
    :alt: Hall Effect Bricklet
    :width: 300px

The Hall Effect bricklet is used to measure gas consumption. The rotary dial in the gas meter has a magnet connect to
the least significant digit. Every revolution this magnet passes the bricklet and thanks to the .. _Hall effect:
http://en.wikipedia.org/wiki/Hall_effect it is possible to measure each revolution

Line Bricklet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/line_bricklet.jpg
    :alt: Line Bricklet
    :width: 300px

The water meter has a little rotating dial that is partly reflective. A line bricklet is used to detect whether the dial
is rotating or not.
