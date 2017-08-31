Feature: Basic functionality
  Scenario: Obtain event and then check whether it was logged
     Given Container is running
      Then Check container logs for "3" received events
