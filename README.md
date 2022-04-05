# Controlador de volume por gestos da mão usando Python

Este projeto é sobre utilizar camera para controlar o volume em tempo real com o uso de bibliotecas em python: openCV, mediapipe e Pycall

**Assunto abordado:** Visão Computacional

## Introdução

O reconhecimento de gestos ajuda os computadores a entender a linguagem do corpo humano. Isso ajuda a construir um vínculo mais potente entre humanos e máquinas, em vez de apenas as interfaces de usuário de texto básicas ou interfaces gráficas de usuário (GUIs). Neste projeto de reconhecimento de gestos, os movimentos do corpo humano são lidos pela câmera do computador. O computador então usa esses dados como entrada para lidar com o aplicativo. 

## Cenário

+ Detectar as mãos usando mediapipe
+ Detectar a localização das pontas dos dedos indicador e polegar
+ Se os dedos indicador e polegar estiverem distantes um do outro aumentar o volume
+ Se os dedos indicador e polegar estiverem encostados um no outro diminuir o volume

## Objetivo
O objetivo deste projeto é desenvolver uma interface que capture dinamicamente o gesto da mão humana e controle o nível de volume.

Quando o dedo indicador se afasta do dedo polegar aumenta o volume e o quando o dedo polegar se aproxima do dedo indicador o volume diminue.

Conforme mostrado nas imagens abaixo:

![image](https://user-images.githubusercontent.com/42357180/161835429-beba5707-de42-4fa9-936d-c707341b77a5.png)

Na imagem abaixo é possível ver em tempo real o ponteiro do volume do windows mudar, conforme é feito o movimento entre os dedos.

![image](https://user-images.githubusercontent.com/42357180/161835512-41c5db07-d4bc-4bc5-ac7a-80d381ed5ae8.png)

![image](https://user-images.githubusercontent.com/42357180/161835557-bbfac549-c98a-423e-a04c-81ff55c8af37.png)

## Bibliotecas utilizadas

+ **OpenCV** - Biblioteca para visão computacional
+ **Pycaw** - Biblioteca de controle de áudio Python
+ **Mediapipe** - Mediapipe é uma biblioteca de aprendizado de máquina de código aberto do Google, que possui algumas soluções para reconhecimento facial e reconhecimento de gestos, e fornece encapsulamento de python, js e outras linguagens. O MediaPipe Hands é uma solução de rastreamento de mãos e dedos de alta fidelidade. Ele usa aprendizado de máquina (ML) para inferir 21 principais informações de mão 3D a partir de apenas um quadro. Podemos usá-lo para extrair as coordenadas dos pontos-chave da mão.

![image](https://user-images.githubusercontent.com/42357180/161835931-4c35b933-b38c-40f6-9f2f-dd9a21a8fba8.png)

O mediapipe detecta nossa mão com pontos para que possa ver a distância entre a ponta do dedo polegar e a ponta do dedo indicador. A distância entre os pontos 4 e 8 é diretamente proporcional ao volume do dispositivo.
Ponto:
+ Detectar pontos de referência de mão
+ Calcule a distância entre a ponta do polegar e a ponta do dedo indicador.
+ Mapeie a distância da ponta do polegar e da ponta do dedo indicador com a faixa de volume. No meu caso, a distância entre a ponta do polegar e a ponta do dedo indicador estava na faixa de 30 a 350 e a faixa de volume foi de -63,5 a 0,0.


## Instalação das Bibliotecas
