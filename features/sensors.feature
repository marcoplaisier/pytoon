Feature: connect to sensors

  Scenario: connect to master brick
    Given we connect to the master brick
    Then we are connected

  Scenario: measure electricity with the ambient light sensor
    Given we have an electricity sensor
    Then we can measure electricity

  Scenario: disregard electricity measurements that are not pulses
    Given we have an electricty sensor
    And someone opens the door
    Then we disregard the measurements