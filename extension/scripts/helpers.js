function buildActivationRules() {
  /* Youtube-DL supports A LOT of sites; I really only want a very small subset.
   * Scraping the supportedSites.md page seems more effort, so I'll just maintain
   * my own list in here.
   */
  var supportedSites = [
    'www.youtube.com',
    'www.soundcloud.com',
    'www.nicovideo.jp/'
  ];

  return supportedSites.map(function(site) {
    return {
      conditions: [
        new chrome.declarativeContent.PageStateMatcher({
          pageUrl: { hostEquals: site }
        })
      ],
      actions: [ new chrome.declarativeContent.ShowPageAction() ]
    }
  });
}

function sendDownloadRequest(currentTab) {
  var xhr = new XMLHttpRequest();

  xhr.open('POST', KAFKA_ENDPOINT);
  xhr.setRequestHeader('Content-Type', 'application/vnd.kafka.json.v2+json');
  xhr.setRequestHeader('Accept', 'application/vnd.kafka.v2+json');

  xhr.send(JSON.stringify({
    'records': [
      {'value': {'url': currentTab.url, 'auth_token': AUTH_TOKEN}}
    ]
  }));
}
