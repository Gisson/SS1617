$user=$_GET['usr'];
$delete_user="DELETE FROM login WHERE user='$user'";
mysql_query($delete_user,$koneksi);
