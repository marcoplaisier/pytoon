Features
===================

Measuring
-------------------

We need a way to determine gas, water and electricity consumption and store this in a database. Unfortunately, we cannot
just read the values from the display. Well, we could but that is not expensive, consumes quite a lot of power and needs
advanced OCR techniques. Instead we use a couple of simple sensors. These sensors measure magnetic fields and
reflectivity which results in a square type graph.
Then, it is quite simple to look at a rising or falling flank and use that as a measurement. This results in a timestamp
which we can store in a database.


Storage
-------------------

After getting a timestamp, we just store the timestamp in a database. We use a table per measurement type (i.e. gas,
electricity, water). This will make it easier to query and aggregate specific types of consumption.


Calculation
-------------------

TODO