# zokrates_examples

```
// Hash : sha3

// key avaliability
// key: 128bit
hash(keykey) == hashedKeykey
Hash(key) == hashedKey
Enc(key, keykey) = encryptedKey  

// ownership
// address: 160bit, datahash, 256bit
```

zokrates: https://zokrates.github.io/gettingstarted.html

```sh
# compile
zokrates compile -i root.zok
# perform the setup phase
zokrates setup
# execute the program
zokrates compute-witness -a 337 113569
# generate a proof of computation
zokrates generate-proof
# export a solidity verifier
zokrates export-verifier
```



