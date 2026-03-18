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
├── temp/
├── BattleSpeechBubbleDlg.json
├── BattleSpeechBubbleDlg_mowe.json
├── README.md
└── tradutor.py
```

### Arquivos principais

- `BattleSpeechBubbleDlg.json`  
  Arquivo base com diálogos de batalha para tradução

- `BattleSpeechBubbleDlg_mowe.json`  
  Arquivo base com diálogos de batalha para tradução

- `tradutor.py`  
  Script responsável por traduzir os diálogos e gerar os arquivos finais

- `temp/`  
  Pasta usada para salvar os blocos temporários durante o processamento

---

## Como funciona

O script lê um arquivo JSON e procura os campos:

```json
"dlg": "..."
```

Somente esses campos são traduzidos para PT-BR.

Os demais campos, como `id`, `desc` e a estrutura do JSON, permanecem intactos.

### Fluxo do processamento

1. O script abre o arquivo JSON configurado na variavel INPUT_FILE
2. Lê a lista `dataList`
3. Divide o conteúdo em blocos
4. Traduz apenas os textos do campo `dlg`
5. Salva os blocos traduzidos dentro da pasta `temp/`
6. Junta todos os blocos ao final
7. Gera um novo arquivo JSON em PT-BR

Essa abordagem é útil para arquivos grandes, porque se o processo for interrompido, os blocos já concluídos continuam salvos.

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

O script atual trabalha com um arquivo por vez.

No `tradutor.py`, ajuste as variáveis no topo do arquivo para definir qual JSON será traduzido.

### Exemplo para `BattleSpeechBubbleDlg.json`

```python
INPUT_FILE = "BattleSpeechBubbleDlg.json"
OUTPUT_FILE = "BattleSpeechBubbleDlg_ptbr.json"
```

Depois execute:

```bash
python tradutor.py
```

### Exemplo para `BattleSpeechBubbleDlg_mowe.json`

```python
INPUT_FILE = "BattleSpeechBubbleDlg_mowe.json"
OUTPUT_FILE = "BattleSpeechBubbleDlg_mowe_ptbr.json"
```

Depois execute novamente:

```bash
python tradutor.py
```

---

## Passo a passo

### 1. Abra o projeto no terminal

Exemplo no PowerShell:

```powershell
cd C:\caminho\para\LimbusDialogueBoxes_pt-br
```

### 2. Instale a dependência

```bash
pip install deep-translator
```

### 3. Escolha o arquivo que deseja traduzir

No topo do `tradutor.py`, ajuste `INPUT_FILE` e `OUTPUT_FILE`.

### 4. Execute o script

```bash
python tradutor.py
```

### 5. Aguarde o processamento

Durante a execução, o script pode:

- criar a pasta `temp/`, se necessário
- gerar arquivos temporários por bloco
- traduzir apenas os campos `dlg`
- consolidar o resultado em um arquivo final

### 6. Verifique o arquivo gerado

Ao final, você terá um arquivo como:

```text
BattleSpeechBubbleDlg_ptbr.json
```

ou

```text
BattleSpeechBubbleDlg_mowe_ptbr.json
```

dependendo do arquivo configurado.

---

## Retomando uma execução interrompida

Como o processamento é feito em blocos, se a execução for interrompida, basta rodar novamente o script.

Os arquivos já gerados na pasta `temp/` podem ser reaproveitados, evitando retrabalho.

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

## Aviso

Projeto feito por fã, sem fins lucrativos, voltado para a comunidade.

**Limbus Company** e seus conteúdos pertencem aos seus respectivos proprietários.