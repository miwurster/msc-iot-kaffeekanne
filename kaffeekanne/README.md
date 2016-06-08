
## Web UI

> Simple mobile-first web interface using [Ionic](http://ionicframework.com/docs/v2/getting-started/tutorial/).

The web application is running as Cloud Foundry application on IBM Bluemix.

It is available at https://kaffeekanne1.eu-gb.mybluemix.net.

![Dashboard](http://rawgit.com/miwurster/msc-iot-kaffeekanne/master/webapp-dashboard.png)

### Requirements

```bash
npm install -g ionic cordova
```

### Build the App

```bash
ionic add platform browser
ionic build browser
```

### Deploy the App

We are using a Cloud Foundry [buildpack](https://github.com/cloudfoundry/staticfile-buildpack) for static sites in order to simply serve our built artifacts:

```bash
cd platforms/browser/www
cf login
    > API Endpoint: https://api.eu-gb.bluemix.net
    > Username: ...
    > Password: ...
cf target -o kaffeekanne -s prod
cf push kaffeekanne1 -b https://github.com/cloudfoundry/staticfile-buildpack
```
