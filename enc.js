const EthCrypto = require('eth-crypto');

function eccEnc() {
  const publicKey = EthCrypto.publicKeyByPrivateKey(
    '0x107be946709e41b7895eea9f2dacf998a0a9124acbb786f0fd1a826101581a07'
  );


  EthCrypto.encryptWithPublicKey(
    publicKey, // publicKey
    '0123456789abcdef' // message
  ).then(encrypted => {
    const strCipher = EthCrypto.cipher.stringify(encrypted);
    console.log(strCipher, strCipher.length);
  });



}

eccEnc();

