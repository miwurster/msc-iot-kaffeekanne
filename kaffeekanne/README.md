
## Web UI

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
cf push kaffeekanne -b https://github.com/cloudfoundry/staticfile-buildpack
```
