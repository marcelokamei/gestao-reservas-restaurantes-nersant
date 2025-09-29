# 🍽️ Sistema de Gestão de Restaurantes# 🍽️ Sistema de Gestão de Restaurantes



Sistema completo de gestão de restaurantes desenvolvido em Python com Streamlit, seguindo princípios de Programação Orientada a Objetos (POO) e utilizando SQLAlchemy como ORM.Sistema completo para gestão de restaurantes com **aplicações separadas** para clientes e administradores. Desenvolvido em Python com **Streamlit**, **SQLAlchemy** e **arquitectura limpa**. **Interface sem branding** e **login administrativo**.



## ✨ Funcionalidades## 🚀 Tecnologias Utilizadas



### 👤 **Área do Cliente**- **Python 3.8+**

- ✅ Registo e autenticação de clientes- **Streamlit** - Interface gráfica moderna e responsiva

- ✅ Visualização de restaurantes disponíveis- **SQLAlchemy** - ORM para persistência de dados

- ✅ Seleção de ambientes (Interior, Esplanada, Terraço)- **SQLite** - Banco de dados (configurável para PostgreSQL/MySQL)

- ✅ Reserva de mesas por data e horário- **Pandas** - Manipulação de dados para relatórios

- ✅ Gestão de reservas existentes- **Email-validator** - Validação de emails

- ✅ Interface intuitiva e responsiva- **Phonenumbers** - Validação de telefones



### 👨‍💼 **Área Administrativa**## ✨ Funcionalidades

- ✅ Dashboard com estatísticas completas

- ✅ Gestão de restaurantes### 👥 Área do Cliente

- ✅ Gestão de ambientes e mesas- ✅ Registo rápido com nome, email e telemóvel

- ✅ Gestão de reservas com filtros por período- ✅ Acesso simples por email

- ✅ Gestão de clientes- ✅ Visualização de restaurantes disponíveis

- ✅ Interface profissional com sidebar personalizada- ✅ Selecção de ambientes/salas por restaurante

- ✅ Pesquisa de mesas disponíveis por data/horário

## 🚀 **Como Executar**- ✅ Sistema de reservas intuitivo

- ✅ Visualização e cancelamento de reservas próprias

### Método 1: Script Automático

```bash### 🏢 Painel Administrativo

./start.sh- ✅ Dashboard com métricas em tempo real

```- ✅ CRUD completo de restaurantes

- ✅ Gestão de ambientes/salas por restaurante

### Método 2: Manual- ✅ Gestão de mesas com capacidade e observações

```bash- ✅ Visualização de todas as reservas

# Instalar dependências (primeira vez)- ✅ Gestão de clientes

python -m venv .venv- ✅ Relatórios avançados:

source .venv/bin/activate  # Linux/Mac  - Reservas por período

pip install -r requirements.txt  - Ocupação por restaurante

  - Clientes mais ativos

# Executar aplicação

python -m streamlit run app.py --server.port 8080## 🏗️ Arquitetura do Projeto

```

```

## 🌐 **Acesso**restaurant-management/

├── models/                 # 📊 Modelos de dados (POO)

- **URL**: http://localhost:8080│   └── __init__.py        # Entidades: Cliente, Restaurante, Ambiente, Mesa, Reserva

- **Cliente**: Registo livre ou login com email/telefone├── database/              # 🗄️ Camada de persistência

- **Admin**: Utilizador: `admin` | Senha: `admin123`│   ├── connection.py      # Configuração SQLAlchemy

│   ├── base_repository.py # Repositório base com CRUD genérico

## 🏗️ **Arquitetura**│   └── repositories.py    # Repositórios específicos

├── services/              # 🔧 Lógica de negócio

```│   └── __init__.py        # Serviços com validações e regras

├── app.py                 # Aplicação principal├── utils/                 # 📚 Biblioteca própria

├── config.py             # Configurações│   ├── validators.py      # Validações de dados

├── models/               # Modelos de dados (SQLAlchemy)│   └── streamlit_utils.py # Utilitários para UI

├── services/            # Lógica de negócio├── pages/                 # 🖥️ Interface do usuário

├── pages/               # Páginas da interface│   ├── client.py          # Área do cliente

├── database/            # Conexão e gestão da BD│   └── admin.py           # Painel administrativo

├── utils/               # Utilitários├── app.py                 # 🚀 Aplicação principal

└── requirements.txt     # Dependências├── config.py              # ⚙️ Configurações

```├── init_data.py           # 📝 Script para dados de exemplo



## 🛠️ **Tecnologias**```



- **Python 3.12+**## 🎯 Princípios Aplicados

- **Streamlit** - Interface web

- **SQLAlchemy** - ORM### Programação Orientada a Objetos (POO)

- **SQLite** - Base de dados- **Encapsulamento**: Métodos privados e validações internas

- **HTML/CSS** - Estilização personalizada- **Herança**: Repositório base para operações CRUD

- **Polimorfismo**: Interfaces comuns para diferentes entidades

- **Abstração**: Serviços abstraem complexidade da lógica de negócio

### Clean Architecture
- **Separação de responsabilidades**: Models, Services, Repositories
- **Inversão de dependência**: Serviços dependem de abstrações
- **Baixo acoplamento**: Módulos independentes e testáveis

### Validação de Dados

## 🎨 **Design**- **Biblioteca própria** com validadores reutilizáveis

- **Validação em tempo real** na interface

Interface profissional com:- **Sanitização** automática de dados de entrada

- Header personalizado com gradiente

- Elementos nativos do Streamlit ocultos## 🚀 Como Executar

- Sidebar customizada para admin

- Paleta de cores harmoniosa### Método 1: Script Automático (Recomendado)

- Experiência de utilizador otimizada

## 🚀 Como Executar

### Método 1: Script de Inicialização (Recomendado)
```bash
# Usar o script de inicialização
bash start.sh
```

### Método 2: Manual
```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env

# 4. (Opcional) Popular com dados de exemplo
python init_data.py

# 5. Executar aplicação
streamlit run app.py
```

## 📊 Dados de Exemplo

O sistema vem com um script que cria dados de exemplo:
- **1 restaurante** (Restaurante Bom Sabor)
- **1 ambiente** (Salão Principal)
- **10 mesas** com diferentes capacidades (4 ou 6 pessoas)
- **3 clientes** pré-cadastrados
- Reservas podem ser criadas através da interface



## 🎨 Interface Responsiva

- **CSS customizado** para aparência moderna
- **Cards interativos** para melhor UX
- **Layout responsivo** que se adapta a diferentes telas
- **Navegação intuitiva** com sidebar e tabs
- **Feedback visual** para todas as ações do usuário

## 📱 Recursos de UI/UX

- ✅ **Mensagens de feedback** (sucesso, erro, aviso, info)
- ✅ **Confirmações de ação** para operações críticas
- ✅ **Formulários validados** em tempo real
- ✅ **Tabelas interativas** com filtros
- ✅ **Cards visuais** para exibição de dados
- ✅ **Métricas em tempo real** no dashboard
- ✅ **Gráficos e relatórios** visuais

## 🔧 Configurações

### Banco de Dados
Por padrão usa SQLite, mas pode ser configurado para PostgreSQL ou MySQL através da variável `DATABASE_URL` no arquivo `.env`:

```env
# SQLite (padrão)
DATABASE_URL=sqlite:///restaurant_management.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/restaurant_db

# MySQL
DATABASE_URL=mysql://user:password@localhost/restaurant_db
```

### Horários de Funcionamento
Os horários disponíveis para reserva podem ser configurados em `config.py`:

```python
TIME_SLOTS = [
    "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
    "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"
]
```
