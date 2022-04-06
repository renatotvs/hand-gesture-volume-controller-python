# Controlador de volume por gestos da mão usando Python

Este projeto é sobre utilizar a camera para controlar o volume em tempo real com o uso de bibliotecas em python: openCV, mediapipe e Pycall

**Assunto abordado:** Visão Computacional

## Introdução

O reconhecimento de gestos ajuda os computadores a entender a linguagem do corpo humano. Isso ajuda a construir um vínculo mais potente entre humanos e máquinas, em vez de apenas as interfaces de usuário de texto básicas ou interfaces gráficas de usuário (GUIs). Neste projeto de reconhecimento de gestos, os movimentos do corpo humano são lidos pela câmera do computador. O computador então usa esses dados como entrada para lidar com o aplicativo. 

## Bibliotecas utilizadas

+ **OpenCV** - Biblioteca para visão computacional
+ **Pycaw** - Biblioteca de controle de áudio Python
+ **Mediapipe** - Mediapipe é uma biblioteca de aprendizado de máquina de código aberto do Google, que possui algumas soluções para reconhecimento facial e reconhecimento de gestos, e fornece encapsulamento de python, js e outras linguagens. O MediaPipe Hands é uma solução de rastreamento de mãos e dedos de alta fidelidade. Ele usa aprendizado de máquina (ML) para inferir 21 principais informações de mão 3D a partir de apenas um quadro. Podemos usá-lo para extrair as coordenadas dos pontos-chave da mão.

