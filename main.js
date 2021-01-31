const { initialize } = require('zokrates-js/node');
const fs = require('fs');

initialize().then((zokratesProvider) => {
  const proof = JSON.parse(fs.readFileSync('./proof.json', 'utf-8'));
  console.log(JSON.parse(proof));
});