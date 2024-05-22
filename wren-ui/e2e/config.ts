import fs from 'fs';
import path from 'path';
import { merge } from 'lodash';

export const testDbConfig = {
  client: 'better-sqlite3',
  connection: 'testdb.sqlite3',
  useNullAsDefault: true,
};

// Replace the default test config with your own e2e.config.json
const defaultTestConfig = {
  bigQuery: {
    projectId: 'wrenai',
    datasetId: 'wrenai.tpch_sf1',
    // The credential file should be under "wren-ui" folder
    credentialPath: 'bigquery-credential-path',
  },
  duckDb: {
    sqlCsvPath: 'https://duckdb.org/data/flights.csv',
  },
  postgreSql: {
    host: 'postgresql-host',
    port: '5432',
    username: 'postgresql-username',
    password: 'postgresql-password',
    database: 'postgresql-database',
    ssl: false,
  },
};

let userTestConfig = {};
try {
  userTestConfig =
    JSON.parse(
      fs.readFileSync(path.resolve(__dirname, 'e2e.config.json'), 'utf8'),
    ) || {};
} catch (_error: any) {
  console.log('No e2e config file found.');
}

export const getTestConfig = () => {
  return merge(defaultTestConfig, userTestConfig);
};