![image](https://user-images.githubusercontent.com/42357180/161835931-4c35b933-b38c-40f6-9f2f-dd9a21a8fba8.png)

Documentação: <a href='https://google.github.io/mediapipe/solutions/hands.html'> Mediapipe </a>

A imagem acima mostra os números dos pontos que o MediaPipe usa para se referir a diferentes pontos da mão. 

Usaremos a distância entre os pontos 4 e 8 que será diretamente proporcional ao volume do dispositivo.

## Cenário 
+ Detectar pontos de referência da mão
+ Detectar a localização das pontas dos dedos indicador e polegar
+ Calcular a distância entre a ponta do polegar e a ponta do dedo indicador.
+ Mapear a distância da ponta do polegar e da ponta do dedo indicador com a faixa de volume. Nesse caso, a distância entre a ponta do polegar e a ponta do dedo indicador estava na faixa de 30 a 350 e a faixa de volume foi de -63,5 a 0,0.

## Objetivo
O objetivo deste projeto é desenvolver uma interface que capture dinamicamente o gesto da mão humana e controle o nível de volume.

Quando o dedo indicador se afasta do dedo polegar aumenta o volume e o quando o dedo polegar se aproxima do dedo indicador o volume diminue.

## Ambiente de desenvolvimento

No desenvolvimento pode ser construído tanto no jupyter notebook quanto outros editores para python. No meu caso utilizei o PyCharm, conforme abaixo:

![image](https://user-images.githubusercontent.com/42357180/161844629-45ea18de-7533-4d75-8a40-0fbf3ccf2ef8.png)

Criar um novo projeto

![image](https://user-images.githubusercontent.com/42357180/161845151-20e42069-f691-4b55-897d-57b8803a801b.png)

![image](https://user-images.githubusercontent.com/42357180/161845831-15f4c12b-874b-4d4f-b399-00b7ffaef5a7.png)

O projeto contém os arquivos abaixo:
+ HandGestureVolumeController.py
+ HandingTrackingModule.py

## Instalação das Bibliotecas

Abrir o terminal e efetuar as seguintes instalações:

> pip install python-opencv

> pip install mediapipe

> pip install pycaw


## Passo 1: Importar bibliotecas

```
import in orange cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
#control volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
```

## Passo 2: Configurações da Camera
```
############################################################
wCam, hCam = 640, 480 # definições do tamanho da tela
############################################################

camera = 0 #1

cap = cv2.VideoCapture(camera)

cap.set(3, wCam) # aplica tamanho na horizontal
cap.set(4, hCam) # aplica tamanho na vertical
```

Acima obtemos a entrada de vídeo da câmera principal do nosso computador. Se estiver usando qualquer outra câmera, substitua o número 0 pelo da câmera que está usando.

## Passo 3: Configurar, Detectar as mãos
```
detector = htm.handDetector(detectionCon=0.7, maxHands=1)
```

No código acima, estamos chamando htm.handDetector módulo para detectar as mãos da entrada de vídeo que recebemos de nossa câmera principal.
As configurações do mediapipe e métodos estão separados no arquivo HandTrackingModule.py que está sendo importado no código.

## Passo 4: Configurações para controlar o alto-falante com a biblioteca pycaw
```
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
```

Estas são as inicializações que precisamos para pycaw funcionar. Você pode encontrar a documentação da biblioteca <a href='https://github.com/AndreMiras/pycaw'> aqui </a>

## Passo 5: encontrar a faixa de volume entre o volume mínimo e máximo
```
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
```

## Passo 6: Captura imagem da camera e faz detecção da mão
```
while True:

    success, img = cap.read()

    img = detector.findHands(img)
```

O código acima verifica se a câmera que especificamos funciona. Se funcionar, vamos capturar para o processamento da imagem e detecção da mão. 

## Passo 7: Capturar o posicionmento da mão
```
lmList = detector.findPosition(img, draw=False)
```

Acima recebemos as coordenadas da mão.

## Passo 8: Aplicar o filtro das coordendas que iremos utilizar:
```
 if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
```
Acima especificamos os pontos da mão que usaremos: indice 4 - Polegar e indice 8 o indicador.

Lá no início temos a imagem com o mapeamento desses pontos com a biblioteca mediapipe.

## Passo 9: Desenhando um círculo entre a ponta do polegar e a ponta do dedo indicador
```
cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
```

O código acima desenha um círculo na ponta do polegar e no dedo indicador com as coordenadas (x e y).

(x1, y1)especifica que vamos desenhar o círculo na ponta do polegar onde 15 é o raio do círculo e (255, 0, 0) é a cor do círculo, cv2.FILLED refere-se à espessura dos pixels que preencherão o círculo com a cor que especificamos.
(x2, y2)especifica que vamos desenhar o círculo na ponta do indicador.

A cor está no padrão BGR (blue, green, red).

## Passo 10: Desenhar uma linha entre os pontos 4 e 8
```
cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
```
No código acima, usamos a cv2.line função para desenhar uma linha entre o ponto quatro da mão e o ponto 8. A linha conectará ponto 4 (x1, y1), que é a ponta do polegar, e ponto 8 (x2, y2), que é a ponta do dedo indicador. (255, 0, 0)é a cor da linha e 3 é a sua espessura.

## Passo 11: Calcular a distância entre os pontos 4 e 8

```
# lengh = math.hypot(x2 - x1, y2 - y1)
```
No código acima, encontramos a distância entre a ponta do polegar e o dedo indicador usando uma hipotenusa. Conseguimos isso chamando a hypot função matemática e passando a diferença entre x2 e x1 e a diferença entre y2 e y1.

## Passo 12: Convertendo o alcance das mãos para o alcance do volume

```
vol = np.interp(lengh, [50, 300], [minVol, maxVol])
```
função NumPy np.interp, para converter o intervalo de mão para o intervalo de volume. Os argumentos usados ​​são:

+ length: Este é o valor que queremos converter.
+ [50 - 300]: Este é o alcance da mão.
+ [volMin, volMax]: Fornecendo o intervalo para o qual queremos converter.

configuração para barra do volume:

```
volBar = np.interp(lengh, [50, 300], [360, 150])
```

configuração para exiição do volume de 0 á 100:

```
volPerc = np.interp(lengh, [50, 300], [0, 100])
```

## Passo 13: Setar o volume principal

```
# volume.SetMasterVolumeLevel(vol, None)
volume.SetMasterVolumeLevelScalar(volPerc / 100, None)
```

No exemplo acima utilizamos volume.SetMasterVolumeLevelScalar.

## Passo 14: Desenhar uma barra de controle de volume

```
cv2.rectangle(img, (50, 150), (85, 360), (255,0,0), 3)
cv2.rectangle(img, (50, int(volBar)), (85, 360), (0, 255, 0), cv2.FILLED)
```

O primeiro retangulo é para criar o contorno e segundo retangulo é criado para receber um preenchimento dinâmico, para simular uma barra de controle do volume.

## Passo 15: Mostra o volume atual na tela

```
cVol = round(volume.GetMasterVolumeLevelScalar() * 100)
cv2.putText(img, f'Vol: {cVol}', (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
```

## Passo 16: Exibe o video para interação com o usuário

```
cv2.imshow("img", img)
```

## Etapa 17: Fechar Janela

```
k = cv2.waitKey(1) & 0xFF

    if k == 27 or k == 13:
        break
```
O código acima encerrará o programa quando o usuário pressionar a tecla ESC ou ENTER.


## Código Completo:

```

import cv2
import numpy as np
import HandTrackingModule as htm
import math
#control volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


############################################################
wCam, hCam = 640, 480
#wCam, hCam = 1200, 600
############################################################

camera = 0 #1

cap = cv2.VideoCapture(camera)

cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


#volume.GetMute()
#volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

vol = -20.0
volBar = 318 #360
volPerc = 20

while True:

    success, img = cap.read()

    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        #print(lmList[2])
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        lengh = math.hypot(x2 - x1, y2 - y1)

        # Hand range 50 - 300
        # Volume Range -65 -0

        vol = np.interp(lengh, [50, 300], [minVol, maxVol])
        volBar = np.interp(lengh, [50, 300], [360, 150])
        volPerc = np.interp(lengh, [50, 300], [0, 100])

        print("volBar: ", volBar)

        print("volPerc: ", round(volPerc))

        #volume.SetMasterVolumeLevel(vol, None)
        volume.SetMasterVolumeLevelScalar(volPerc / 100, None)
        print(int(lengh), vol)

    else:
        # seta um volume padrão é o ultimo volume feito pelo movimento das mãos
        #volume.SetMasterVolumeLevel(vol, None)
        volume.SetMasterVolumeLevelScalar(volPerc / 100, None)

    cv2.rectangle(img, (50, 150), (85, 360), (255,0,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 360), (0, 255, 0), cv2.FILLED)

    cVol = round(volume.GetMasterVolumeLevelScalar() * 100) # mostra volume do windows
    cv2.putText(img, f'Vol: {cVol}', (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("img", img)

    k = cv2.waitKey(1) & 0xFF

    if k == 27 or k == 13:
        break

```

## Resultados

Conforme mostrado nas imagens abaixo:

![image](https://user-images.githubusercontent.com/42357180/161835429-beba5707-de42-4fa9-936d-c707341b77a5.png)

Na imagem abaixo é possível ver em tempo real o ponteiro do volume do windows mudar, conforme é feito o movimento entre os dedos.

![image](https://user-images.githubusercontent.com/42357180/161835512-41c5db07-d4bc-4bc5-ac7a-80d381ed5ae8.png)

![image](https://user-images.githubusercontent.com/42357180/161835557-bbfac549-c98a-423e-a04c-81ff55c8af37.png)
