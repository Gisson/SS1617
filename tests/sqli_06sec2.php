$user=$_GET['usr'];
$delete_user="DELETE FROM login WHERE user='$user'";
mysql_query(mysql_escape_string($delete_user),$koneksi);
