### I-A	Problem procene kretanja
Procena sopstvenog polozaja je jedan od najvaznijih problema u mobilnoj robotici.
Nedovoljno brza i stabilna procena negatvino utice na upravljanje kretanjem,
dok se konstantne greske nagomilavaju i vremenom se gubi precizna pozicija robota.

#### I-B	Odometrija i lokalizacija
Odometrija je osnovni pristup proceni kretanja.
Promena polozaja se procenjuje na osnovu merenja nekog senzora.
Lokalizacija procenjuje polozaj u poznatom okruzenju i moze da kompenzuje nagomilanu
gresku odometrije.

### II-A	Vizuelna odometrija (slika stereo i mono kamere)
Vizuelna odometrija inkrementalno procenjuje kretanje kamere na osnovu promene u
slikama koji taj pokret indukuje. Uspesnost procene kretanja direktno zavisi od
sadrzaja slika spoljasnjeg okruzenja. Najvazniji su sledeci faktori: osvetljenost
scene, staticna scena, tekstura i dovoljno preklapanje uzastopnih slika. Stereo
vizuelna odometrija koristi 2 kamere za procenu kretanja, dok monokularna koristi 1.

#### II-B	Procena dubine (slika disparity.jpeg, formula: b·f/d i znacenje velicina)
Procena dubine predstavlja osnovu algoritama vizuelne odometrije. U stereo slucaju,
dubina 3D tacke se racuna na osnovu bazne distance, odnosno rastojanja izmedju leve i
desne kamere, dispariteta, odnosno razlike polozaja odgovarajuceg piksela u obe slike,
i zizne daljine. Greska procene dubine raste sa kvadratom udaljenosti izmedju tacke i kamere.
I zbog toga se u slucaju velikih udaljenosti tacaka u sceni, stereo vizuelna odometrija se
svodi na slucaj monokularne.

#### II-C	Monokularna vizuelna odometrija (slika mono kamere)
U monokularnom slucaju, tacka u sceni se posmatra iz dva razlicita polozaja kamere.
Dubina ne moze direktno da se izmeri, jer ne postoji podatak kao bazna distanca. I zbog
toga, algoritmi za vizuelnu odometriju mogu da procene kretanje samo do faktora skale.

### III-A	Podela vizuelne odometrije (stablo podele i greske)
Metode vizuelne odometrije mogu da se podele na geometrijske i metode zasnovane na
dubokom ucenju. Geometrijske mogu dalje da se podele na metode zasnovane na
karakteristicnim tackama i direktne.

#### III-B	Fotometrijska greska (formula 4 i znacenje oznaka)
Direktne metode procenjuju kretanje minimizacijom fotometrijske greske. Ona predstavlja
razliku intenziteta izmedju odgovarajucih piksela u paru slika.

#### III-C	Reprojekciona greska (slika karakteristike i greske)
Metode zasnovane na karakteristicnim tackama detektuju i uparuju karakteristike.
Karakteristika je obrazac u slici koji se razlikuje od svog neposrednog okruzenja. U ovim
metodama, kretanje se procenjuje minimizacijom reprojekcione greske. Ona predstavlja
razliku izmedju izmerenih koordinata karakteristicne tacke u slici i projektovanih
koordinata odgovarajuce 3D tacke.

## TODO:
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
