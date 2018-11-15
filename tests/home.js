module.exports = {
  afterEach: (client, done) => client.globals.report(client, done),

  // Check heading
  heading: (client) => {
    client
      .url(client.launch_url)
      .waitForElementVisible('body', 10000)
      .assert.containsText("h1", "Welcome to CKAN")
      .end();

  },
};
