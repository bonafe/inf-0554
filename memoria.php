<?php
  $fh = fopen('/proc/meminfo','r');
  $mem = 0;
  while ($line = fgets($fh)) {
    echo "$line";
  }
  fclose($fh);
?>