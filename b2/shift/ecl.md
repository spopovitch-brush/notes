# ECL Shift

Lanciare `cisco AnyConnect Secure Mobility Client`. 
```
Server: kekvpn.kek.jp
Password: {Authenticator} + 1100
```

Lanciare su Powershell
```bash
ssh -L 8013:eclpc13:80 -L 5900:eclpc14:5900 gaudino@bdaq.local.kek.jp -i .\.ssh\id_rsa_bdaq
Password: 11001100
Password bdaq: AkiraSalemme11_3006
```


Open [http://localhost:8013/](http://localhost:8013/) in your browser.

Password per VNC: `kagome0`

After shift: [elog](https://elog.belle2.org/elog/ECL+operation/)

Esempi di logs:
 ```txt
 03/11/2025
**ECL OWL 1 - Shift Report**
ECL is stable, no issues.

Null runs during all the shift
 ```
