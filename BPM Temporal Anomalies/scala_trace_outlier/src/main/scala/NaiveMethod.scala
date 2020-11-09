import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.storage.StorageLevel

import scala.collection.mutable.ListBuffer


case class DistanceElement(id1: Long, id2: Long, distance: Double)

case class DistancesFromTrace(id: Long, distances: List[DistanceElement])

object NaiveMethod {

  def distance(v1: Structs.Trace_Vector, v2: Structs.Trace_Vector): Double = {
    var d: Double = 0
    v1.elements.zip(v2.elements).foreach(x => {
      d += math.pow(x._1 - x._2, 2)
    })
    math.sqrt(d / v1.elements.length)
  }

  def initializeDistances(traces: RDD[Structs.Trace_Vector], k: Int): RDD[DistancesFromTrace] = {
    val spark = SparkSession.builder().getOrCreate()
    val collected = traces.collect()
    val broadcasted = spark.sparkContext.broadcast(collected)
    val distances = traces.map(v1 => {
      val distanceList = broadcasted.value.map(v2 => {
        DistanceElement(v1.id, v2.id, this.distance(v1, v2))
      }).toList
      DistancesFromTrace(v1.id, distanceList.sortBy(_.distance))
    })
      .map(x => {
        DistancesFromTrace(x.id, x.distances.slice(1, k + 1))
      })
      .persist(StorageLevel.MEMORY_AND_DISK)
    distances
  }


}
