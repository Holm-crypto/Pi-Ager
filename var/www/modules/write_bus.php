<?php 
// include 'database.php';
#Bus Werte in Datenbank schreiben
if(!empty($_POST['change_sensorbus_submit']))
{                       // ist das $_POST-Array gesetzt
    logger('DEBUG', 'button save change_sensorbus pressed');
    $bus_value = $_POST['bustype_admin'];
    if ($bus_value == 1){
        write_busvalue(1);
        logger('DEBUG', 'sensorbus saved. changed to 1wire (1)');
        print "<script language='javascript'>window.location.href='index.php';</script>";
        for ($x = 1; $x <= 100; $x++){
            sleep(2);
            file_get_contents(__DIR__ . 'index.php');
        }
        shell_exec('sudo /var/sudowebscript.sh sensorbus1wire');
    }
    if ($bus_value == 0){
        write_busvalue(0);
        logger('DEBUG', 'sensorbus saved. changed to i2c (0)');
        for ($x = 1; $x <= 100; $x++){
            sleep(2);
            file_get_contents(__DIR__ . 'index.php');
        }
        print "<script language='javascript'>window.location.href='index.php';</script>";
        sleep(5);
        shell_exec('sudo /var/sudowebscript.sh sensorbusi2c');
    }
    echo "<meta http-equiv='refresh' content='0'>";
}
?>