<?php
  
   //TODO: adicionar monitoramento de IO:
   //		sudo apt-get install sysstat
   //		iostat -d 30 /dev/sda 

  ini_set('display_errors', 1);
  ini_set('display_startup_errors', 1);
  error_reporting(E_ALL);

  function valorCampo($campo){
     return explode (" ", trim ($campo))[0];
  }

  $fh = fopen('/proc/meminfo','r');
 
  $memTotal = 0;
  $memFree = 0;
  $memAvailable = 0;

  while ($line = fgets($fh)) {
    
    $campos = explode(":",$line);

    if ($campos[0] == "MemTotal") { 

       $memTotal = floatval(valorCampo($campos[1]));
       echo "Memória Total: $memTotal\n";
 
    }elseif ($campos[0] == "MemAvailable"){

       $memAvailable = floatval(valorCampo($campos[1]));
       echo "Memória Disponível: $memAvailable\n";
    }
    //echo "$line";
  }
  $percDisponivel = $memAvailable/$memTotal;
  echo "Percentual de memória disponível: $percDisponivel\n";
  $cpu = implode("-",sys_getloadavg());
  echo "CPU: $cpu\n";
  fclose($fh);
?>
