package Utils
import scala.io.Source
object Results {

  def read(filename:String):List[(Int,Int)]={
    Source.fromFile(filename).getLines().map(line=>{
      val x=line.split(",")
      (x(0).toInt,x(1).toInt)
    }).toList
  }

  def read_with_description(filename:String):List[(String,Int,Int)]={
    Source.fromFile(filename).getLines().map(line=>{
      val x=line.split(",")
      (x(0),x(1).toInt,x(2).toInt)
    }).toList
  }

}
