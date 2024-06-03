import 'package:isar/isar.dart';

part 'activity.g.dart'; // Ensure this line is present

@Collection()
class Activity {
  Id measurementId = Isar.autoIncrement; // Use Isar's auto-increment feature

  String? name;
  late DateTime timeStamp;
  String? description;

  Activity({this.name, required this.timeStamp, this.description});
}
