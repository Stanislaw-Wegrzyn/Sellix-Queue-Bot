# Sellix-Queue-Bot
Bot odpowiedzialny za nadzorowanie autonomicznym sklepem discord nitro, współpracując ze snajperką nitro poprzez webhook channel.

<h2>Informacje ogólne: </h2>
<ul>
<li> <b>Język:</b> Python </li>
<li> <b>Użyte biblioteki zewnętrzne:</b>
<ul>
    <li>requests</li>
    <li>paramiko</li>
    <li>discord_components</li>
    <li>discord.py</li>
    <li>sellix</li>
    <li>remoteauthclient</li>
</ul>
</ul>

<h2> Mechaniki zawarte w programie: </h2>
<ul>
    <li>Lokalna baza danych na podstawie blikow JSON</li>
    <li>Kolejka klijętów i ceny produktów automatycznie i regularnie aktualizowane</li>
    <li>System kredytów (wirtualnej waluty) oraz rankingu klijentów</li>
    <li>Weryfikacja poprawności tokenów discord urzytkowników poprzez obsługe discord.com/api/v9</li>
    <li>Obsłuaga wielu serwerów vps poprze poołączenie ssh</li>
    <li>Bramka płatności Sellix na podstawie webhooków</li>
</ul>

<h2>Uwagi: </h2>
<ul>
    <li>Plik konfiguracyjny aby program móg być możliwie uniwersalny</li>
    <li>Zabezpieczenie przed nagłym przerwaniem procedury płatności</li>
    <li>Baza danych na plikach może nie jest najlepszym rozwiązaniem ale oszczędza to czas podczas konfiguracji</li>
  </ul>
