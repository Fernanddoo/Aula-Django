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

Neste ponto, iremos começar a construir um e-commerce.

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

## Vamos fazer um CRUD!

### O que é um CRUD??

CRUD é um acrônimo em inglês para as quatro operações básicas utilizadas em bancos de dados relacionais e na maioria das aplicações web:

- Create (Criar): A função de adicionar novos registros ou dados.

- Read (Ler): A função de ler, consultar ou visualizar os dados existentes.

- Update (Atualizar): A função de editar ou modificar um registro que já existe.

- Delete (Deletar): A função de remover um registro do banco de dados.

Resumindo, um CRUD é o conjunto de funcionalidades essenciais para gerenciar os dados de uma aplicação. Quase todo sistema que você usa, de uma rede social a um e-commerce, é, em sua essência, uma série de operações CRUD mais complexas.

## Vamos criar nossa página principal!

### Passo 1: Definir o modelo

Vamos definir o modelo dos produtos que aparecerão na nossa loja online!

Abra o arquivo **models** no app loja e vamos colar o seguinte código:

```python
# loja/models.py
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
```

## O que fizemos aqui?

- Criamos uma classe Produto que herda de models.Model.

- Definimos três campos: nome (texto), preco (número decimal) e descricao (texto longo, opcional).

- O método __str__ é uma representação em texto do objeto, útil para o painel de administração do Django.

Agora, precisamos aplicar essa alteração ao banco de dados. No seu terminal, execute:

```bash
python manage.py makemigrations loja
python manage.py migrate
```

### Passo 2: Criar as URLs

As URLs definem quais "endereços" do nosso site levarão a quais funções (views) do nosso código.

Primeiro, vamos criar um arquivo de URLs para o nosso app loja. Crie o arquivo **loja/urls.py**:

```python
# loja/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página principal que lista os produtos (Read)
    path('', views.lista_produtos, name='lista_produtos'),

    # Rota para o formulário de adicionar um novo produto (Create)
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),

    # Rota para editar um produto existente (Update)
    path('editar/<int:pk>/', views.editar_produto, name='editar_produto'),

    # Rota para excluir um produto (Delete)
    path('excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),
]
```

Agora, precisamos conectar essas URLs do app loja às URLs principais do projeto. Abra o arquivo urls.py do seu projeto principal (o que fica ao lado do settings.py) e inclua as URLs da loja:

```python
# urls.py do projeto
from django.contrib import admin
from django.urls import path, include # Adicione 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Qualquer acesso à rota '/' será gerenciado pelo app 'loja'
    path('', include('loja.urls')),
]
```

### Passo 3: Criar as Views

As views contêm a lógica principal da nossa aplicação. Elas recebem uma requisição da web e retornam uma resposta.

Abra o arquivo loja/views.py e adicione o seguinte:

```python
# loja/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm

# Read (Ler)
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/lista_produtos.html', {'produtos': produtos})

# Create (Criar)
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'loja/produto_form.html', {'form': form})

# Update (Atualizar)
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'loja/produto_form.html', {'form': form})

# Delete (Deletar)
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    return render(request, 'loja/produto_confirm_delete.html', {'produto': produto})
```

Perceba que importamos um ProdutoForm. Formulários no Django ajudam a validar e a lidar com dados de entrada de forma segura. Vamos criá-lo.

### Passo 4: Criar o formulário

Crie um novo arquivo em loja, chamado: **forms.py**

```python
# loja/forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'descricao']
```

- ModelForm é uma classe mágica do Django que cria um formulário automaticamente a partir de um modelo. É muito prático!

### Passo 5: Criar os Templates!!!

Os templates são os arquivos HTML que o usuário final verá. Crie uma pasta templates dentro do seu app loja, e dentro dela, outra pasta chamada loja. A estrutura ficará assim: loja/templates/loja/.

