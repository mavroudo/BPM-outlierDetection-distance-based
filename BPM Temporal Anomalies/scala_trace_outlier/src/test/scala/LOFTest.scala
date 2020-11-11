import org.apache.log4j.{Level, Logger}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.scalatest.{BeforeAndAfterAll, FunSuite}
import oultierDetectionAlgorithms.{Distances, InitializeNeighbors, LOF, Structs}

class LOFTest extends FunSuite with BeforeAndAfterAll{

  private var preprocessed:RDD[Structs.Trace_Vector]=_
  override def beforeAll(): Unit ={
    val filename = "input/financial_log.xes"
    val dims = 10
    Logger.getLogger("org").setLevel(Level.ERROR)
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    val log = Utils.read_xes(filename)
    preprocessed=Preprocess.preprocess(log,dims,Utils.convert_to_vector_both_duration_repetitions)
  }
//  test("Initialize k-neighbors with naive method"){
//    val minPts = 50 //number of nearest neighbors
//    val lof= new LOF(preprocessed,minPts,Distances.distanceRMSE)
//    lof.initialize(InitializeNeighbors.init_naive)
//    assert(lof.get_distances().count()==preprocessed.count())
//    assert(lof.get_distances().first().distances.length==minPts)
//  }
//  test("Outlying Factor"){
//    val minPts = 50 //number of nearest neighbors
//    val lof= new LOF(preprocessed,minPts,Distances.distanceRMSE)
//    lof.initialize(InitializeNeighbors.init_naive)
//    val lofAssigned=lof.assignOutlierFactor()
//    lofAssigned.collect().foreach(x=>{
//      println(x._1.id,x._2)
//    })
//  }

}
