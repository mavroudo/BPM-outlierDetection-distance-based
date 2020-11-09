import org.apache.log4j.{Level, Logger}
import org.apache.spark.ml.feature.{PCA, StandardScaler}
import org.apache.spark.ml.linalg.{DenseVector, Vectors}

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.{Row, SQLContext, SparkSession}
import org.apache.spark.storage.StorageLevel

object TemporalTraceAnomalies {

  def main(args: Array[String]): Unit = {
    val filename = "input/financial_log.xes"
    val k = 13000 //number of nearest neighbors
    val dims = 40
    val zeta = 10
    val n =4
    Logger.getLogger("org").setLevel(Level.ERROR)
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    val log = Utils.read_xes(filename)
    val transformed = Utils.convert_to_vector_both_duration_repetitions(log) //create vectors
    val preparedForRdd = transformed.map(x => Tuple2.apply(x.id, Vectors.dense(x.elements))) //make it dataframe
    val df = spark.createDataFrame(preparedForRdd).toDF("id", "features")
    val normalizedDF = Utils.normalize(df) //normalize data
    val reduceDimensionalityDF = Utils.reduceDimensionalityPCA(normalizedDF, dims) //apply pca


    //method 1: broadcast them in order to create queries
    val backToRdd: RDD[Structs.Trace_Vector] = reduceDimensionalityDF.rdd.map(row => {
      Structs.Trace_Vector(row.getAs[Long]("id"), row.getAs[DenseVector]("pcaFeatures").values)
    }).persist(StorageLevel.MEMORY_AND_DISK)

    spark.time {
      val distances = NaiveMethod.initializeDistances(backToRdd,k)
      println("size: ",distances.first().distances.size)
      val sortedByOutlyingFactor=OutlierDetection.assignOutlyingFactor(distances, k)
      sortedByOutlyingFactor.persist(StorageLevel.MEMORY_AND_DISK)
      val outliers:Array[(Long,Double)]=sortedByOutlyingFactor.collect().sortBy(_._2).slice(0,zeta+1) //top zeta elements
      println("Outliers based on top zeta reported")
      outliers.foreach(println)
      println("Outliers based on deviating more than n times stdev from mean")
      val outliers_stats:RDD[(Long,Double)]=OutlierDetection.outlierBasedOnDeviation(sortedByOutlyingFactor,n)
      outliers_stats.foreach(println)

    }
    spark.stop()
  }
}
