### I-A	Problem procene kretanja
Procena sopstvenog polozaja je jedan od najvaznijih problema u mobilnoj robotici.
Nedovoljno brza i stabilna procena negatvino utice na upravljanje kretanjem,
dok se konstantne greske nagomilavaju i vremenom se gubi precizna pozicija robota.

#### I-B	Odometrija i lokalizacija
Odometrija je osnovni pristup proceni kretanja.
Promena polozaja se procenjuje na osnovu merenja nekog senzora.
Lokalizacija procenjuje polozaj u poznatom okruzenju i moze da kompenzuje nagomilanu
gresku odometrije.

### II-A	Vizuelna odometrija
Vizuelna odometrija inkrementalno procenjuje kretanje kamere na osnovu promene u
slikama koji taj pokret indukuje. Uspesnost procene kretanja direktno zavisi od
sadrzaja slika spoljasnjeg okruzenja. Najvazniji su sledeci faktori: osvetljenost
scene, staticna scena, tekstura i dovoljno preklapanje uzastopnih slika.

## TODO:
II-B	procena dubine u stereo
II-C	degeneracija stereo u mono
III-A	podela vizuelne odometrije
III-B	fotometrijska i reprojekciona greska
IV-A	SVO
IV-B	struktura
IV-C	procena kretanja
V-A		ORB-SLAM3
V-B		tipovi informacija
V-C		struktura i procesi
VI-A	TSformer-VO
VI-B	preklapanje ulaznih klipova
VI-C	samopaznja			(VIDI I STA JE TACNO)
VII-A	Prikupljanje eksperimentalnog skupa podataka
VII-B	kratak opis robota: slika robota
VII-C	rosbag
VII-D	kamera
VII-E	kalibracija: zasto mora, slika charuco table i proracunati parametri
VII-F	sekvence: slike sekvenci, snimak odozgo i snimak sa robota
VIII-A	Rezultati - kriterijumi
VIII-B	kratko o poravnavanju
VIII-C	rezultati SVO			- slika i deo iz tabele
VIII-D	rezultati ORB-SLAM3		- slika i deo iz tabele
VIII-E	rezultati TSformerVO	- slika i deo iz tabele
IX-A	Zakljucak: primena
IX-B	dalje ispitivanje
