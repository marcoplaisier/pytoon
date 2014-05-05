Feature: connect to sensors

  Scenario: connect to master brick
    Given we connect to the master brick
    Then we can find all sensors connect to the master brick