Feature: connect to sensors

  Scenario: connect to master brick
    Given we connect to the master brick
<<<<<<< HEAD
    Then we are connected
=======
    Then we are connected

  Scenario: measure electricity with the ambient light sensor
    Given we connect to the master brick
    When we have an electricity sensor
    Then we can measure electricity
    And we store the electricity measurements in the database
>>>>>>> electricity
