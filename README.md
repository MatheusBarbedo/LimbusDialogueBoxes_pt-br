# LIMBUSDIALOGUEBOXES_PT-BR

Tradução em **Português Brasileiro (PT-BR)** das caixas de diálogo de batalha de **Limbus Company**.

## Visão geral

Este projeto traduz para PT-BR os diálogos exibidos nas **speech bubbles** durante as batalhas de **Limbus Company**.

A base utilizada veio do projeto **LimbusDialogueBoxes_EN**, de **NotherWael**, que organiza e traduz essas falas para o inglês. A partir desse material, este repositório foi montado para gerar versões em **Português Brasileiro**, preservando a estrutura original dos arquivos JSON.

Atualmente o projeto trabalha com estes arquivos base:

- `BattleSpeechBubbleDlg.json`
- `BattleSpeechBubbleDlg_mowe.json`

Ambos possuem campos `dlg` que podem ser traduzidos para PT-BR.

---

## O que este projeto faz

- Traduz apenas os campos `dlg` dos arquivos JSON
- Mantém intactos os campos `id`, `desc` e a estrutura do arquivo
- Preserva tags e marcações especiais, como `<i>`, `<color>`, etc.
- Reaproveita traduções já existentes com base no campo `id`
- Traduz apenas **novos ids** que ainda não existem no arquivo de saída
- Registra logs específicos para auditoria do processo
- Mostra progresso no console em **batch**, no estilo do fluxo antigo

---

## Estrutura do projeto

```text
LimbusDialogueBoxes_pt-br/
├── original/
│   ├── BattleSpeechBubbleDlg.json
│   └── BattleSpeechBubbleDlg_mowe.json
├── traduzido/
├── logs/
├── src/
│   ├── app.py
│   ├── config.py
│   ├── incremental_service.py
│   ├── io_json.py
│   └── translator_service.py
├── tradutor.py
├── requirements.txt
└── README.md
```

### Pastas

- `original/`  
  Contém os arquivos JSON originais usados como entrada

- `traduzido/`  
  Contém os arquivos finais traduzidos em PT-BR

- `logs/`  
  Contém os logs gerados durante a execução

- `src/`  
  Contém os módulos separados por responsabilidade

---

## Como funciona

O script lê um arquivo JSON da pasta `original/` e procura os campos:

```json
"dlg": "..."
```

Somente esses campos são traduzidos para PT-BR.

Os demais campos, como `id`, `desc` e a estrutura do JSON, permanecem intactos.

### Fluxo incremental

1. O script abre o arquivo da pasta `original/`
2. Verifica se já existe um arquivo correspondente em `traduzido/`
3. Monta um mapa por `id` com base no arquivo já traduzido
4. Para cada item do arquivo original:
   - se o `id` já existe no traduzido, reaproveita o `dlg`
   - se o `id` é novo, coloca o item na fila de tradução
   - se não houver `id`, coloca o item na fila de tradução direta
5. A fila de tradução é processada em **batch**
6. O resultado final é salvo em `traduzido/`

Assim, quando novos diálogos forem adicionados ao arquivo original, você não precisa retraduzir tudo do zero.

---

## Fluxo de logs

Durante a execução, o projeto gera os seguintes arquivos dentro da pasta `logs/`:

### 1. Log principal

```text
logs/tradutor.log
```

Contém exceções, warnings e informações técnicas do processo.

### 2. Log de novos ids traduzidos

```text
logs/BattleSpeechBubbleDlg_novos_ids_traduzidos.txt
logs/BattleSpeechBubbleDlg_mowe_novos_ids_traduzidos.txt
```

Contém um `id` por linha para cada item novo traduzido naquela execução.

### 3. Log de itens sem id traduzidos diretamente

```text
logs/BattleSpeechBubbleDlg_itens_sem_id_traduzidos.jsonl
logs/BattleSpeechBubbleDlg_mowe_itens_sem_id_traduzidos.jsonl
```

Cada linha contém um JSON com:

- índice do item
- `desc`
- `original_dlg`
- `translated_dlg`