1. lista_produtos.html (A página principal, o "R" de Read):

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Nossa Loja</title>
</head>
<body>
    <h1>Produtos da Loja</h1>
    <a href="{% url 'adicionar_produto' %}">Adicionar Novo Produto</a>
    <hr>
    <ul>
        {% for produto in produtos %}
            <li>
                <strong>{{ produto.nome }}</strong> - R$ {{ produto.preco }}
                <p>{{ produto.descricao|default:"Sem descrição." }}</p>
                <a href="{% url 'editar_produto' pk=produto.pk %}">Editar</a> |
                <a href="{% url 'excluir_produto' pk=produto.pk %}">Excluir</a>
            </li>
            <br>
        {% empty %}
            <li>Nenhum produto cadastrado ainda.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

2. produto_form.html (Formulário para Criar e Editar - "C" e "U"):

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Formulário de Produto</title>
</head>
<body>
    <h1>{% if form.instance.pk %}Editar Produto{% else %}Adicionar Produto{% endif %}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
    </form>
    <br>
    <a href="{% url 'lista_produtos' %}">Voltar para a lista</a>
</body>
</html>
```

- {% csrf_token %} é uma tag de segurança essencial do Django para prevenir ataques.

- {{ form.as_p }} renderiza os campos do formulário (nome, preço, descrição) como parágrafos.

3. produto_confirm_delete.html (Tela de confirmação para deletar - "D"):

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Confirmar Exclusão</title>
</head>
<body>
    <h1>Confirmar Exclusão</h1>
    <p>Você tem certeza que deseja excluir o produto "{{ produto.nome }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Sim, excluir</button>
        <a href="{% url 'lista_produtos' %}">Cancelar</a>
    </form>
</body>
</html>
```

### Passo 6: Vamos melhorar nossa interface!

Para evitar repetir o mesmo código de cabeçalho e rodapé em todas as páginas, a melhor prática é criar um template base que os outros irão "herdar".

1. No seu diretório loja/templates/loja/, crie um novo arquivo chamado base.html.

2. Cole o seguinte código nesse arquivo:

```html
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-g">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Minha Loja{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="{% url 'lista_produtos' %}">Loja Django</a>
    </div>
  </nav>

  <main class="container mt-4">
    {% block content %}
    {% endblock %}
  </main>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
```

## O que fizemos aqui??

- Criamos uma estrutura HTML padrão.

- Adicionamos os links do CSS e do JavaScript do Bootstrap via CDN.

- Criamos uma barra de navegação (navbar) simples no topo.

- Definimos uma área principal com a classe container do Bootstrap, que centraliza e adiciona margens ao conteúdo.

- O mais importante: {% block content %}. Esta é uma "marcação" que diz ao Django: "as páginas filhas que herdarem de mim poderão inserir seu conteúdo específico aqui".

### Agora vamos atualizar os outros arquivos

Substitua todo o conteúdo de loja/templates/loja/lista_produtos.html pelo seguinte:

```html
{% extends 'loja/base.html' %}

{% block title %}Lista de Produtos{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h1>Produtos da Loja</h1>
    <a href="{% url 'adicionar_produto' %}" class="btn btn-primary">Adicionar Novo Produto</a>
</div>
<hr>

{% if produtos %}
<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>Nome</th>
            <th>Preço</th>
            <th>Descrição</th>
            <th>Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for produto in produtos %}
        <tr>
            <td>{{ produto.nome }}</td>
            <td>R$ {{ produto.preco }}</td>
            <td>{{ produto.descricao|default:"-" }}</td>
            <td>
                <a href="{% url 'editar_produto' pk=produto.pk %}" class="btn btn-secondary btn-sm">Editar</a>
                <a href="{% url 'excluir_produto' pk=produto.pk %}" class="btn btn-danger btn-sm">Excluir</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<div class="alert alert-warning" role="alert">
    Nenhum produto cadastrado ainda.
</div>
{% endif %}
{% endblock %}
```

Principais mudanças:

- **{% extends 'loja/base.html' %}:** Informa ao Django para usar nosso novo template base.

- Todo o conteúdo está dentro de **{% block content %}.**

- Usamos uma ```html<table class="table table-striped">``` para uma listagem muito mais organizada.

- Os links de "Adicionar", "Editar" e "Excluir" agora são botões estilizados (btn, btn-primary, btn-danger, etc.).

