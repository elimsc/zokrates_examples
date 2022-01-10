```sh
zokrates compile -i enc_hash.zok
zokrates setup
cat mid.json | zokrates compute-witness --abi --stdin

zokrates generate-proof
zokrates verify
```

setup: 1.970s
generate-proof: 0.452s
verify: 0.018s