---

## Progresso no console

Durante a execução, o script mostra o progresso em **batch**, em vez de item por item.

Exemplo:

```text
Total de itens no arquivo original: 1633
Total de itens pendentes para tradução: 10
Total de ids reaproveitados: 1623
Processando em 1 batch(s) de até 200 itens cada.

[batch 1/1] Traduzindo itens pendentes 0 até 9...
   -> batch concluído (10 itens)

Concluído.
```

Esse formato mantém a ideia do fluxo antigo, mas aplicado apenas aos itens realmente pendentes na execução incremental.

---

## Pré-requisitos

Antes de executar o projeto, você precisa ter instalado:

- **Python 3.10+** recomendado
- **pip**

Dependência Python:

- `deep-translator`

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/MatheusBarbedo/LimbusDialogueBoxes_pt-br.git
cd LimbusDialogueBoxes_pt-br
```

Instale a dependência:

```bash
py -m pip install -r requirements.txt
```

ou:

```bash
py -m pip install deep-translator
```

---

## Como rodar

O projeto trabalha com **um arquivo por vez**.

No arquivo `src/config.py`, ajuste:

```python
INPUT_FILE = "BattleSpeechBubbleDlg.json"
```

ou:

```python
INPUT_FILE = "BattleSpeechBubbleDlg_mowe.json"
```

Você também pode ajustar o tamanho do batch:

```python
BATCH_SIZE = 200
```

Depois execute:

```bash
py tradutor.py
```

---

## Passo a passo

### 1. Coloque os arquivos originais na pasta `original/`

Estrutura esperada:

```text
original/
├── BattleSpeechBubbleDlg.json
└── BattleSpeechBubbleDlg_mowe.json
```

### 2. Abra o projeto no terminal

Exemplo no PowerShell:

```powershell
cd C:\caminho\para\LimbusDialogueBoxes_pt-br
```

### 3. Instale as dependências

```bash
py -m pip install -r requirements.txt
```

### 4. Escolha o arquivo que deseja traduzir

No `src/config.py`, altere `INPUT_FILE`:

```python
INPUT_FILE = "BattleSpeechBubbleDlg.json"
```

ou:

```python
INPUT_FILE = "BattleSpeechBubbleDlg_mowe.json"
```

### 5. Ajuste o batch, se quiser

No `src/config.py`:

```python
BATCH_SIZE = 200
```

### 6. Execute o script

```bash
py tradutor.py
```

### 7. Verifique o resultado

O arquivo final será salvo em:

```text
traduzido/BattleSpeechBubbleDlg.json
```

ou:

```text
traduzido/BattleSpeechBubbleDlg_mowe.json
```

---

## Observação importante sobre atualizações

Se você adicionar novos itens ao arquivo da pasta `original/`, basta rodar o script novamente.

Ele irá:

- reaproveitar os `ids` já traduzidos
- traduzir apenas os novos `ids`
- registrar esses novos `ids` no log correspondente
- agrupar o trabalho em batch no console

---

## Revisão da tradução

Como parte do conteúdo foi gerada com auxílio de tradução automática, algumas linhas ainda podem precisar de:

- ajustes de contexto
- adaptação de tom
- revisão gramatical
- padronização de termos do universo de Limbus Company

---

## Status

🚧 Projeto em andamento.

O objetivo é complementar o trabalho já feito pela comunidade em PT-BR, trazendo também a tradução das caixas de diálogo de batalha que ainda não haviam sido cobertas.

---

## Créditos

Este projeto utiliza como base o trabalho original de:

**NotherWael**  
Projeto: **LimbusDialogueBoxes_EN**  
Link: [https://github.com/NotherWael/LimbusDialogueBoxes_EN](https://github.com/NotherWael/LimbusDialogueBoxes_EN)

Todos os créditos pela versão original em inglês e pela organização do material-base pertencem ao autor do projeto acima.

---

## Aviso

Projeto feito por fã, sem fins lucrativos, voltado para a comunidade.

**Limbus Company** e seus conteúdos pertencem aos seus respectivos proprietários.