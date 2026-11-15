---
name: plano-de-estudo
description: >-
  Use quando o usuário pedir um plano de estudo, plano de ensino, trilha ou
  curso sobre qualquer tema (para ele mesmo ou para ensinar um grupo),
  especialmente com vídeos do YouTube.
---
# Plano de estudo / ensino com vídeos

Monta um plano prático em sessões, com um vídeo real do YouTube por tópico, entregue como uma Page (Canvas).

## 1. Entender o pedido (sem formulário)
Tire do contexto ou pergunte só o que faltar, uma coisa por vez:
- **Tema** e, se houver, produto/versão específica.
- **Público**: quem vai estudar e o nível atual.
- **Objetivo**: o que a pessoa deve saber fazer no fim.
- **Formato**: quantas sessões e quanto tempo cada (padrão: 4 a 6 sessões de ~50 min).
- **Idioma dos vídeos** (padrão: o idioma do usuário; aceitar inglês com legendas quando faltar conteúdo).
- **Contexto do usuário** (empresa, área, setor) para personalizar exemplos.
Se o pedido já tiver o suficiente, não pergunte nada e comece.

## 2. Pesquisar (em segundo plano, por um executor)
- Confirme os fatos atuais do tema em fontes oficiais. Registre a data da checagem.
- Busque vídeos REAIS no YouTube por tópico: primeiro canais oficiais no idioma pedido, depois criadores confiáveis no idioma, depois oficiais em inglês (marcar "em inglês, legendas").
- Valide cada vídeo pelo oEmbed `https://www.youtube.com/oembed?url=<URL>&format=json` (confirma título e canal). Descarte o que falhar. Nunca invente vídeos, títulos ou canais.

## 3. Estrutura do plano
Para cada sessão: título e objetivo; conceitos-chave na linguagem do público; vídeo(s) com título, canal, link, idioma e por que assistir; atividade prática; pergunta de verificação ou entregável curto.
Incluir também: visão geral da trilha, casos de uso por área/perfil quando for um grupo, cuidados (segurança, governança, limitações) quando o tema pedir, e uma biblioteca de vídeos com a contagem por idioma.

## 4. Entrega
- Escreva como Page (skill `canvas`) e mande no chat só uma ou duas linhas com o link.
- Diga quantos vídeos estão no idioma pedido e quantos em outro.
- Ofereça um próximo passo útil (roteiro de demos, quiz, slides, material de apoio).

## 5. Ajustes
Pedidos de mudança editam a mesma Page em vez de criar outra.