- A mensagem de "nenhum produto" agora é um alert do Bootstrap, mais destacado.

Substitua todo o conteúdo de loja/templates/loja/produto_form.html pelo seguinte:

```html
{% extends 'loja/base.html' %}

{% block title %}{% if form.instance.pk %}Editar Produto{% else %}Adicionar Produto{% endif %}{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h2 class="card-title">
            {% if form.instance.pk %}Editar Produto{% else %}Adicionar Produto{% endif %}
        </h2>
    </div>
    <div class="card-body">
        <form method="post">
            {% csrf_token %}

            <div class="mb-3">
                <label for="{{ form.nome.id_for_label }}" class="form-label">Nome</label>
                <input type="text" name="{{ form.nome.name }}" id="{{ form.nome.id_for_label }}" class="form-control" value="{{ form.nome.value|default_if_none:'' }}" required>
            </div>
            <div class="mb-3">
                <label for="{{ form.preco.id_for_label }}" class="form-label">Preço</label>
                <input type="number" step="0.01" name="{{ form.preco.name }}" id="{{ form.preco.id_for_label }}" class="form-control" value="{{ form.preco.value|default_if_none:'' }}" required>
            </div>
            <div class="mb-3">
                <label for="{{ form.descricao.id_for_label }}" class="form-label">Descrição</label>
                <textarea name="{{ form.descricao.name }}" id="{{ form.descricao.id_for_label }}" class="form-control" rows="3">{{ form.descricao.value|default_if_none:'' }}</textarea>
            </div>

            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="{% url 'lista_produtos' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

Principais mudanças:

- A página agora herda de base.html.

- Envolvemos o formulário em um componente card do Bootstrap para um visual mais limpo.

- **Importante:** Em vez de usar {{ form.as_p }}, renderizamos cada campo manualmente. Isso nos permite adicionar a classe form-control aos inputs e form-label às labels, que é a forma como o Bootstrap estiliza formulários.

- Os botões de "Salvar" e "Cancelar" também foram estilizados.

Por fim, a tela de confirmação de exclusão.

Substitua todo o conteúdo de loja/templates/loja/produto_confirm_delete.html pelo seguinte:

```html
{% extends 'loja/base.html' %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="card border-danger">
    <div class="card-header bg-danger text-white">
        <h2 class="card-title">Confirmar Exclusão</h2>
    </div>
    <div class="card-body">
        <p>Você tem certeza que deseja excluir o produto <strong>"{{ produto.nome }}"</strong>?</p>
        <p>Esta ação não poderá ser desfeita.</p>

        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Sim, tenho certeza</button>
            <a href="{% url 'lista_produtos' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

Principais mudanças:

- Herda de base.html.

- Usa um card com borda e cabeçalho vermelhos (border-danger, bg-danger) para sinalizar visualmente que esta é uma ação destrutiva.

- Os botões foram estilizados para refletir as ações (vermelho para confirmar a exclusão, cinza para cancelar).

E com isso, caros, criamos um e-commerce em Django!!!! (Super básico)

## Continuando onde paramos (provavelmente vai dar erro de versão das bibliotecas)

### Importante!

- Provavelmente a nossa VENV deve ter sido apagado, então, criem novamente antes de seguir adiante!!!

Vamos utilizar o git para clonar o repositório e continuar de onde paramos n última aula, usando o seguinte comando:

```bash
    git clone https://github.com/Fernanddoo/Aula-Django.git
```

E depois acessem o diretório do projeto:

```bash
    cd .\aulaDjango\
```

Depois de estar no diretório correto, há apenas uns comandos que restam para estarmos com o projeto rodando novamente
Mas antes de rodar o requirements, vamos abri-lo e colar isto:

```txt
asgiref==3.7.2
Django==2.2.1
dotenv==0.9.9
python-dotenv==0.21.1
sqlparse==0.4.4
tzdata==2025.2
```

- Execute os seguintes comando:

```bash
    pip install -r  requirements.txt   
```

- E depois:

```bash
    python manage.py migrate
```

E após isso feito, rodamos o projeto novamente!

```bash
    python manage.py runserver
```

## Vamos atualizar ainda mais nossa loja

### Passo 1

Vamos também adicionar imagens para nossos produtos, para termos mais visual em nossa página de e-commerce

Vamos começar atualizando o modelo dos produtos, parece ser armazenado o link das imagens que pegaremos da web:

O arquivo **loja/models.py** vai ficar assim:

```python
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    imagem_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome
```

### Importante!!!

Como nós alteramos nosso modelo do produto, lembrem!!! Precisamos passar novamente essa mudança para o banco de dados entender o que foi alterado no nosso modelo produto

- Vamos executar novamente os dois comandos:

```bash
    python manage.py makemigrations
    python manage.py migrate
```

### Passo 2

Também precisamos atualizar nosso forms, que é onde nós inserimos as informações do produto que cadastramos.

- Vamos copiar o seguinte código:

```python
    # loja/forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'descricao', 'imagem_url']
```

Notem que até o momento, tanto no model, quanto no forms, apenas adicionamos um campo a mais, isso se dá, pois o que estamos fazendo é apenas atribuir mais uma variável dentre as outras no nosso modelo Produto.

### Passo 3

Agora teremos que renderizar essa nova alteração em nossas telas, aqui estarão a maior parte das nossas mudanças.

- **loja/templates/loja/lista_produtos.html**

```html
<thead class="table-dark">
    <tr>
        <th>Imagem</th> <th>Nome</th>
        <th>Preço</th>
        <th>Descrição</th>
        <th>Ações</th>
    </tr>
</thead>
```

Nesta parte do arquivo, vamos inserimos a tag <th>Imagem<th> para onde irá aparecer nossa imagem.

E agora dentro do loop, outra alteração:

```html
<tbody>
    {% for produto in produtos %}
    <tr>
        <td>
            {% if produto.imagem_url %}
                <img src="{{ produto.imagem_url }}" alt="{{ produto.nome }}" style="width: 100px; height: auto; border-radius: 8px;">
            {% else %}
                <span class="text-muted">Sem Imagem</span>
            {% endif %}
        </td>
        <td>{{ produto.nome }}</td>
        <td>R$ {{ produto.preco }}</td>
        <td>{{ produto.descricao|default:"-" }}</td>
        <td>
            <a href="{% url 'editar_produto' pk=produto.pk %}" class="btn btn-secondary btn-sm">Editar</a>
            <a href="{% url 'excluir_produto' pk=produto.pk %}" class="btn btn-danger btn-sm">Excluir</a>
        </td>
    </tr>
    {% endfor %}
</tbody>
```

Com isso, nossa renderização dos produtos está completa, só falta agora, nossa tela do forms também estar de acordo com as mudanças

- Vamos colocar o seguinte código:

```html
<div class="mb-3">
    <label for="{{ form.imagem_url.id_for_label }}" class="form-label">URL da Imagem</label>
    <input type="url" name="{{ form.imagem_url.name }}" id="{{ form.imagem_url.id_for_label }}" class="form-control" value="{{ form.imagem_url.value|default_if_none:'' }}">
</div>
```

Os inserimos junto dos outros campos dentro da tag <form> no arquivo html

E com isso, podemos rodar novamente o projeto e verificar nossas mudanças!!!

E com isso, nosso e-commerce vai crescendo mais e mais... Mas o que falta??? 

- Login/Cadastro de usuários
- Carrinho de compras
- Search bar

Entre outros mais, mas... Hora do Desafio!

## Dê-em a sua cara para o projeto!

Vamos reforçar o que aprendemos com html e css e tentar aplicar isso ao projeto do django também!

O projeto está utilizando a estilização do [Bootstrap](https://getbootstrap.com.br/docs/4.1/getting-started/introduction)

Clicando no link, vocês tem acesso a documentação do Bootstrap e utilizar a estilização própria dele. (Ela é mais difícil de personalizar, mas possuí muitas opções prontas para utilizar)

### OU

Vocês podem remover o bootstrap e trabalhar com o html e css puro!



