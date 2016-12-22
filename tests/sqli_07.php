$password=$_POST['password'];
$username=$_POST['username'];
$sql_user = "select * from login where user='$username' and password=md5('$password') ";
$hasil_user = mysql_query($sql_user,$koneksi);
