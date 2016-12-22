$course=$_GET['id']; 
//	    (/home/iberiam/testes/WWW2015/communityedition/web_school/inc/get_batch.php)

$batchlist=$batchObj->selectbatch($course);
//	    (/home/iberiam/testes/WWW2015/communityedition/web_school/inc/get_batch.php)

$sql =  "SELECT * FROM batch WHERE course_id='$course' AND org_id='$org_id' ";
$result =  $this->database->query($sql);
