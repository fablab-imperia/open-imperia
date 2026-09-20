# Architettura

```text
                 OpenImperia
                     |
        +------------+------------+
        |                         |
       CKAN                   Collectors
        |                         |
        |                  +------+------+
        |                  |             |
        |               Source A      Source B
        |                  |             |
        +------ CKAN API --+-------------+
```

## Principi

1. I collector non accedono direttamente al database CKAN.
2. La pubblicazione avviene tramite Action API.
3. Ogni sorgente è una classe `DataSource`.
4. L'autodiscovery permette di aggiungere una sorgente creando un modulo Python.
5. I segreti non vengono committati.
