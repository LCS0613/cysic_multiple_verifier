# cysic_multiple_verifier
Shell scripts for build multiple cysic verifier(for Linux)

## 1. Modify wallet_address.yaml
- Set multiple EVM address in "wallet_address.yaml"
```python
wallets:
  - name: wallet1
    wallet_address: 0x~
  - name: wallet2
    wallet_address: 0x~
  ...
```
## 2. Build multiple cysic-verifier
- Each verifier will create in "cysic-verifier-{wallet name}" and start in screen "{walle_name}"
```python
bash setting.sh
```
