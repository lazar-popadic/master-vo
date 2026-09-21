### Problem procene kretanja
Procena sopstvenog polozaja je jedan od najvaznijih problema u mobilnoj robotici.
Nedovoljno brza i stabilna procena negatvino utice na upravljanje kretanjem,
dok se konstantne greske nagomilavaju i vremenom se gubi precizna pozicija robota.

#### Odometrija i lokalizacija
Odometrija je osnovni pristup proceni kretanja.
Promena polozaja se procenjuje na osnovu merenja nekog senzora.
Lokalizacija procenjuje polozaj u poznatom okruzenju i moze da kompenzuje nagomilanu
gresku odometrije.

### Vizuelna odometrija
Vizuelna odometrija inkrementalno procenjuje kretanje kamere na osnovu promene u
slikama koji taj pokret indukuje. Uspesnost procene kretanja direktno zavisi od
sadrzaja slika spoljasnjeg okruzenja. Najvazniji su sledeci faktori: osvetljenost
scene, staticna scena, tekstura i dovoljno preklapanje uzastopnih slika.

