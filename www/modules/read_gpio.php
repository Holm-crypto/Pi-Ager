<?php 
    # Status auslesen
    $read_gpio_cooling_compressor = shell_exec('sudo /var/sudowebscript.sh read_gpio_cooling_compressor'); #Kühlung
    $read_gpio_heater = shell_exec('sudo /var/sudowebscript.sh read_gpio_heater'); #Heizung
    $read_gpio_humidifier = shell_exec('sudo /var/sudowebscript.sh read_gpio_humidifier'); #luftbefeuchter
    $read_gpio_circulating_air = shell_exec('sudo /var/sudowebscript.sh read_gpio_circulating_air'); #Umluft
    $read_gpio_exhausting_air = shell_exec('sudo /var/sudowebscript.sh read_gpio_exhausting_air'); #Abluft
    $read_gpio_uv_light = shell_exec('sudo /var/sudowebscript.sh read_gpio_uv_light'); #UV-Licht
    $read_gpio_light = shell_exec('sudo /var/sudowebscript.sh read_gpio_light'); # Licht
    $read_gpio_reserved1 = shell_exec('sudo /var/sudowebscript.sh read_gpio_reserved1'); # Reserviert 1
    

    #Prüfen ob Programme laufen
    $grepagingtable = shell_exec('sudo /var/sudowebscript.sh grepagingtable'); #Reifetab.py
    $grepmain = shell_exec('sudo /var/sudowebscript.sh grepmain'); #Rss.py

    #Schaltzustände setzen
    if($read_gpio_cooling_compressor == 0) {
        $cooler_on_off_png = 'images/led-on-green-20x20.png';
        }
    if($read_gpio_cooling_compressor == 1) {
        $cooler_on_off_png = 'images/led-off-green-20x20.png';
        }
    if($read_gpio_heater == 0) {
        $heater_on_off_png = 'images/led-on-green-20x20.png';
        }
    if($read_gpio_heater == 1) {
        $heater_on_off_png = 'images/led-off-green-20x20.png';
        }
    if($read_gpio_circulating_air == 0) {
        $circulating_on_off_png = 'images/led-on-green-20x20.png';
        }
    if($read_gpio_circulating_air == 1) {
        $circulating_on_off_png = 'images/led-off-green-20x20.png';
        }
    if($read_gpio_exhausting_air == 0) {
        $exhausting_on_off_png = 'images/led-on-green-20x20.png';
        }
    if($read_gpio_exhausting_air == 1) {
        $exhausting_on_off_png = 'images/led-off-green-20x20.png';
        }
    if($read_gpio_humidifier == 0) {
        $humidifier_on_off_png = 'images/led-on-green-20x20.png';
        }
    if($read_gpio_humidifier == 1) {
        $humidifier_on_off_png = 'images/led-off-green-20x20.png';
        }
    if($grepagingtable == 0) {
        $agingtable_on_off_png = 'images/led-off-green-20x20.png';
    }
    else {
        $agingtable_on_off_png = 'images/led-on-green-20x20.png';
    }
    if($grepmain == 0) {
        $pi_ager_on_off_png = 'images/led-off-green-20x20.png';
    }
    else {
        $pi_ager_on_off_png = 'images/led-on-green-20x20.png';
    }
?>