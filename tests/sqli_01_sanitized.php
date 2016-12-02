$nis=$_POST['nis'];
$nis2=mysql_real_escape_string($nis);
$query="SELECT *FROM siswa WHERE nis='$nis2'";
$q=mysql_query($query,$koneksi);
