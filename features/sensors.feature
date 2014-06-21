Feature: connect to sensors

  Scenario: connect to master brick
    Given we connect to the master brick
    Then we are connected

  Scenario: measure electricity with the ambient light sensor
    Given we connect to the master brick
    When we have a electricity sensor
    Then we can measure electricity
    And we store the electricity measurements in the database

  Scenario: measure gas with Hall effect sensor
    Given we connect to the master brick
    When we have a gas sensor
    Then we can measure gas
    And we store the gas measurements in the database