package oultierDetectionAlgorithms

import Utils.Preprocess
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import Structs.Trace_Temporal_KNN

object ODAL {

  def find_outliers(log:Structs.Log,k:Int,n:Float):Array[Long]={
    val preprocessedRDD:RDD[Structs.Trace_Temporal_KNN]=this.preprocessForKnn(log)
    val spark=SparkSession.builder().getOrCreate()
    val traces=spark.sparkContext.broadcast(preprocessedRDD.collect())
    val kthNeighbor=preprocessedRDD.map(trace=>{
      val distances=traces.value.filter(_.signature==trace.signature)
        .map(x=>this.distance(x,trace))
        .sorted
      val point=Math.min(k+1,distances.length-1)
      (trace,distances(point),point)
    })
    outliers(kthNeighbor,n)

  }

  private def preprocessForKnn(log: Structs.Log): RDD[Trace_Temporal_KNN] = {
    log.traces.map(trace=>{
      val signature=new StringBuilder()
      trace.events.foreach(event=>{
        signature.append(event.task)
      })
      Structs.Trace_Temporal_KNN(trace.id,signature.toString(),trace.events.map(_.duration.toDouble))
    })
  }

  /**
   * The have the same signature
   * @param trace1
   * @param trace2
   * @return
   */
  private def distance(trace1:Trace_Temporal_KNN,trace2:Trace_Temporal_KNN):Double={
    trace1.durations.zip(trace2.durations)
      .map(x=>Math.abs(x._1-x._2))
      .sum
  }

  private def outliers(data: RDD[(Trace_Temporal_KNN, Double, Int)],n:Float):Array[Long]={
    val distances=data.map(_._2).collect()
    val mean_value=mean[Double](distances)
    val stdev_value=stdDev[Double](distances)
    data.filter(x=>x._2>mean_value+n*stdev_value)
      .map(_._1.id)
      .collect()
  }

  import Numeric.Implicits._

  def mean[T: Numeric](xs: Iterable[T]): Double = xs.sum.toDouble / xs.size

  def variance[T: Numeric](xs: Iterable[T]): Double = {
    val avg = mean(xs)

    xs.map(_.toDouble).map(a => math.pow(a - avg, 2)).sum / xs.size
  }

  def stdDev[T: Numeric](xs: Iterable[T]): Double = math.sqrt(variance(xs))

}
