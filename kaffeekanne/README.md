
## Web UI

> Simple mobile-first web interface using [Ionic 2](http://ionicframework.com/docs/v2/getting-started/tutorial/)

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

```bash
cd platforms/browser/www
cf login
    > API Endpoint: https://api.eu-gb.bluemix.net
    > Username: ...
    > Password: ...
cf target -o kaffeekanne -s dev
cf push kaffeekanne1 -b https://github.com/cloudfoundry/staticfile-buildpack
```

The web application will be available at https://kaffeekanne1.eu-gb.mybluemix.net.
