import requests


test_data = {
  "pages" : [ {
    "components" : [ {
      "id" : 14,
      "alias" : "HEADER",
      "title" : "Header"
    }, {
      "id" : 1,
      "metadata" : {
        "type" : "DATA",
        "granularity" : "QUARTER",
        "presentation" : "TABLE"
      },
      "alias" : "SUMMARY_GLOBAL_WITH_TREND",
      "title" : "Summary Global, with trend."
    }, {
      "id" : 2,
      "metadata" : {
        "type" : "DATA",
        "granularity" : "DAY",
        "presentation" : "TABLE"
      },
      "alias" : "SUMMARY_REGIONAL_WITH_TREND",
      "title" : "Summary Regional, with trend."
    } ]
  }],
  "name" : "testPost1",
  "description" : "Template",
  "startDate" : "2017-01-01T00:00:00",
  "endDate" : "2017-12-31T23:59:59",
  "defaultGranularity" : "WEEK",
  "timePeriod" : "LAST_QUARTER",
  "pageType" : "LETTER",
  "pageLayout" : "LANDSCAPE"
}


def test_home():
    "GET request to url returns a 200"
    url = 'https://cap-gateway-release.app.dev.cap.nectarcorp.com/rapi/templates'
    resp = requests.get(url)
    assert resp.status_code == 200
