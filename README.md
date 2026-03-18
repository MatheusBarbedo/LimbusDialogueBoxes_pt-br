# LIMBUSDIALOGUEBOXES_PT-BR

Tradução em **Português Brasileiro (PT-BR)** das caixas de diálogo de batalha de **Limbus Company**.

## Visão geral

Este projeto foi criado para traduzir para PT-BR os diálogos exibidos nas **speech bubbles** durante as batalhas de **Limbus Company**.

A base utilizada veio do projeto **LimbusDialogueBoxes_EN**, de **NotherWael**, que organiza e traduz essas falas para o inglês. A partir desse material, este repositório foi montado para gerar versões em **Português Brasileiro**, preservando a estrutura original dos arquivos JSON.

Atualmente o projeto trabalha com estes arquivos base:

- `BattleSpeechBubbleDlg.json`
- `BattleSpeechBubbleDlg_mowe.json`

Ambos possuem campos `dlg` que podem ser traduzidos para PT-BR.

---

## Créditos

Este projeto utiliza como base o trabalho original de:

**NotherWael**  
Projeto: **LimbusDialogueBoxes_EN**  
Link: [https://github.com/NotherWael/LimbusDialogueBoxes_EN](https://github.com/NotherWael/LimbusDialogueBoxes_EN)

Todos os créditos pela versão original em inglês e pela organização do material-base pertencem ao autor do projeto acima.

---

## O que este projeto faz

- Traduz apenas os campos `dlg` dos arquivos JSON
- Mantém intactos os campos `id`, `desc` e a estrutura do arquivo
- Preserva tags e marcações especiais, como `<i>`, `<color>`, etc.
- Processa arquivos grandes em blocos para evitar perda de progresso
- Gera arquivos finais consolidados em PT-BR

---

## Estrutura do projeto

```text
LIMBUSDIALOGUEBOXES_PT-BR/
├── original/
│   ├── BattleSpeechBubbleDlg.json
│   └── BattleSpeechBubbleDlg_mowe.json
├── traduzido/
├── temp/
├── README.md
└── tradutor.py
```

### Pastas

- `original/`  
  Contém os arquivos JSON originais que serão usados como entrada

- `traduzido/`  
  Contém os arquivos finais traduzidos em PT-BR

- `temp/`  
  Contém os chunks temporários gerados durante o processamento

### Arquivos principais

- `tradutor.py`  
  Script responsável por traduzir os diálogos e gerar os arquivos finais

- `README.md`  
  Documentação do projeto

---

## Como funciona

O script lê um arquivo JSON da pasta `original/` e procura os campos:

```json
"dlg": "..."
```

Somente esses campos são traduzidos para PT-BR.

Os demais campos, como `id`, `desc` e a estrutura do JSON, permanecem intactos.

### Fluxo do processamento

1. O script abre o arquivo JSON configurado na pasta `original/`
2. Lê a lista `dataList`
3. Divide o conteúdo em blocos
4. Traduz apenas os textos do campo `dlg`
5. Salva os blocos traduzidos dentro da pasta `temp/`
6. Junta todos os blocos ao final
7. Gera um novo arquivo JSON em PT-BR na pasta `traduzido/`

Essa abordagem é útil para arquivos grandes, porque se o processo for interrompido, os blocos já concluídos continuam salvos.

---

## Convenção dos arquivos gerados

### Arquivos temporários

Os chunks temporários são gerados com o nome do arquivo base, sem a extensão:

```text
temp/chunk_BattleSpeechBubbleDlg_0001.json
temp/chunk_BattleSpeechBubbleDlg_0002.json
temp/chunk_BattleSpeechBubbleDlg_mowe_0001.json
temp/chunk_BattleSpeechBubbleDlg_mowe_0002.json
```

### Arquivos finais

Os arquivos traduzidos são gerados na pasta `traduzido/`:

```text
traduzido/BattleSpeechBubbleDlg.json
traduzido/BattleSpeechBubbleDlg_mowe.json
```

---

## Pré-requisitos

Antes de executar o projeto, você precisa ter instalado:

- **Python 3.10+** recomendado
- **pip**
- Dependência Python:
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
pip install deep-translator
```

---

## Como rodar

O script atual trabalha com **um arquivo por vez**.

No `tradutor.py`, ajuste a variável `INPUT_FILE` no topo do arquivo para definir qual JSON será traduzido.

### Exemplo para `BattleSpeechBubbleDlg.json`

```python
INPUT_FILE = "BattleSpeechBubbleDlg.json"
```

Depois execute:

```bash
python tradutor.py
```

O script vai ler:

```text
original/BattleSpeechBubbleDlg.json
```

E gerar:

```text
traduzido/BattleSpeechBubbleDlg.json
```

### Exemplo para `BattleSpeechBubbleDlg_mowe.json`

```python
INPUT_FILE = "BattleSpeechBubbleDlg_mowe.json"
```

Depois execute novamente:

```bash
python tradutor.py
```

O script vai ler:

```text
original/BattleSpeechBubbleDlg_mowe.json
```

E gerar:

```text
traduzido/BattleSpeechBubbleDlg_mowe.json
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

### 3. Instale a dependência

```bash
pip install deep-translator
```

### 4. Escolha o arquivo que deseja traduzir

No topo do `tradutor.py`, ajuste:

```python
INPUT_FILE = "BattleSpeechBubbleDlg.json"
```

ou

```python
INPUT_FILE = "BattleSpeechBubbleDlg_mowe.json"
```

### 5. Execute o script

```bash
python tradutor.py
```

### 6. Aguarde o processamento

Durante a execução, o script irá:

- criar a pasta `traduzido/`, se necessário
- criar a pasta `temp/`, se necessário
- gerar arquivos temporários por bloco
- traduzir apenas os campos `dlg`
- consolidar o resultado em um arquivo final

### 7. Verifique o arquivo gerado

O resultado final ficará na pasta `traduzido/`.

Exemplos:

```text
traduzido/BattleSpeechBubbleDlg.json
traduzido/BattleSpeechBubbleDlg_mowe.json
```

---

## Retomando uma execução interrompida

Como o processamento é feito em blocos, se a execução for interrompida, basta rodar novamente o script.

Os arquivos já gerados na pasta `temp/` podem ser reaproveitados, evitando retrabalho.

Como os chunks agora incluem o nome do arquivo base, é possível traduzir arquivos diferentes sem misturar os blocos temporários.

---

## Logs e revisão

O script gera um arquivo de log chamado:

```text
tradutor.log
```

Esse log pode ajudar a identificar falhas de tradução ou valores inesperados durante a execução.

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

## Aviso

Projeto feito por fã, sem fins lucrativos, voltado para a comunidade.

**Limbus Company** e seus conteúdos pertencem aos seus respectivos proprietários.
