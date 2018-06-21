# Rancherpai

## Sobre
  <p align="justify">O Rancherpai é uma biblioteca em python para permitir o controle e monitoramento da ferramenta de orquestração de container Rancher atravéz de bots, de forma a permitir maior conforto, autonomia e agilidade ao se trabalhar com a infraestrutura operacional de projetos grandes de software </p>

## Instalação
  Nesta seção está descrito cada passo necessário para a configuração e utilização da aplicação.

#### Pré-requisitos
  * [Git](https://git-scm.com/)
  * [Docker](https://www.docker.com/get-docker)
  * Uma instancia do Rancher
  * Um grupo no slack

  #### Configuração

  Clone o repositório no diretório desejado
  ```bash
  git clone https://github.com/arthur0496/Rancherpai.git
  ```

  Crie seu bot user no slack

  Utilize o seguinte comando para criar uma imagem da sua aplicaçãos
  ```bash
  docker build -t rancherpai /caminho_para_o_repositorio/.
  ```

  Utilize o seguinte comando para subir um container da aplicação
  ```bash
  docker run rancherpai
  ```
  Insira as seguintes variaveis dentro do container(da forma que achar melhora):
    - SLACK_BOT_TOKEN= o tokken do bot criado por você
    - RANCHER_ACCESS_KEY= a chave de acesso da sua instancia do Rancher
    - RANCHER_SECRET_KEY= a chave secreta da sua instancia do Rancher
    - RANCHER_URL= a url da sua instancia do Rancher


## Licença
 [MIT](https://github.com/arthur0496/Rancherpai/blob/master/LICENSE)
