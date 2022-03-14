# IMIĘ I NAZWISKO: DANIEL BALCERZAK
# KIERUNEK: INFORMATYKA
# PRZEDMIOT: ALOGRYTMY I STUKRUTY DANYCH
# ROK/SEMESTR: I/II


from PIL import Image
import numpy as np

# Zmienna do której zapisana jest nazwa pliku, który będzie otwarty

PHOTO_TO_OPEN = "kobieta.jpg"

# Zmienna DO_BLACK_AND_WHITE powinna posiadać wartości True albo False. W przypadku przyjęcia wartości True, zdjęcie
# zmieniane jest na odcienie szarości
DO_BLACK_AND_WHITE = 0

# Zmienna odpowiedzialna za kontrast. W celu uzyskania najlepszych efektów należy użyć wartości dodatnich. Gdzie wartość
# jeden (1) jest wartością oryginalnego obrazu. Wartości w przedziale <0, 1) zmiejszają kontrast a wartości (1, 255>
# zwiększają
CONTRAST_VALUE = 1.4

# Zmienna globalna reprezentująca granicę pomiędzy ciemnymi a jasnymi odcieniami. Ustawienie optymalne to 128
MIDDLE_BRIGHT_VALUE = 128

# Zmienna odpowiedzialna za jasność obrazu. Gdzie wartości ujemne to ściemnianie a wartości dodatnie rozjaśnianie obrazu
BRIGHTNESS_VALUE = -40

# Marcierz 3x3 odpowiadająca za przetwarzanie piksela uwzględniając piksele otaczające.
MATRIX = [[0, 0, 0],
          [0, 1, 0],
          [0, 0, 0]]

# Funkcja chunks() przyjmuje argumenty w postaci listy oraz liczby. Fnkcja jest funkcją generującą, ktora dzieli listę
# na określoną ilość kawałków. Instrukcja yield przerywa dzialanie funkcji, zapisuje jej stan, zwraca zaratość i wznawia
# działanie w miejscu w którym została zatrzymana


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Funkcja brighterdarker() przyjmuje argumeny w postaci zmiennej Integer, ktore reprezentują wartości piksela.
# Do wartości liczbowej piksela dodawana lub odejmowana jest wartość zadana w zmiennej globalnej.
# Funkcja zwraca wartość


def brigherdarker(pix):
    pix += BRIGHTNESS_VALUE
    return pix


# Funckja contrast() przjmuje argumenty w postaci wartści zmiennej Integer, ktora reprezentuje wartość piksela.
# Wartość 255 po podzieleniu na pół z założenia rozdziela obiekty jaśniejsze od ciemniejszych.
# Po odjęciu wartości środkowej mnożone przez liczbę w zakresie <0, 255> wartości dodatnie czyli jasne i ujemne
# czyli ciemne zmieniają swoją wartość. Po dodatniu odjętej wartości wracamy do poprzedniego zakresu barw.


def contrast(pix):
    pix -= MIDDLE_BRIGHT_VALUE
    pix *= CONTRAST_VALUE
    pix += MIDDLE_BRIGHT_VALUE
    return pix

# Funckja makeBlackWhite() przyjmuje wartości czerwonej, zielonej i niebieskiej warstwy oraz obrazu oryginalengo.
# Funckja tworzy nową warstwę z odcieniami szarości. Na RGB składa sie 29,9% czerwieni, 58,7% zieleni i
# 11,4% niebieskiego. Każdą z warstw zmniejszamy o odpowiedni procent i dodajemy składowe.
# Powstaje warstwa odcieni szarości, ktorą funkcja zwraca w postaci obrazu.


def makeBlackWhite(red_layer_list, green_layer_list, blue_layer_list, image):
    redLayer = red_layer_list.copy()
    greenLayer = green_layer_list.copy()
    blueLayer = blue_layer_list.copy()
    redLayer2d = list(chunks(redLayer, image.width))
    greenLayer2d = list(chunks(greenLayer, image.width))
    blueLayer2d = list(chunks(blueLayer, image.width))
    LayerNew = []
    for x in range(1, image.height - 1):
        for y in range(1, image.width - 1):
            blackWhitePix = redLayer2d[x][y] * 0.299 + greenLayer2d[x][y] * 0.587 + blueLayer2d[x][y] * 0.114
            LayerNew.append(blackWhitePix)

    LayerNew2d = list(chunks(LayerNew, image.width - 2))
    arr = np.array(LayerNew2d, dtype=np.uint8)
    newImg = Image.fromarray(arr)
    return newImg

# Funkcja makeNewLayer() przyjmuje argumenty w postaci listy pikseli warstwy oraz obrazu oryginalnego.
# Funkcja odpowiedzialna jest zamianę poszczególnych pikseli zgodnie z wytycznymi w programie.
# Funkcja zwraca warstwę w postaci jej obrazu.


def makeNewLayer(layer_list, image):
    Layer = layer_list
    Layer2d = list(chunks(Layer, image.width))
    LayerNew = []
    for x in range(1, image.height - 1):
        for y in range(1, image.width - 1):
            NewPix = (Layer2d[x - 1][y - 1] * MATRIX[0][0] + Layer2d[x - 1][y] * MATRIX[0][1] + Layer2d[x - 1][y + 1] *
                      MATRIX[0][2] + Layer2d[x][y - 1] * MATRIX[1][0] + Layer2d[x][y] * MATRIX[1][1] +
                      Layer2d[x][y + 1] * MATRIX[1][2] + Layer2d[x + 1][y - 1] * MATRIX[2][0] + Layer2d[x + 1][y] *
                      MATRIX[2][1] + Layer2d[x + 1][y + 1] * MATRIX[2][2])

            NewPix = brigherdarker(NewPix)
            NewPix = contrast(NewPix)

            # Warunki sprawdzają czy po przekształceniu wartości pikseli nie wykroczono poza zakras <0,255>, jeżeli
            # wykroczono ustawia wartość piksela na wartość graniczną.

            if NewPix > 255:
                NewPix = 255
            if NewPix < 0:
                NewPix = 0

            LayerNew.append(NewPix)

    LayerNew2d = list(chunks(LayerNew, image.width - 2))
    arr = np.array(LayerNew2d, dtype=np.uint8)
    newImg = Image.fromarray(arr)
    return newImg


# Funkcja main() jest funkcją główną. Nie przyjmuje i nie zwraca argumenów.

def main():
    im = Image.open(PHOTO_TO_OPEN)
    RGB = im.split()
    redLayerOrgin = list(RGB[0].getdata())
    greenLayerOrgin = list(RGB[1].getdata())
    blueLayerOrgin = list(RGB[2].getdata())

    if DO_BLACK_AND_WHITE:
        BWIm = makeBlackWhite(redLayerOrgin, greenLayerOrgin, blueLayerOrgin, im)
        BW = BWIm.split()
        redLayerBW = list(BW[0].getdata())
        newIm = makeNewLayer(redLayerBW, BWIm)

    else:
        R = makeNewLayer(redLayerOrgin, im)
        G = makeNewLayer(greenLayerOrgin, im)
        B = makeNewLayer(blueLayerOrgin, im)
        newIm = Image.merge("RGB", (R, G, B))

    # Okazanie zdjęcia
    newIm.show()

    # Zapisanie zdjęcia
    newIm.save(PHOTO_TO_OPEN[0:-4]+"_saved.jpg")
    print("Zdjęcie zostało zapisane")


if __name__ == '__main__':
    main()
