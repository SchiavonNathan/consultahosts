# ConsultaHosts

Este projeto realiza a consulta de estatísticas de hosts cadastrados em um servidor Zabbix via API.

## Funcionalidades
- Conecta à API do Zabbix usando credenciais definidas em um arquivo `.env`.
- Exibe estatísticas gerais de hosts (total, online, offline).
- Exibe estatísticas detalhadas por grupo de hosts.

## Requisitos
- Python3
- Instalar dependências com:
  ```bash
  pip install -r requirements.txt
  ```
- Criar um arquivo `.env` na mesma pasta do `main.py` com as variáveis:
  ```env
  ZABBIX_SERVER=https://seu-servidor-zabbix
  ZABBIX_USER=seu_usuario
  ZABBIX_PASSWORD=sua_senha
  ```

## Execução
Execute o script principal:
```bash
python main.py
```
Exemplo de retorno:
```bash
--- Estatísticas Gerais ---
Total de Hosts Cadastrados: 194
Hosts Online (Disponíveis): 188
Hosts Offline (Indisponíveis): 6

--- Detalhes por Grupo ---
- Grupo1 (Total: 100)
  Online:  98
  Offline: 2
- Grupo2 (Total: 94)
  Online:  90
  Offline: 4
```

## Observações
- Certifique-se de que o arquivo `.env` está correto e na mesma pasta do script.
- O script ignora a verificação SSL da sessão Zabbix.

## Licença
Este projeto é apenas para fins educacionais e internos.
