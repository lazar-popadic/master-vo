### I-A		Problem procene kretanja
- Procena sopstvenog polozaja je jedan od najvaznijih problema u mobilnoj robotici.
- Odometrija je osnovni pristup proceni kretanja i njen zadatak je da
proceni promenu polozaja na osnovu merenja nekog senzora.
- Lokalizacija procenjuje polozaj u poznatom okruzenju i moze da kompenzuje nagomilanu
gresku odometrije.

### II-A	Vizuelna odometrija
- Vizuelna odometrija inkrementalno procenjuje kretanje kamere na osnovu promene u
slikama koji taj pokret indukuje.
- Uspesnost procene kretanja direktno zavisi od sadrzaja slika spoljasnjeg okruzenja.
- Najvazniji su sledeci faktori: osvetljenost scene, staticna scena, tekstura i
dovoljno preklapanje uzastopnih slika.

#### II-B	Vizuelna odometrija (slika stereo i mono kamere)
- Stereo vizuelna odometrija koristi 2 kamere za procenu kretanja, dok monokularna koristi 1.

#### II-C	Procena dubine (slika dispariteta)
- Procena dubine predstavlja osnovu algoritama vizuelne odometrije. 
- U stereo slucaju, dubina 3D tacke se racuna na osnovu bazne distance- ..., dispariteta- ...,
i zizne daljine.
- Greska procene dubine raste sa kvadratom udaljenosti izmedju tacke i kamere.
- I zbog toga se u slucaju velikih udaljenosti tacaka u sceni, stereo vizuelna odometrija
svodi na slucaj monokularne.

#### II-D	Monokularna vizuelna odometrija (slika mono kamere)
- U monokularnom slucaju, tacka u sceni se posmatra iz dva razlicita polozaja kamere.
- Dubina ne moze direktno da se izmeri, jer ne postoji podatak kao bazna distanca.
- I zbog toga, algoritmi za monokularnu vizuelnu odometriju mogu da procene kretanje
samo do faktora skale.

### III-A	Podela vizuelne odometrije (stablo podele i greske)
- Metode vizuelne odometrije mogu da se podele na geometrijske i metode zasnovane na
dubokom ucenju.
- Geometrijske mogu dalje da se podele na metode zasnovane na karakteristicnim tackama
i direktne.

#### III-B	Fotometrijska greska (formula 4 i znacenje oznaka)
- Direktne metode procenjuju kretanje minimizacijom fotometrijske greske.
- Ona predstavlja razliku intenziteta izmedju odgovarajucih piksela u paru slika.

#### III-C	Reprojekciona greska (slika karakteristike i greske)
- Metode zasnovane na karakteristicnim tackama detektuju i uparuju karakteristike.
- Karakteristika je obrazac u slici koji se razlikuje od svog neposrednog okruzenja.
- U ovim metodama, kretanje se procenjuje minimizacijom reprojekcione greske.
- Ona predstavlja razliku izmedju izmerenih koordinata karakteristicne tacke u slici
i projektovanih koordinata odgovarajuce 3D tacke.

###	IV-A	SVO (Semi-Direct Visual Odometry)
- SVO je algoritam za monokularnu vizuelnu odometriju koji je prvenstveno razvijen za
primenu u mikro letelicama.
- Algoritam koristi korespondenciju karakteristika koja je implicitan rezultat direktne
procene kretanja.

#### IV-B	SVO - Struktura(slika 2.1)
- Algoritam je podeljen u dva paralelna procesa.
- Proces za procenu kretanja obradjuje svaku sliku i procenjuje pozu u odnosu na mapu.
- Proces za mapiranje prosiruje mapu novim 3D tackama.

#### IV-C	SVO - Procena kretanja (ista slika 2.1)
- Procena kretanja se sastoji iz 3 koraka.
- U inicijalizaciji poze se procenjuje relativna poza kamere u odnosu na prethodnu sliku
minimizacijom fotometrijske greske izmedju porducja slike koji odgovaraju istim 3D tackama.
- Drugi korak predstavlja optimizaciju polozaja svakog izdvojenog podrucja pojedinacno.
- Poslednjim korakom se optimizuju poza kamere i polozaji 3D tacaka minimizacijom reprojekcione
greske.

### V-A		ORB-SLAM3
- ORB-SLAM3 je sistem za vSLAM, odnosno vizuelnu simultanu lokalizaciju i mapiranje
- Obuhvata cisto vizuelni, vizuelno-inercijalni i SLAM sa vise mapa.
- Podrzava monokularne, stereo i depth kamere.

