import org.apache.spark.rdd.RDD

object Structs {

  case class Sequence(id: Long, events: List[Event])

  case class Event(task:String, timestamp:String, duration:Long)

  case class Log (traces:RDD[Sequence],activities:List[String])

  case class Trace_Vector(id:Long, elements:Array[Double])



}
