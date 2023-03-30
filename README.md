# New Relic NerdGraph Interactions
This repository contains Python code to interact with the New Relic NerdGraph API. This is a work-in-progress, and I hope to add new features and functionality over time to help New Relic users more easily interact with NerdGraph in more meaningful ways.

## Requirements
A New Relic User API Key is required to run these queries. User API Key permissions are inherited from the New Relic user permissions from the user that created the key. Please review the [New Relic Docs](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/#user-key) for more information.

The following packages are required to run this code:
- requests
- os
- json
- logging
- dotenv

## .env
This project is set up to leverage a `.env` file for storing your New Relic User API Key and account number, which are represented by the following variables:
- NEW_RELIC_API_KEY (used by APIHandler)
- ACCOUNT_ID (used by APMQueryHandler)