#### V-B	ORB-SLAM3 - Tipovi informacija
- Autori razlikuju 3 novoa informacija koji su znacajni za procenu kretanja.
- Kratkorocne informacije se koriste za pracenje elemenata mape dok su pogledu, i zaboravljaju se
cim nestanu iz pogleda.
- Srednjerocne informacije se koriste za uparivanje trenutne slike sa elementima iz okruzenja koji
se nalaze blizu kamere.
- Dugorocne informacije su zasnovane na prepoznavanju okruzenja i one omogucavaju spajanje nepovezanih
mapa i relokalizaciju.

#### V-C	ORB-SLAM3 - Struktura i procesi
- ORB-SLAM se sastoji iz 3 paralelna procesa i strukture Atlas.
- Proces za pracenje procenjuje pozu minimizacijom reprojekcione greske uparenih karakteristika.
- Proces za lokalno mapiranje dodaje nove i otklanja redundantne kljucne slike i 3D tacke.
- Proces za spajanje mapa detektuje zajednicke regione izmedju mapa i vrsi spajanje mapa.
- Atlas je struktura za reprezentaciju vise nepovezanih mapa, od kojih je jedna aktivna u svakom trenutku.

### VI-A	TSformer-VO
- TSformer-VO je metoda monokularne vizuelne odometrije zasnovana na dubokom ucenju,
- koja problem procene kretanja posmatra kao zadatak razumevanja videa.
- Model regresijom procenjuje relativne poze kamere na osnovu kratkog skupa uzastopnih slika.

#### VI-B	TSformer-VO - Struktura (slika 2.4)
- Skup od Nf uzastopnih slika predstavlja ulazni podatak.
- Svaka slika se deli u nepreklapajuce regione koji se ugradjuju u tokene.
- Niz tokena prolazi kroz Transformer enkoder.
- Na pocetak niza tokena se dodaje klasni token, koji se prosledjuje izlaznom viseslojnom perceptronu.
- Za jednu relativnu pozu su potrebne 2 uzastopne slika.
- Odnosno, za skup od Nf slika, dobijamo Nf-1 pozu.

#### VI-C	TSformer-VO - Samopaznja (slika 2.6 ali samo gornji deo)
- Samopaznja je mehanizam kojim model razmatra odnose izmedju tokena.
- Podeljena prostorno-vremenska samopaznja podrazumeva razdvajanje vremenske i prostorne obrade.
- Prvo se razmatraju tokeni sa istim prostornim indeksom duz vremenske ose,
- a zatim tokeni iz iste slike duz prostorne ose.

### VII-A	Prikupljanje eksperimentalnog skupa podataka
- Kako bi se ispitala primena vizuelne odometrije u mobilnoj robotici, prikupljen je eksperimentalni
skup podataka.
- Eksperimentalnu postavku cine robot sa kamerom, koji se krece kroz razlicite sekvence kretanja u
definisanom prostoru.

#### VII-B	Robot (slika 3.1)
- Za prikupljanje podataka koriscen je mobilni robot razvijen u okviru tima +381 Robotics.
- Robot koristi diferencijalni pogon koji omogucava 3 osnovna tipa kretanja: pravolinijska translacija,
rotacija oko centra robota i krivolinijsko kretanja.

#### VII-C	Robot (slika 3.2, jednacine 6-13)
- Оdometrijski sistem je odvojen od pogonskog.
- Inkrementalni enkoderi se nalaze na pasivnim tockovima.
- Kretanje robota se procenjuje na osnovu merenja sa enkodera prema kinematskom modelu diferencijalnog
robota.

#### VII-D	Kamera
- Za snimanje sekvenci je koriscena OV9281 kamera.
- Ona je tipa global-shutter, odnosno svi pikseli u slici se snimaju u istom trenutku i tokom istog vremena ekspozicije.
- Ova kamera je monohromatska i snimanje je vrseno brzinom 120 slika po sekundi, rezolucije 1280*720 piksela.

#### VII-E	Kalibracija kamere (slika 3.3 i formule 16-17)
- Kalibracija kamere sluzi za identifikaciju unutrasnjih parametara kamere i koeficijenata izoblicenja,
- koji su prikazani ovde.
- Za kalibraciju je koriscena ChArUco tabla, koja kombinuje sahovsku tablu i ArUco markere. 
- Za kalibraciju je korisceno 50 slika table

#### VII-F	Sekvence (snimak odozgo, 48s dok pricam)
- Robot se kretao po stolu za takmicenje Eurobot 2026 koji se nalazi u laboratoriji G3.
- Snimljena su dva tipa sekvenci.
- Prvi tip se sastoji od pravolinijskih translacija i rotacije, dok drugi tip koristi i
krivolinijske kretnje.
- Oba tipa obuhvataju po 2 sekvence sa razlicitim maksimalnim brzinama.

