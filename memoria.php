<?php
  $fh = fopen('/proc/meminfo','r');
  $mem = 0;
  while ($line = fgets($fh)) {
    echo "<p>$line</p>";
  }
  fclose($fh);
?>