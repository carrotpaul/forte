function buildRules() {
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

chrome.runtime.onInstalled.addListener(function() {
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules(buildRules());
  });
});
