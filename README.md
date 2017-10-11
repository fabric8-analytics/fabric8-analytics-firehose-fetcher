# Fabric8-Analytics Firehose Fetcher

The aim of this service is to listen [Libraries.io Firehose Stream](https://github.com/librariesio/firehose-stream) and based on events create new analyses.
* Note that currently it supports just plain reading of stream without any config.

## Contributing

See our [contributing guidelines](https://github.com/fabric8-analytics/common/blob/master/CONTRIBUTING.md) for more info.

## Known issues
From our experience firehose stream might be little bit unstable, which is causing various 
exceptions. These exceptions are about connectivity issues (InvalidRead or Timeout) and we 
decided to handle these exceptions by OpenShift by simply restarting container if some issue occurs.
