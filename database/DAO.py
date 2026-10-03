from database.DB_connect import DBConnect
from model.album import Album
"""
CHINOOK: ALBUM E PLAYLIST

Si consideri il database "Chinook", contenente informazioni su album (album),
brani (track), playlist (playlist) e associazioni tra playlist e brani
(playlisttrack). Si intende costruire un'applicazione che permetta di analizzare
le relazioni tra album in base alle playlist in cui compaiono i loro brani.

PUNTO 1
a. L'utente inserisce in un campo di testo una durata d in minuti.

b. Premendo "Crea Grafo", l'applicazione costruisce un grafo semplice, non
   orientato e non pesato.
   - I vertici sono gli album la cui durata complessiva (somma delle durate dei
     loro brani) e' maggiore di d minuti.
   - Esiste un arco tra due album distinti se almeno un brano del primo e almeno
     un brano del secondo compaiono nella stessa playlist.
   Costruito il grafo, l'applicazione visualizza il numero di vertici e di archi.

c. L'utente seleziona da un menu a tendina un album a1 tra quelli presenti nel
   grafo. Premendo "Analisi componente", l'applicazione stampa la dimensione
   della componente connessa che contiene a1 e la durata complessiva, in minuti,
   di tutti gli album di quella componente.

PUNTO 2
a. L'utente inserisce in un campo di testo una durata massima dTOT in minuti.

b. Premendo "Set di album", l'applicazione determina, mediante un algoritmo
   ricorsivo, un insieme di album che:
   - contenga a1, l'album selezionato al punto 1.c;
   - contenga solo album della stessa componente connessa di a1;
   - abbia una durata complessiva minore o uguale a dTOT;
   - contenga il massimo numero di album possibile.

c. L'applicazione stampa gli album dell'insieme con la rispettiva durata, il
   numero di album e la durata totale. Se a1 da solo supera dTOT, va mostrato
   un messaggio.

Tutti i possibili errori di immissione, validazione dati, accesso al database
ed algoritmici devono essere gestiti; non sono ammesse eccezioni generate dal
programma.

NOTE
- La durata dei brani e' nel campo Milliseconds di track: per avere i minuti si
  divide per 60000.

VALORI DI CONTROLLO
- d = 60: 102 vertici, 4231 archi.
- d = 100: 13 vertici, 48 archi.
- d = 60, album "Big Ones", Analisi componente: 92 album, 6745.72 minuti.
- d = 60, album "Big Ones", Set di album:
    dTOT 200 -> 3 album, 194.00 minuti
    dTOT 300 -> 4 album, 254.30 minuti
    dTOT 400 -> 6 album, 374.96 minuti
- d = 60, album "Chronicle, Vol. 1", dTOT 300 -> 4 album, 248.88 minuti
"""

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi(minuti):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT al.AlbumId AS alID, al.Title AS titolo, SUM(t.Milliseconds) / 60000 AS durata
            FROM album al, track t
            WHERE al.AlbumId = t.AlbumId
            GROUP BY al.AlbumId, al.Title
            HAVING SUM(t.Milliseconds) / 60000 > %s
        """
        cursor.execute(query, (minuti,))
        for row in cursor:
            result.append(Album(row["alID"], row["titolo"], float(row["durata"])))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getEdges():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT DISTINCT a1.AlbumId AS id1, a2.AlbumId AS id2
            FROM (SELECT DISTINCT pt.PlaylistId, t.AlbumId
                  FROM playlisttrack pt, track t
                  WHERE pt.TrackId = t.TrackId) a1,
                 (SELECT DISTINCT pt.PlaylistId, t.AlbumId
                  FROM playlisttrack pt, track t
                  WHERE pt.TrackId = t.TrackId) a2
            WHERE a1.PlaylistId = a2.PlaylistId
              AND a1.AlbumId < a2.AlbumId
        """
        cursor.execute(query)
        for row in cursor:
            result.append((row["id1"], row["id2"]))
        cursor.close()
        cnx.close()
        return result