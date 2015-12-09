Feature: connect to sensors

  Scenario: connect to master brick
    Given we connect to the master brick
    Then we are connected

  Scenario: measure light intensity with the ambient light sensor
    Given we connect to the master brick
    When we have a electricity sensor
    Then we can measure electricity