$user=mysql_escape_string($_GET['usr']);
$delete_user="DELETE FROM login WHERE user='$user'";
mysql_query($delete_user,$koneksi);
