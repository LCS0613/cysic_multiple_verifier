# cysic_multiple_verifier
Shell scripts for build multiple cysic verifier(for Linux)

## 1. Modify wallet_address.yaml
- Set multiple EVM addresses in the wallet_address.yaml file.
```python
wallets:
  - name: wallet1
    wallet_address: 0x~
  - name: wallet2
    wallet_address: 0x~
  ...
```
## 2. Build multiple cysic-verifier instances
- Each verifier will be created in a folder named cysic-verifier-{wallet_name} and will start in a screen session named {wallet_name}.
```python
bash setting.sh
```
