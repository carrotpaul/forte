// Add rules to enable the extension for supported sites only
chrome.runtime.onInstalled.addListener(function() {
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules(buildActivationRules());
  });
});

// Listen to when someone clicks on the extension
chrome.pageAction.onClicked.addListener(function(tab) {
  sendDownloadRequest(tab);
});
