# Usa a imagem base do Node.js
FROM node:22-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta 4200 (porta padrão do Angular CLI)
EXPOSE 4200

# Comando para rodar o servidor de desenvolvimento do Angular
CMD ["npx", "ng", "serve", "--host", "0.0.0.0"]