import cv2 as cv
import mediapipe as mp
from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 5005
client = SimpleUDPClient(ip, port)


mp_hands = mp.solutions.hands #importa il modulo per il rilevamento delle mani e la stima della posizione dei punti chiave delle mani
mp_draw = mp.solutions.drawing_utils #importa il modulo per disegnare i punti chiave della mano e le connessioni tra di essi sul frame

cap = cv.VideoCapture(0) # accende la webcam 0 = webcam del computer

with mp_hands.Hands() as hands: #crea un oggetto per il rilevamento delle mani con i parametri di default, che includono la rilevazione di entrambe le mani e la stima della posizione dei punti chiave delle mani

    while True:

        ret, frame = cap.read() #legge un frame dalla webcam, ret è un booleano che indica se la lettura è avvenuta con successo, frame è l'immagine catturata

        if not ret:
            break 

        frame = cv.flip(frame, 1) # capovolge il frame orizzontalmente per avere un effetto specchio
        
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB) #converte il frame in RGB perché mediapipe lavora con questo formato

        results = hands.process(rgb) #elabora il frame con il rilevatore di mani e restituisce i risultati, che contengono le informazioni sui punti chiave delle mani rilevate

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand, handedness in zip(results.multi_hand_landmarks, results.multi_handedness): #per ogni mano rilevata, ottiene l'indice della mano e i punti chiave della mano
                label = handedness.classification[0].label  # "Left" o "Right"
                side = label.lower()  # "left" o "right"

                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS) #disegna i punti chiave della mano e le connessioni tra di essi sul frame
                for idx_landmark, landmark in enumerate(hand.landmark): #per ogni punto chiave della mano, ottiene le coordinate normalizzate (x, y, z) e le invia come messaggio OSC con un indirizzo specifico
                    client.send_message(f"/hand/{side}/{idx_landmark}/x", landmark.x)  #crea un indirizzo OSC per ogni punto chiave della mano, con il formato /hand/indice_mano/indice_punto_chiave
                    client.send_message(f"/hand/{side}/{idx_landmark}/y", landmark.y)
                    client.send_message(f"/hand/{side}/{idx_landmark}/z", landmark.z)
            #client.send_message(osc_address, [landmark.x, landmark.y, landmark.z]) #invia un messaggio OSC con l'indirizzo e i valori delle coordinate del punto chiave della mano
            #print(idx_hand, idx_landmark, landmark.x, landmark.y, landmark.z) #stampa l'indice della mano, l'indice del punto chiave e le coordinate normalizzate del punto chiave della mano
      
        cv.imshow("Hands", frame)
    
        if cv.waitKey(1) & 0xFF == ord('q'): #se l'utente preme il tasto 'q', esce dal ciclo e chiude la finestra
            break

cap.release()
cv.destroyAllWindows()