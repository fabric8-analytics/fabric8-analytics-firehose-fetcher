Feature: Basic functionality

  Scenario: Obtain event and then check whether it was logged
     Given Container is running
      when Got three Firehose events
      then Check container logs for received events