#### VII-G	Procena referentnih putanja (straight snimak, prvih 10s je to, ali pusti da ide)
- Dimenzije stola su tacno definisane i na obodu stola je zid.
- U trenutku kada robot udari u zid, jedna njegova koordinata i orijentacija su tacno definisane.
- Kratkom sekvencom u kojoj robot udari u dva zida koja se nalaze pod pravim uglom mozemo da dobijemo referentnu tacku gde je potpuno poznat polozaj robota.
- Referentne tacke su koriscene za proveru greske odometrije sa tockova i za dobijanje referentne putanje.

#### VII-H	rosbag (snimak sa robota, 47s ide dok pricam)
- Ovde je prikazan snimak sa kamere na robotu tokom jedne od sekvenci.
- Za pravljenje skupa podataka koriscen je rosbag. To je alat koji sluzi za snimanje podataka koji se
objavljuju na topicima u okviru ROS-a.
- Pored samih podataka, cuva se i vreme objavljivanja.
- Snimljeni podaci se kasnije mogu reprodukovati, cime se reprodukuje tok podataka zabelezen tokom rada robota
u realnom vremenu.
- To omogucava da se razliciti algoritmi testiraju na identicnim podacima.

### VIII-A	Kriterijumi evaluacije
- Za evaluaciju je koriscen alat KITTI Odometry Evaluation Toolbox.
- U okviru njega je definisano 5 kriterijuma: ...
- Medjutim, relativna greska poze za translaciju nije razmatrana, zbog uticaja gubitka pracenja na njenu
vrednost.

#### VIII-B	Poravnavanje procenjene i referentne putanje
- Kako bi procenjena i referentna putanja mogle da se porede, potrebno ja da budu predstavljene u istom
koordinatnoм sistemu.
- Takodje, zbog ogranicenja monokularne vizuelne odometrija da proceni kretanje
samo do faktora skale, potrebno je skalirati procenjene putanje.
- Poravnavanje se vrsi u okviru alata za evaluaciju, primenom Umeyama metode.

#### VIII-C	Rezultati SVO (slika i tabela)
- SVO je ostvario dobru procenu rotacije i na lokalnom i na globalnom nivou.
- Medjutim, nije u stanju da pouzdano proceni skalu translacije.
- U brzoj krivolinijskoj sekvenci je doslo do jednog gubitka pracenja pri rotaciji.
- Svaki procenjeni segment odrzava priblizno istu orijentaciju, ali relativna skala se stalno menja
i dolazi do znacajnih odstupanja od referentne putanje.

#### VIII-D	Rezultati ORB-SLAM3 (slika i tabela)
- U ORB-SLAM algoritmu je dolazilo do gubitka pracenja na kraju svake rotacije oko centra robota.
- U sporoj krivolinijskoj sekvenci je doslo do uspesne lokalizacije, sto je dovelo do odlicnog
podudaranja sa referentnom putanjom, sto moze da se vidi na slici.
- ORB-SLAM pokazuje dobru globalnu procenu kretanja, ali losiju lokalnu procenu. 
- Takodje pokazuje osetljivost na brzinu kretanja: sa porastom brzine, opada uspesnost procene.

#### VIII-E	Rezultati TSformer-VO (slika i tabela)
- TSformer-VO nije uspeo da smisleno proceni kretanje.
- Verovatan razlog za to je velika razlika izmedju skupa podataka na kojima je obucavan i podataka u
ovom eksperimentu.

### IX-A	Zakljucak: primena
- Monokularna vizuelna odometrija je prikazana kao potencijalno resenje problema procene kretanja.
- Kamere predstavljaju relativno jeftine senzore koji obezbedjuju veliku kolicinu podataka velikom
frekvencijom.
- Pored procene kretanja, podaci mogu da se koriste i za lokalizaciju i za resavanje
drugih zadataka masinske vizije.
- Medjutim, monokularna vizuelna odometrija ima znacajna ogranicenja.
- Procena kretanja je osetljiva na vizuelno okruzenje i na brzinu kretanja.
- U slucaju gubitka pracenja sistem ostaje bez informacija o kretanju.
- Neodredjenost apsolutne skale omogucava samo relativnu procenu kretanja.
- Zbog toga, monokularna vizuelna odometrija je pogodnija kao deo sistema za lokalizaciju nego kao
samostalan izvor procene polozaja.

### IX-B	Zakljucak: dalja ispitivanja
- Dalja ispitivanja bi mogla da obuhvataju duze sekvence i vec mapirane prostore.
- Zbog ogranicenja konstrukcije robota, nisu ispitane razlicite orijentacije kamere.
- Mogla bi se ispitati i fuzija sa drugim senzorima, narocito inercijalnim sa kojima se
cesto kombinuju algoritmi vizuelne odometrije.
