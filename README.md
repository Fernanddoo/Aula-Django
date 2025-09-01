# Criando seu E-commerce no Django!!!

- Para começar, vamos criar um ambiente virtual:

```bash
    python -m venv venv
```

O ambiente virtual vai ter uma cópia do python e todas as bibliotecas que você instalar.

## Ativando a sua venv

- Se for Windows:
```bash
    .\venv\Scripts\activate
```
- Se for Linux:
```bash
    source venv/bin/activate
```

## Criando o projeto django

- Vamos conferir a instalação do django:

```bash
    django-admin --version
```

- Caso não estiver instalado:

```bash
    pip install django
```

E agora só falta nos criarmos um projeto django, para isso utilizamos o **django-admin** em nosso terminal.

- Execute o seguinte comando:

```bash
    django-admin startproject <qualquer_nome>
```

Com isso estamos pronto para começar, mas...

## O que é o Django?

Ele é um Framework Web Python. Vamos quebrar esse termo:

- **Framework:** É uma estrutura de trabalho, um conjunto de ferramentas, regras e componentes prontos que organizam e aceleram o desenvolvimento. Em vez de começar do zero, você começa com uma base sólida e testada.

- **Web:**  É feito especificamente para construir coisas para a internet, como sites, APIs e aplicações complexas.

- **Python:** É escrito e utilizado na linguagem de programação Python, que é conhecida por sua clareza e simplicidade.

Em resumo, Django é uma ferramenta que cuida de todas as partes repetitivas e complicadas de construir um site, permitindo que você, o desenvolvedor, foque na lógica e nas funcionalidades únicas do seu projeto.

Dito isso, vamos continuar:

## Criando um app no Django

Neste ponto, iremos começar a construir no e-commerce.

- Para isso, vamos rodar o seguinte comando para criar um "app":

```bash
    python manage.py startapp loja
```

Feito isso, só falta uma etapa que precisamos fazer antes de colocar no projeto para funcionar e essa etapa seria realizar nossas migrations.

### O que são migrations?

Pense nas migrations como um sistema de controle de versão (como o Git) para a estrutura do seu banco de dados.

Elas são arquivos Python que o Django gera automaticamente. Cada arquivo descreve um conjunto de mudanças que precisam ser aplicadas ao banco de dados para que ele corresponda ao estado atual dos seus arquivos models.py.

Em vez de alterar o banco de dados diretamente, você altera seu código Python (models.py) e o Django descobre quais alterações são necessárias e escreve o "roteiro" (a migration) para aplicá-las.

### E como funciona na prática?

- O trabalho com migrations se resume a dois comandos principais e sequenciais:

```bash
    python manage.py makemigrations
    python manage.py migrate
```

Com isso o django irá olhar para nossas models, gerar os arquivos necessários para planejar as mudanças e depois com o **migrate** ele executa essas mudanças e as sobe para o nosso banco de dados, alterando a estrutura de forma segura.

E chegando agora no finalmente, vamos colocar o projeto para funcionar...

## Colocando nosso projeto para funcionar!

- E o último comando será:

```bash
    python manage.py runserver
```

Feito isso, nosso projeto irá rodar em nosso localhost da máquina em que está instalado e podemos clicar no terminal no endereço retornado ou abrir nosso navegador e acessar:

```
    localhost:8000
```

E com isso podemos criar no e-commerce!